# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Voc Style mAP for evaluating model performance."""

import torch
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException
from .utils import prepare_dataset_for_eval
from ..common.constants import PredefinedLiterals
from ...common.logging_utils import get_logger

from pycocotools import mask as pycoco_mask

logger = get_logger(__name__)


def _map_score_voc_11_point_metric(precision_list, recall_list):
    """
    Compute mAP score using Voc 11 point metric.
    The maximum precision at 11 recall values (0, 0.1, ..., 1.0) is computed and the average of these precision
    values is used as the mAP score.
    precision_list and recall_list should have same dimensions.

    :param precision_list: List of precision values
    :type precision_list: torch.Tensor of shape (number of precision values)
    :param recall_list: List of recall values
    :type precision_list: torch.Tensor of shape (number of recall values)
    :return: mAP score computed
    :rtype: torch.Tensor of shape ()
    """

    if precision_list.shape != recall_list.shape:
        msg = "Precision list (shape {}) and recall list (shape {}) are not of same shape. " \
              "Cannot compute map score".format(precision_list.shape, recall_list.shape)
        logger.error(msg)
        raise AutoMLVisionSystemException(msg, has_pii=False)

    score = torch.tensor(0.0)
    for recall_threshold in torch.arange(0.0, 1.1, 0.1):
        valid_precisions = precision_list[recall_list >= recall_threshold]
        if valid_precisions.nelement() == 0:
            score += 0.0
        else:
            score += torch.max(valid_precisions)
    score /= 11.0
    return score


def _map_score_voc_auc(precision_list, recall_list):
    """
    Compute mAP score using Voc Area Under Curve (auc) metric.
    The recall values at which maximum precision changes are identified and these points of change are used
    to compute the area under precision recall curve.
    precision_list and recall_list should have same dimensions.

    :param precision_list: List of precision values
    :type precision_list: torch.Tensor of shape (number of precision values)
    :param recall_list: List of recall values
    :type precision_list: torch.Tensor of shape (number of recall values)
    :return: mAP score computed.
    :rtype: torch.Tensor of shape ()
    """

    if precision_list.shape != recall_list.shape:
        msg = "Precision list (shape {}) and recall list (shape {}) are not of same shape. " \
              "Cannot compute map score".format(precision_list.shape, recall_list.shape)
        logger.error(msg)
        raise AutoMLVisionSystemException(msg, has_pii=False)

    # Add precision 1 at recall 0 to beginning of tensor.
    precision_list = torch.cat((torch.tensor([1.0]), precision_list))
    recall_list = torch.cat((torch.tensor([0.0]), recall_list))

    # Identify indices corresponding to unique recall values in the recall_list.
    recall_delta = recall_list[1:] - recall_list[:-1]
    # Verify that recall_list is sorted
    if torch.lt(recall_delta, 0).any():
        msg = "Recall list is not sorted in ascending order. Cannot compute map score using auc."
        logger.error(msg)
        raise AutoMLVisionSystemException(msg, has_pii=False)

    recall_change_indices = (recall_delta.nonzero(as_tuple=True)[0] + 1).tolist()

    # Maximum precision at unique recall values.
    max_precision_list = torch.zeros(len(recall_change_indices) + 1)
    # Adjusted precision at unique recall values. Computed as maximum precision to the right of that recall value.
    adjusted_precision_list = torch.zeros(len(recall_change_indices) + 1)
    # Unique recall values.
    unique_recall_list = torch.zeros(len(recall_change_indices) + 1)

    same_recall_ranges = zip([0] + recall_change_indices, recall_change_indices + [len(recall_list)])
    for index, (recall_start, recall_end) in reversed(list(enumerate(same_recall_ranges))):
        unique_recall_list[index] = recall_list[recall_start]
        max_precision_list[index] = torch.max(precision_list[recall_start:recall_end])
        adjusted_precision_list[index] = max_precision_list[index]
        if index != adjusted_precision_list.shape[0] - 1:
            adjusted_precision_list[index] = max(adjusted_precision_list[index], adjusted_precision_list[index + 1])

    # Compute mAP as sum(adjusted_precision[i] * (unique_recall[i]-unique_recall[i-1]))
    score = torch.sum(torch.mul(adjusted_precision_list[1:], unique_recall_list[1:] - unique_recall_list[:-1]))

    return score


