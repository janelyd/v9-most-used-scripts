import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def polygon_to_bbox(polygon_points):
    x_coords = polygon_points[0::2]
    y_coords = polygon_points[1::2]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    return x_min, y_min, x_max, y_max

def iou(box1, box2):
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
    
    iou = inter_area / union_area if union_area != 0 else 0 # korunma koşulu?
    
    # Sadece IoU'yu return ediyoruz, korunma koşulu eklenmiş şekilde
    return iou

def process_files(gt_folder, pred_folder, iou_threshold=0.5):
    y_true = []
    y_pred = []

    for filename in os.listdir(gt_folder):
        if filename.endswith('.txt'):
            gt_path = os.path.join(gt_folder, filename)
            pred_path = os.path.join(pred_folder, filename)

            with open(gt_path, 'r') as gt_file:
                gt_lines = gt_file.readlines()

            if not os.path.exists(pred_path):
                # Eğer predict dosyası yoksa, tüm ground truth sınıfları için FN artır.
                for line in gt_lines:
                    class_id = int(line.strip().split()[0])
                    y_true.append(class_id)
                    y_pred.append(-1)  # Negatif sınıfı temsil etmesi için
                continue

            with open(pred_path, 'r') as pred_file:
                pred_lines = pred_file.readlines()

            gt_boxes = []
            pred_boxes = []

            for line in gt_lines:
                split_line = list(map(float, line.strip().split()))
                class_id = int(split_line[0])
                bbox = polygon_to_bbox(split_line[1:])
                gt_boxes.append((class_id, bbox))

            for line in pred_lines:
                split_line = list(map(float, line.strip().split()))
                class_id = int(split_line[0])
                bbox = polygon_to_bbox(split_line[1:])
                pred_boxes.append((class_id, bbox))

            matched_gt = set()
            matched_pred = set()

            for i, (gt_class, gt_bbox) in enumerate(gt_boxes):
                for j, (pred_class, pred_bbox) in enumerate(pred_boxes):
                    if gt_class == pred_class and iou(gt_bbox, pred_bbox) >= iou_threshold:
                        y_true.append(gt_class)
                        y_pred.append(pred_class)
                        matched_gt.add(i)
                        matched_pred.add(j)

            for i, (gt_class, _) in enumerate(gt_boxes):
                if i not in matched_gt:
                    y_true.append(gt_class)
                    y_pred.append(-1)

            for j, (pred_class, _) in enumerate(pred_boxes):
                if j not in matched_pred:
                    y_true.append(-1)
                    y_pred.append(pred_class)

    return y_true, y_pred

def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels + [-1])
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=labels + ['None'], yticklabels=labels + ['None'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

gt_folder = r"C:\Users\ceren\Desktop\labels_compare\test_gt"
pred_folder = r"C:\Users\ceren\Desktop\labels_compare\test_pred"
iou_threshold = 0.5

y_true, y_pred = process_files(gt_folder, pred_folder, iou_threshold)

print("Confusion Matrix:")
plot_confusion_matrix(y_true, y_pred, labels=[0, 1])