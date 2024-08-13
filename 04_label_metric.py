import os
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def read_labels(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [int(line.split()[0]) for line in lines]

def get_labels(folder_path):
    labels = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            labels[file_name] = read_labels(file_path)
    return labels

gt_folder = r"C:\Users\ceren\Desktop\labels\gt_labels"
pred_folder = r"C:\Users\ceren\Desktop\labels\predict_labels"

gt_labels = get_labels(gt_folder)
pred_labels = get_labels(pred_folder)

y_true = []
y_pred = []

for file_name in gt_labels.keys():
    if file_name in pred_labels:
        gt = gt_labels[file_name]
        pred = pred_labels[file_name]
        
        # Eğer tahmin dosyasında birden fazla etiket varsa, ilkini al
        gt_label = gt[0] if gt else 0
        pred_label = pred[0] if pred else 0
        
        y_true.append(gt_label)
        y_pred.append(pred_label)

classes = [0, 1]

for cls in classes:
    print(f"Sınıf {cls} için metrikler:")
    
    y_true_bin = [1 if label == cls else 0 for label in y_true]
    y_pred_bin = [1 if label == cls else 0 for label in y_pred]
    
    tn, fp, fn, tp = confusion_matrix(y_true_bin, y_pred_bin).ravel()
    
    precision = precision_score(y_true_bin, y_pred_bin)
    recall = recall_score(y_true_bin, y_pred_bin)
    f1 = f1_score(y_true_bin, y_pred_bin)
    
    print(f"True Positives: {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Negatives: {tn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\n")