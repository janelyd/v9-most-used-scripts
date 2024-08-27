import os
import json
from PIL import Image

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
    
    # Bounding box için min ve max koordinatları belirle
    min_x = min([min([p[0] for p in item['points']]) for item in data])
    max_x = max([max([p[0] for p in item['points']]) for item in data])
    min_y = min([min([p[1] for p in item['points']]) for item in data])
    max_y = max([max([p[1] for p in item['points']]) for item in data])
    
    # Görseli bounding box'a göre kırp
    cropped_image = image.crop((min_x, min_y, max_x, max_y))
    
    # Kırpılan görseli kaydet
    cropped_image_name = f"{os.path.splitext(os.path.basename(image_file))[0]}_cropped.png"
    cropped_image_path = os.path.join(output_folder, cropped_image_name)
    cropped_image.save(cropped_image_path)
    
    print(f"{os.path.basename(image_file)} için kırpma işlemi tamamlandı.")