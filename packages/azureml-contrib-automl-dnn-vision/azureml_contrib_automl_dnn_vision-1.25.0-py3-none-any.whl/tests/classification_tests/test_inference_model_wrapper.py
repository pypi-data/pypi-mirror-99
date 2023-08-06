import json
import os
import tempfile
from pathlib import Path

import pytest

from PIL import Image

import torch

from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.common.utils import _get_default_device
from azureml.contrib.automl.dnn.vision.classification.common.transforms import _get_common_valid_transforms
from azureml.contrib.automl.dnn.vision.classification.inference.score import _featurize_with_model, _score_with_model
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.common.classification_utils import _load_model_wrapper

from tests.common.run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock, LabeledDatasetFactoryMock

from azureml.contrib.automl.dnn.vision.common.artifacts_utils import save_model_checkpoint


@pytest.mark.usefixtures('new_clean_dir')
class TestInferenceModelWrapper:
    def test_inference_cpu(self, image_dir):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_name = 'seresnext'
            model_wrapper = ModelFactory().get_model_wrapper(model_name,
                                                             10,
                                                             multilabel=False,
                                                             device='cpu',
                                                             distributed=False,
                                                             rank=0)
            # save the model wrapper
            save_model_checkpoint(epoch=1,
                                  model_name=model_name,
                                  number_of_classes=model_wrapper.number_of_classes,
                                  specs={'multilabel': model_wrapper.multilabel, 'labels': model_wrapper.labels},
                                  model_state=model_wrapper.state_dict(),
                                  optimizer_state={},
                                  lr_scheduler_state={},
                                  output_dir=tmp_output_dir)

            model_file = os.path.join(tmp_output_dir, ArtifactLiterals.MODEL_FILE_NAME)
            inference_model = _load_model_wrapper(model_file, False, 0, 'cpu')
            assert inference_model.labels == model_wrapper.labels

            image_path = os.path.join(image_dir, 'crack_1.jpg')
            im = Image.open(image_path)

            tensor_image = torch.stack([inference_model._resize_and_crop(im)], dim=0)
            outputs = inference_model.model(tensor_image)
            probs = inference_model.predict_probs_from_outputs(outputs)

            assert probs.shape[1] == model_wrapper.number_of_classes
            assert inference_model._featurizer(tensor_image).shape[0] == 1

    def test_featurization(self, root_dir, image_dir, src_image_list_file_name):
        image_class_list_file_path = os.path.join(root_dir, src_image_list_file_name)
        batch_size_list = range(1, 3)
        self._featurization_test(root_dir, image_dir, image_class_list_file_path, batch_size_list, 4)

    @staticmethod
    def _write_image_list_to_file(image_dir, image_class_list_file_path):
        Path(image_class_list_file_path).touch()
        with open(image_class_list_file_path, mode="w") as fp:
            for image_file in os.listdir(image_dir):
                fp.write(image_file + "\n")

    def test_featurization_invalid_image_file(self, root_dir, image_dir, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            temp_image_class_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            self._write_image_list_to_file(image_dir, temp_image_class_list_file_path)
            expected_feature_file_length = 4  # Should not include invalid image.
            self._featurization_test(root_dir, image_dir, temp_image_class_list_file_path, [3],
                                     expected_feature_file_length)
            self._featurization_test(root_dir, image_dir, temp_image_class_list_file_path, [1],
                                     expected_feature_file_length)

    @staticmethod
    def _featurization_test(root_dir, image_dir, image_class_list_file_path,
                            batch_size_list, expected_feature_file_length):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_name = 'seresnext'
            device = _get_default_device()
            model_wrapper = ModelFactory().get_model_wrapper(model_name,
                                                             10,
                                                             multilabel=False,
                                                             device=device,
                                                             distributed=False,
                                                             rank=0)

            # run featurizations
            featurization_file = 'features.txt'
            features_output_file = os.path.join(tmp_output_dir, featurization_file)

            Path(features_output_file).touch()

            model_wrapper.transforms = _get_common_valid_transforms(
                resize_to=model_wrapper.resize_to_size,
                crop_size=model_wrapper.crop_size
            )

            for batch_size in batch_size_list:
                TestInferenceModelWrapper._featurization_batch_test(features_output_file, image_dir,
                                                                    image_class_list_file_path,
                                                                    model_wrapper, batch_size,
                                                                    expected_feature_file_length)

    @staticmethod
    def _featurization_batch_test(features_output_file, image_dir,
                                  image_class_list_file_path, inference_model_wrapper, batch_size,
                                  expected_feature_file_length):

        datastore_name = "TestDatastoreName"
        datastore_mock = DatastoreMock(datastore_name)
        workspace_mock = WorkspaceMock(datastore_mock)
        experiment_mock = ExperimentMock(workspace_mock)
        run_mock = RunMock(experiment_mock)

        _featurize_with_model(inference_model_wrapper, run_mock, root_dir=image_dir,
                              output_file=features_output_file,
                              image_list_file=image_class_list_file_path,
                              device=_get_default_device(),
                              batch_size=batch_size, num_workers=0)

        with open(features_output_file) as fp:
            for line in fp:
                obj = json.loads(line.strip())
                assert 'filename' in obj
                assert 'feature_vector' in obj
                assert len(obj['feature_vector']) > 0
        with open(features_output_file) as fp:
            lines = fp.readlines()
        assert len(lines) == expected_feature_file_length

    def test_score(self, root_dir, image_dir, src_image_list_file_name):
        image_class_list_file_path = os.path.join(root_dir, src_image_list_file_name)
        self._score_test(root_dir, image_dir, image_class_list_file_path, 4, 10)

    def test_score_invalid_image_file(self, root_dir, image_dir, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            temp_image_class_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            self._write_image_list_to_file(image_dir, temp_image_class_list_file_path)
            expected_score_file_length = 4  # Should not include invalid image.
            self._score_test(root_dir, image_dir, temp_image_class_list_file_path,
                             expected_score_file_length, 10)
            self._score_test(root_dir, image_dir, temp_image_class_list_file_path,
                             expected_score_file_length, 1)

    @staticmethod
    def _score_test(root_dir, image_dir, image_class_list_file_path, expected_score_file_length, batch_size):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_name = 'seresnext'
            device = _get_default_device()
            model_wrapper = ModelFactory().get_model_wrapper(model_name,
                                                             10,
                                                             multilabel=False,
                                                             device=device,
                                                             distributed=False,
                                                             rank=0)

            # run predictions
            predictions_file = 'predictions.txt'
            predictions_output_file = os.path.join(tmp_output_dir, predictions_file)

            datastore_name = "TestDatastoreName"
            datastore_mock = DatastoreMock(datastore_name)
            workspace_mock = WorkspaceMock(datastore_mock)
            experiment_mock = ExperimentMock(workspace_mock)
            run_mock = RunMock(experiment_mock)
            test_dataset_id = 'a2458938-7966-4ca0-b4ba-a97d89d4eb2b'
            labeled_dataset_factory_mock = LabeledDatasetFactoryMock(test_dataset_id)
            test_target_path = "TestTargetPath"
            labeled_dataset_file = os.path.join(tmp_output_dir, 'labeled_dataset.json')

            Path(predictions_output_file).touch()
            Path(labeled_dataset_file).touch()

            model_wrapper.transforms = _get_common_valid_transforms(
                resize_to=model_wrapper.resize_to_size,
                crop_size=model_wrapper.crop_size
            )

            _score_with_model(model_wrapper, run_mock, test_target_path,
                              root_dir=image_dir,
                              output_file=predictions_output_file,
                              image_list_file=image_class_list_file_path,
                              device=device,
                              labeled_dataset_factory=labeled_dataset_factory_mock,
                              always_create_dataset=True,
                              num_workers=0,
                              labeled_dataset_file=labeled_dataset_file,
                              batch_size=batch_size)

            with open(predictions_output_file) as fp:
                for line in fp:
                    obj = json.loads(line.strip())
                    assert 'filename' in obj
                    assert 'probs' in obj
                    assert len(obj['probs']) > 0
            with open(predictions_output_file) as fp:
                lines = fp.readlines()
            assert len(lines) == expected_score_file_length

            assert labeled_dataset_factory_mock.task == "ImageClassification"
            expected_path = test_target_path + "/labeled_dataset.json"
            assert labeled_dataset_factory_mock.path == expected_path

            assert len(datastore_mock.files) == 1

            (files, root_dir, target_path, overwrite) = datastore_mock.files[0]
            assert len(files) == 1
            assert root_dir == tmp_output_dir
            assert target_path == test_target_path
            assert overwrite

            assert len(datastore_mock.dataset_file_content) == expected_score_file_length

            for line in datastore_mock.dataset_file_content:
                line_contents = json.loads(line)
                assert line_contents['image_url'].startswith('AmlDatastore://')
                assert 'label' in line_contents
                assert 'label_confidence' in line_contents

            assert run_mock.properties['labeled_dataset_id'] == test_dataset_id
