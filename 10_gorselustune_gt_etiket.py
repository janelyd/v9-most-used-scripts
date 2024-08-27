import os
import cv2
import numpy as np

# Görüntülerin bulunduğu klasör
image_folder = r"D:\download\DOWNLOAD\exp14testleri\exp14"

# Etiketlerin bulunduğu klasör
label_folder = r"C:\Users\ceren\Desktop\labels_compare\grountruth_labels"

# Görüntü dosyalarını listele
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

for image_file in image_files:
    # Etiket dosyasının adını oluştur
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(label_folder, label_file)
    
    # Etiket dosyası varsa işleme devam et
    if os.path.exists(label_path):
        # Görüntüyü oku
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        
        # Görüntü boyutlarını al
        height, width = image.shape[:2]
        
        # Etiket dosyasını oku
        with open(label_path, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            # Etiket değerini ve koordinatları al
            parts = line.strip().split()
            label = parts[0]
            coords = list(map(float, parts[1:]))
            
            # Koordinatları piksel konumlarına çevir
            pixels = [(int(x * width), int(y * height)) for x, y in zip(coords[::2], coords[1::2])]
            
            # Bounding box'ı hesapla
            x_min = min(p[0] for p in pixels)
            y_min = min(p[1] for p in pixels)
            x_max = max(p[0] for p in pixels)
            y_max = max(p[1] for p in pixels)
            
            # Bounding box'ı çiz
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
            
            # Etiket değerini yaz
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, label, (x_min, y_min-10), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        # Görüntüyü kaydet
        cv2.imwrite(image_path, image)

print("İşlem tamamlandı.")