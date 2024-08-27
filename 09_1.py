import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def polygon_to_bbox(polygon_points):
    """Verilen çokgen noktalarını bounding box'a dönüştürür."""
    x_coords = polygon_points[0::2]
    y_coords = polygon_points[1::2]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    return x_min, y_min, x_max, y_max

def iou(box1, box2):
    """İki bounding box arasında Intersection over Union (IoU) hesaplar."""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area != 0 else 0

def get_id(line):
    """Verilen satırın ilk karakterini sınıf id'si olarak döndürür."""
    return int(line.strip().split()[0])

def calculate_iou(gt_polygon, pred_polygon):
    """Verilen ground truth ve tahmin çokgenlerinden IoU hesaplar."""
    gt_bbox = polygon_to_bbox(gt_polygon)
    pred_bbox = polygon_to_bbox(pred_polygon)
    return iou(gt_bbox, pred_bbox)

def compare_labels(gt_folder, pred_folder):
    """Ground truth ve prediction etiketlerini karşılaştırarak TP, FP, FN hesaplar."""
    tp_0, fp_0, fn_0 = 0, 0, 0
    tp_1, fp_1, fn_1 = 0, 0, 0

    gt_labels = sorted([os.path.join(gt_folder, f) for f in os.listdir(gt_folder) if os.path.isfile(os.path.join(gt_folder, f))])
    pred_labels = sorted([os.path.join(pred_folder, f) for f in os.listdir(pred_folder) if os.path.isfile(os.path.join(pred_folder, f))])

    for gt_label in gt_labels:
        with open(gt_label, 'r') as gt_file:
            gt_lines = gt_file.readlines()

        matched_predictions = []

        for gt_line in gt_lines:
            gt_id = get_id(gt_line)
            gt_polygon = list(map(float, gt_line.strip().split()[1:]))

            found_match = False

            for pred_label in pred_labels:
                if os.path.basename(pred_label) == os.path.basename(gt_label):  # Dosya isimleri aynıysa
                    with open(pred_label, 'r') as pred_file:
                        pred_lines = pred_file.readlines()

                    for pred_line in pred_lines:
                        pred_id = get_id(pred_line)
                        pred_polygon = list(map(float, pred_line.strip().split()[1:]))

                        iou_value = calculate_iou(gt_polygon, pred_polygon)

                        if gt_id == pred_id and iou_value > 0.5:
                            if gt_id == 0:
                                tp_0 += 1
                            elif gt_id == 1:
                                tp_1 += 1
                            found_match = True
                            matched_predictions.append(pred_line)
                            break

            if not found_match:
                if gt_id == 0:
                    fn_0 += 1
                elif gt_id == 1:
                    fn_1 += 1

        # False Positives (FP) hesapla:
        for pred_label in pred_labels:
            if os.path.basename(pred_label) == os.path.basename(gt_label):  # Dosya isimleri aynıysa
                with open(pred_label, 'r') as pred_file:
                    pred_lines = pred_file.readlines()

                for pred_line in pred_lines:
                    if pred_line not in matched_predictions:
                        pred_id = get_id(pred_line)
                        if pred_id == 0:
                            fp_0 += 1
                        elif pred_id == 1:
                            fp_1 += 1

    print(f"Class 0 için:")
    print(f"True Positives (TP): {tp_0}, False Positives (FP): {fp_0}, False Negatives (FN): {fn_0}\n")
    
    print(f"Class 1 için:")
    print(f"True Positives (TP): {tp_1}, False Positives (FP): {fp_1}, False Negatives (FN): {fn_1}\n")

    return (tp_0, fp_0, fn_0), (tp_1, fp_1, fn_1)

# Kullanım:
gt_folder = r"C:\Users\ceren\Desktop\labels_compare\test_gt"
pred_folder = r"C:\Users\ceren\Desktop\labels_compare\test_pred"

# compare_labels fonksiyonunu çağır ve dönen değerleri al:
(tp_0, fp_0, fn_0), (tp_1, fp_1, fn_1) = compare_labels(gt_folder, pred_folder)

compare_labels(gt_folder, pred_folder)



# ---- precision | recall | f1 score -----------
def calculate_precision(tp, fp):
    """Precision hesaplaması."""
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)

def calculate_recall(tp, fn):
    """Recall hesaplaması."""
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)

def calculate_f1(precision, recall):
    """F1 Skoru hesaplaması."""
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)

# Precision ve Recall değerlerini hesapla:
precision_0 = calculate_precision(tp_0, fp_0)
recall_0 = calculate_recall(tp_0, fn_0)

f1_score_0 = calculate_f1(precision_0, recall_0)


precision_1 = calculate_precision(tp_1, fp_1)
recall_1 = calculate_recall(tp_1, fn_1)

f1_score_1 = calculate_f1(precision_1, recall_1)



print(f"Class 0 Precision: {precision_0:.4f}, Recall: {recall_0:.4f}")
print(f"Class 1 Precision: {precision_1:.4f}, Recall: {recall_1:.4f}")


print(f"Class 0 F1 Skoru: {f1_score_0:.4f}")
print(f"Class 1 F1 Skoru: {f1_score_1:.4f}")


# ************************** confusion matrix

tn_0  = 0
tn_1 = 0





