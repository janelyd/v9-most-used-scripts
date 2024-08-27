import os
from PIL import Image

# Dönüştürmek istediğiniz klasörün yolu
input_folder = r"C:\Users\ceren\Desktop\2_CAP"
output_folder = r"C:\Users\ceren\Desktop\2_CAP\jpeg_output"

# Çıktı klasörünü oluştur (varsa hata vermez)
os.makedirs(output_folder, exist_ok=True)

# Klasördeki tüm dosyaları döngüye al
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        # Dosyanın tam yolunu oluştur
        png_path = os.path.join(input_folder, filename)
        
        # Görseli aç ve RGB moduna çevir (JPEG için gereklidir)
        img = Image.open(png_path).convert("RGB")
        
        # Yeni dosya adı oluştur (png uzantısını çıkar, jpeg ekle)
        jpeg_filename = os.path.splitext(filename)[0] + ".jpeg"
        jpeg_path = os.path.join(output_folder, jpeg_filename)
        
        # Görseli JPEG formatında kaydet
        img.save(jpeg_path, "JPEG", quality=95)
        
        print(f"{filename} dosyası JPEG formatına dönüştürüldü.")

print("Tüm PNG dosyaları başarıyla JPEG formatına dönüştürüldü.")