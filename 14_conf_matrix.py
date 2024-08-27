import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    """Ground truth ve prediction etiketlerini karşılaştırarak çeşitli sayımları yapar."""
    x, y, z, t = 0, 0, 0, 0
    a, b, c, d = 0, 0, 0, 0

    gt_labels = sorted([os.path.join(gt_folder, f) for f in os.listdir(gt_folder) if os.path.isfile(os.path.join(gt_folder, f))])
    pred_labels = sorted([os.path.join(pred_folder, f) for f in os.listdir(pred_folder) if os.path.isfile(os.path.join(pred_folder, f))])

    for gt_label in gt_labels:  # Ground truth dosyasındaki her bir ground truth etiketi boyunca
        with open(gt_label, 'r') as gt_file:
            gt_lines = gt_file.readlines()

        corresponding_pred_label = next((pl for pl in pred_labels if os.path.basename(pl) == os.path.basename(gt_label)), None)
        
        if corresponding_pred_label:
            with open(corresponding_pred_label, 'r') as pred_file:
                pred_lines = pred_file.readlines()
            
            for gt_line in gt_lines:  # Ground truth etiketindeki her satır için
                gt_id = get_id(gt_line)
                gt_polygon = list(map(float, gt_line.strip().split()[1:]))

                best_iou = 0
                best_pred_id = None

                for pred_line in pred_lines:  # Predict txt'sindeki her satır için
                    pred_id = get_id(pred_line)
                    pred_polygon = list(map(float, pred_line.strip().split()[1:]))
                    iou_value = calculate_iou(gt_polygon, pred_polygon)  # İlgili iki ground truth ve predict satırındaki koordinatların IoU hesaplaması

                    if iou_value > best_iou:
                        best_iou = iou_value
                        best_pred_id = pred_id

                if best_iou > 0.5:
                    if gt_id == 0 and best_pred_id == 0:
                        x += 1
                    elif gt_id == 1 and best_pred_id == 1:
                        t += 1
                    elif gt_id == 0 and best_pred_id == 1:
                        y += 1
                    elif gt_id == 1 and best_pred_id == 0:
                        z += 1
                else:
                    if gt_id == 0:
                        a += 1
                    elif gt_id == 1:
                        b += 1
        else:
            # Eğer karşılık gelen bir predict etiketi yoksa
            for gt_line in gt_lines:
                gt_id = get_id(gt_line)
                if gt_id == 0:
                    c += 1
                elif gt_id == 1:
                    d += 1

    print(f"x: {x}, y: {y}, z: {z}, t: {t}, a: {a}, b: {b}, c: {c}, d: {d}")
    return x, y, z, t, a, b, c, d

# Kullanım:
gt_folder = r"C:\Users\ceren\Desktop\labels_compare\test_gt"
pred_folder = r"C:\Users\ceren\Desktop\labels_compare\30_0_100__fr_lr\labels"

# compare_labels fonksiyonunu çağır ve dönen değerleri al:
x, y, z, t, a, b, c, d = compare_labels(gt_folder, pred_folder)

# Confusion matrix olarak değerlerinizi yerleştirin
confusion_matrix = np.array([[x, y, c],
                             [z, t, d],
                             [a, b, 0]])

# Matrisin görselleştirilmesi
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues", cbar=False, 
            xticklabels=[0, 1, ''], yticklabels=[0, 1, ''])

# Eksen başlıkları
plt.xlabel('Predicted Labels')
plt.ylabel('Ground truth Labels')
plt.title('Confusion Matrix')

# Görseli göster
plt.show()