import os
import numpy as np
from collections import defaultdict

def get_bounding_box(coordinates):
    if len(coordinates) % 2 != 0:
        coordinates = coordinates[:-1]
    
    coords = np.array(coordinates).reshape(-1, 2)
    min_x, min_y = coords.min(axis=0)
    max_x, max_y = coords.max(axis=0)
    return [min_x, min_y, max_x, max_y]

def process_label_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read().strip().split()
    
    class_id = int(content[0])
    coordinates = [float(coord) for coord in content[1:]]
    bounding_box = get_bounding_box(coordinates)
    
    return class_id, bounding_box

def process_folder(folder_path):
    results = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                class_id, bounding_box = process_label_file(file_path)
                results[filename] = (class_id, bounding_box)
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
    return results

def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    x_left = max(x1, x3)
    y_top = max(y1, y3)
    x_right = min(x2, x4)
    y_bottom = min(y2, y4)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x4 - x3) * (y4 - y3)

    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

def calculate_ap(recalls, precisions):
    mrec = np.concatenate(([0.], recalls, [1.]))
    mpre = np.concatenate(([0.], precisions, [0.]))

    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    i = np.where(mrec[1:] != mrec[:-1])[0]
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap

def calculate_map50(gt_results, pred_results, iou_threshold=0.5):
    class_metrics = defaultdict(lambda: {"tp": [], "fp": [], "scores": [], "num_gt": 0})
    
    for filename in gt_results:
        gt_class, gt_box = gt_results[filename]
        class_metrics[gt_class]["num_gt"] += 1
        
        if filename in pred_results:
            pred_class, pred_box = pred_results[filename]
            pred_score = 1.0  # Assuming a confidence score of 1 for all predictions
            iou = calculate_iou(gt_box, pred_box)
            
            if iou >= iou_threshold and gt_class == pred_class:
                class_metrics[gt_class]["tp"].append(1)
                class_metrics[gt_class]["fp"].append(0)
                class_metrics[gt_class]["scores"].append(pred_score)
            else:
                class_metrics[gt_class]["tp"].append(0)
                class_metrics[gt_class]["fp"].append(1)
                class_metrics[gt_class]["scores"].append(pred_score)

    aps = []
    for class_id, metrics in class_metrics.items():
        tp = np.array(metrics["tp"])
        fp = np.array(metrics["fp"])
        scores = np.array(metrics["scores"])
        
        sorted_indices = np.argsort(-scores)
        tp = tp[sorted_indices]
        fp = fp[sorted_indices]
        
        tp_cumsum = np.cumsum(tp)
        fp_cumsum = np.cumsum(fp)
        
        recalls = tp_cumsum / metrics["num_gt"]
        precisions = tp_cumsum / (tp_cumsum + fp_cumsum)
        
        ap = calculate_ap(recalls, precisions)
        aps.append(ap)
    
    mAP50 = np.mean(aps)
    return mAP50

def calculate_metrics(gt_results, pred_results, iou_threshold=0.7):
    tp = 0
    fp = 0
    fn = 0

    for filename in gt_results:
        gt_class, gt_box = gt_results[filename]
        
        if filename in pred_results:
            pred_class, pred_box = pred_results[filename]
            iou = calculate_iou(gt_box, pred_box)
            
            if iou >= iou_threshold and gt_class == pred_class:
                tp += 1
            else:
                fp += 1
        else:
            fn += 1

    for filename in pred_results:
        if filename not in gt_results:
            fp += 1

    return tp, fp, fn

# Ana işlem
gt_folder = r"D:\download\DOWNLOAD\testarttiroo\train\groundtruth"
pred_folder = r"D:\download\DOWNLOAD\labelasasasas\labels"

gt_results = process_folder(gt_folder)
pred_results = process_folder(pred_folder)

tp, fp, fn = calculate_metrics(gt_results, pred_results)

print(f"True Positives: {tp}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

# Precision, Recall ve F1-score hesaplama
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1_score:.4f}")

# mAP50 hesaplama
mAP50 = calculate_map50(gt_results, pred_results)
print(f"mAP50: {mAP50:.4f}")