import os
import json
import numpy as np
from PIL import Image, ImageDraw

# Verilen dosya ve klasör yolları
label_file_path = r"C:\Users\ceren\Desktop\2_CAP_labeled\Label.txt"
image_folder = r"C:\Users\ceren\Desktop\2_CAP_labeled"
output_folder = r"C:\Users\ceren\Desktop\2_CAP_labeled\crop_img"

# Çıktı klasörünü oluştur (varsa hata vermez)
os.makedirs(output_folder, exist_ok=True)

# Label.txt dosyasını oku
with open(label_file_path, 'r') as file:
    lines = file.readlines()

# Her satırı işle
for line in lines:
    # Satırı dosya adı ve JSON verisi olarak ayır
    image_file, json_data = line.strip().split('\t')
    
    # Görselin tam yolunu oluştur
    image_path = os.path.join(image_folder, os.path.basename(image_file))
    
    # JSON verisini yükle
    data = json.loads(json_data)
    
    # Görseli aç
    image = Image.open(image_path).convert("RGBA")
    
    # Her obje için kırpma işlemini yap
    for i, item in enumerate(data):
        points = item['points']
        
        # Koordinatları uygun formata dönüştür
        polygon = [(int(x), int(y)) for (x, y) in points]
        
        # Maske oluştur
        mask = Image.new("L", image.size, 0)
        ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=255)
        
        # Görseli maske ile kes
        cropped_image = Image.new("RGBA", image.size)
        cropped_image.paste(image, mask=mask)
        
        # Kırpılan bölgeyi bul
        bbox = mask.getbbox()
        cropped_image = cropped_image.crop(bbox)
        
        # Kırpılan görseli kaydet
        cropped_image_name = f"{os.path.splitext(os.path.basename(image_file))[0]}_crop_{i}.png"
        cropped_image_path = os.path.join(output_folder, cropped_image_name)
        cropped_image.save(cropped_image_path)
    
    print(f"{os.path.basename(image_file)} için kırpma işlemi tamamlandı.")