class VocMap:
    """
    VOC style map
    """
    PRECISION = "precision"
    RECALL = "recall"
    AVERAGE_PRECISION = "average_precision"
    MAP = "map"
    LABEL_METRICS = "label_metrics"

    def __init__(self, dataset):
        """

        :params dataset: Dataset with ground truth data used for evaluation.
        :type dataset: CommonObjectDetectionDatasetWrapper
        """
        coco_dataset = prepare_dataset_for_eval(dataset)
        self._dataset = dataset
        self._gt_boxes = coco_dataset["annotations"]
        self._iou_threshold = 0.5
        self._use_voc_11_point_metric = False
        self._epsilon = 1e-10

        self._labels = self._dataset.classes
        self._label_gts = {label: list(filter(lambda x: x["category_id"] == label, self._gt_boxes))
                           for label in self._labels}

    def compute(self, predictions, task="bbox"):
        """
        Compute per-label AP scores at fixed IoU threshold and mean AP across labels
        :param predictions: List of predictions.
        :type predictions: List
        :param task: Task type - Object detection (bbox) or Instance segmentation (segm)
        :type task: str
        :return: Dictionary containing
                 - mean precision, mean recall, mAP as float
                 - per-label precision, recall and AP scores as dict in the following format.
                    {"1": {"precision": torch.Tensor, "recall": torch.Tensor, "average_precision": torch.Tensor}...}
        :rtype: Dict
        """
        label_scores = {}
        for label in self._labels:
            if label != PredefinedLiterals.BG_LABEL:
                label_predictions = list(filter(lambda x: x["category_id"] == label, predictions))
                label_scores[self._dataset.label_to_index_map(label)] = self._map_precision_recall(label_predictions,
                                                                                                   label, task)

        def _mean_score(metric_name):
            # Compute mean score across labels.
            scores = [label_score[metric_name] for label_score in label_scores.values()]
            scores_list = torch.tensor(scores, dtype=torch.float)
            valid_score_indices = scores_list != -1
            mean_score = torch.sum(scores_list * valid_score_indices.float()) / torch.sum(valid_score_indices)
            return mean_score.item()

        result = {
            self.LABEL_METRICS: label_scores,
            self.PRECISION: _mean_score(self.PRECISION),
            self.RECALL: _mean_score(self.RECALL),
            self.MAP: _mean_score(self.AVERAGE_PRECISION)
        }

        return result

    def _categorize_prediction(self, prediction, label_gts, detected_gt_indices, task):
        """
        Categorize a prediction as true positive or false positive.
        :param prediction: Prediction that needs to be categorized.
        :type prediction: dict
        :param label_gts: Ground truths for this label.
        :type: label_gts: List of dicts
        :param detected_gt_indices: Indices of gts already detected.
            This tensor will be updated when a new true positive is found.
        :type: detected_gt_indices: torch.tensor of dtype torch.uint8 and shape (number of label_gts)
        :param task: Task type - bbox or segm
        :type task: str
        :return: 0 - False positive, 1 - True Positive, 2 - Neither
        """
        # Get image gts
        image_gt_indices = [index for index, gt in enumerate(label_gts) if gt["image_id"] == prediction["image_id"]]

        if not image_gt_indices:
            return 0

        # Get gt with maximum iou
        entityType = "segmentation" if task == "segm" else "bbox"
        image_gt_entities = [label_gts[entry][entityType] for entry in image_gt_indices]
        iscrowd = [int(label_gts[entry]["iscrowd"]) for entry in image_gt_indices]
        prediction_entity = [prediction[entityType]]
        ious = pycoco_mask.iou(prediction_entity, image_gt_entities, iscrowd)
        iou_prediction_gts = torch.from_numpy(ious[0])

        max_iou, max_iou_index = torch.max(iou_prediction_gts, dim=0)
        max_iou_index_in_label_gts = image_gt_indices[max_iou_index]

        # Logic to categorize
        result = 2
        if max_iou >= self._iou_threshold:
            max_iou_gt = label_gts[max_iou_index_in_label_gts]
            if not max_iou_gt["iscrowd"]:
                if detected_gt_indices[max_iou_index_in_label_gts] == 0:
                    result = 1
                    detected_gt_indices[max_iou_index_in_label_gts] = 1
                else:
                    # already detected. Count as False positive
                    result = 0
            else:
                # ignore it
                result = 2
        else:
            result = 0

        return result

    def _precision_recall_curve(self, predictions, label, task):
        """
        Compute precision at multiple recall levels for a particular label.
        :param predictions: List of predictions for the label.
        :type predictions: List of dict.
        :param label: Label that is of interest.
        :type label: str
        :param task: Task type - bbox or segm
        :type task: str
        :return: Tuple of list of precision and list of recall sorted in increasing order of recall.
                 Note that there can be duplicates in recall list.
        :rtype: Tuple of tensor.Tensor, tensor.Tensor if there are non crowd gts with the label,
                (None, None) otherwise.
        """

        label_gts = self._label_gts.get(label, [])
        label_gts_non_crowd = list(filter(lambda x: not x["iscrowd"], label_gts))

        if not label_gts_non_crowd:
            return None, None

        if not predictions:
            return torch.tensor([]), torch.tensor([])

        # Sort by descending order of score
        predictions_scores = torch.tensor([entry["score"] for entry in predictions], dtype=torch.float)
        predictions_order = torch.argsort(predictions_scores, descending=True)

        label_detected_gts = torch.zeros(len(label_gts), dtype=torch.uint8)
        # Note that true_positives and false_positives correspond to predictions in predictions_order
        # For example, true_positives[0] is category of highest score prediction in predictions,
        # not predictions[0].
        true_positives = torch.zeros(len(predictions), dtype=torch.uint8)
        false_positives = torch.zeros(len(predictions), dtype=torch.uint8)

        for index, prediction_index_tensor in enumerate(predictions_order):
            prediction = predictions[prediction_index_tensor.item()]
            prediction_category = self._categorize_prediction(prediction, label_gts, label_detected_gts, task)
            if prediction_category == 0:
                false_positives[index] = 1
            elif prediction_category == 1:
                true_positives[index] = 1

        cumulative_true_positives = torch.cumsum(true_positives, dim=0)
        cumulative_false_positives = torch.cumsum(false_positives, dim=0)
        precision_list = cumulative_true_positives / \
            (cumulative_true_positives + cumulative_false_positives + self._epsilon)
        recall_list = cumulative_true_positives / torch.tensor(len(label_gts_non_crowd), dtype=torch.float)

        return precision_list, recall_list

    def _map_precision_recall(self, predictions, label, task):
        """
        Compute the per-label average precision(mAP), precision, recall at fixed iou threshold.
        :param predictions: List of predictions for the label.
        :type predictions: List of dict
        :param label: label that is of interest
        :type label: str
        :param task: Task type - bbox or segm
        :type task: str
        :return: Per-label mAP score, precision, recall
        :rtype: Dict[str, torch.tensor of shape ()]
        """
        precision_list, recall_list = self._precision_recall_curve(predictions, label, task)

        if recall_list is None:
            # No non-crowd ground truths
            if not predictions:
                return {self.AVERAGE_PRECISION: torch.tensor(-1.0),
                        self.PRECISION: torch.tensor(-1.0),
                        self.RECALL: torch.tensor(-1.0)}
            else:
                return {self.AVERAGE_PRECISION: torch.tensor(-1.0),
                        self.PRECISION: torch.tensor(0.0),
                        self.RECALL: torch.tensor(-1.0)}

        if recall_list.nelement() == 0:
            # No predictions, has non-crowd ground truths
            return {self.AVERAGE_PRECISION: torch.tensor(0.0),
                    self.PRECISION: torch.tensor(-1.0),
                    self.RECALL: torch.tensor(0.0)}

        result = {self.PRECISION: precision_list[-1], self.RECALL: recall_list[-1]}
        if self._use_voc_11_point_metric:
            score = _map_score_voc_11_point_metric(precision_list, recall_list)
        else:
            score = _map_score_voc_auc(precision_list, recall_list)
        result[self.AVERAGE_PRECISION] = score

        return result
