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
    
    iou = inter_area / union_area if union_area != 0 else 0
    
    # Sadece IoU'yu return ediyoruz, korunma koşulu eklenmiş şekilde
    return iou

# kullanımı:

# # Çokgenleri bounding box'a dönüştür
# box1 = polygon_to_bbox(polygon1)
# box2 = polygon_to_bbox(polygon2)

# # Bounding box'lar arasındaki IoU'yu hesapla
# iou_value = iou(box1, box2)



def get_id(file_path):
    """ Verilen dosya yolundaki ilk satırın ilk karakterini okur ve döndürür."""
    with open(file_path, 'r') as file:
        line = file.readline().strip()  # İlk satırı oku ve boşlukları temizle
        if line:  # Satır boş değilse
            return line[0]  # İlk karakteri döndür
    return None  # Eğer dosya boşsa veya ilk satır boşsa None döndür

# Örnek kullanım
file_path = 'data.txt'  # Buraya dosyanızın yolunu yazın
id = get_id(file_path)

# ------------- ---------- main code -------- -------------



gt_labels = r"C:\Users\ceren\Desktop\labels_compare\test_gt"
predicted_labels = r"C:\Users\ceren\Desktop\labels_compare\test_pred"

gt_label = # gt_labels klasörünün içindeki txt dosyalarının her biri
predicted_label = # predicted_labels klasörünün içindeki txt dosyalarının her biri

# ---- 0 için -----
tp_0, fp_0, fn_0 = 0

# ---- 1 için -----
tp_1, fp_1, fn_1 = 0




for gt_label in gt_labels: # ground truth klasöründeki her txt dosyası için
    gt_id = get_id(gt_label) #  ground truth txt sinin ilk karakterini al
    if gt_id == 0:
        for predicted_label in predicted_labels: # predict klasöründeki her predict klasörü için 
            if predicted_label exists in gt_labels: # sıradaki predict txt dosyasının aynısı ground truth klasöründe de var ise
                for line in predicted_label: # predict txt sindeki her satır için bu işlemi yap
                    predicted_id = get_id(line) # ilgili satırsaki ilk karakteri al, bu senin sınıfın
                    if gt_id == predicted_id: # eğer ground truthtaki sınıfın ile , ynı isimdeki predict txtdeki sınıfın aynı ise
                        iou = calculate_iou(gt_label,predicted_label) # ilgili iki etiket arasında iou hesabı yap
                        if iou > 0.5: 
                            tp_0 = tp_0 + 1
                        else
                            fp_0 = fp_0 + 1
                    elif gt_id != predicted_id:
                        if iou > 0.5:
                            tp_0 = tp_0 + 1
                        else
                            fp_0 = fp_0 + 1

    elif gt_id == 1:
        for predicted_label in predicted_labels: # predict klasöründeki her predict klasörü için 
            if predicted_label exists in gt_labels: # sıradaki predict txt dosyasının aynısı ground truth klasöründe de var ise
                for line in predicted_label: # predict txt sindeki her satır için bu işlemi yap
                    predicted_id = get_id(line) # ilgili satırsaki ilk karakteri al, bu senin sınıfın
                    if gt_id == predicted_id: # eğer ground truthtaki sınıfın ile , ynı isimdeki predict txtdeki sınıfın aynı ise
                        iou = calculate_iou(gt_label,predicted_label) # ilgili iki etiket arasında iou hesabı yap
                        if iou > 0.5: 
                            fp_1 = fp_1 + 1
                        else
                            fp_1 = fp_1 + 1
                    elif gt_id != predicted_id:
                        if iou > 0.5:
                            fp_1 = fp_1 + 1
                        else
                            fp_1 = fp_1 + 1



print(" 0 sınıfı için")
print("tp: \
      fp: \
      fn")

print(" 1 sınıfı için")
print("tp: \
      fp: \
      fn")


 