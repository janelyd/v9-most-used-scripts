# train_label_ ve 1 e göre eşleşen txt ile uygun klasöre resimi koy
# işlem sonucunda aynı klasörde txt ve png dosaları aynı klasör içinde olucak

import os
import shutil

# Kaynak klasör (resimler)
source_folder = r"C:\Users\ceren\Desktop\YOLODataset\YOLODataset\images\test"

# Hedef klasörler (etiketler)
target_folder_0 = r"C:\Users\ceren\Desktop\yolodataset2\images+labels\test_0"
target_folder_1 = r"C:\Users\ceren\Desktop\yolodataset2\images+labels\test_1"



# Kaynak klasördeki tüm .png dosyalarını tara
for filename in os.listdir(source_folder):
    if filename.endswith('.png'):
        image_path = os.path.join(source_folder, filename)
        base_name = os.path.splitext(filename)[0]  # Uzantısız dosya adı

        # label_0 klasöründe eşleşen .txt dosyası var mı kontrol et
        if os.path.exists(os.path.join(target_folder_0, base_name + '.txt')):
            # Resmi test_0 etiket klasörüne kopyala
            shutil.copy(image_path, os.path.join(target_folder_0, filename))

        # label_1 klasöründe eşleşen .txt dosyası var mı kontrol et
        elif os.path.exists(os.path.join(target_folder_1, base_name + '.txt')):
            # Resmi test_1  etiket klasörüne kopyala
            shutil.copy(image_path, os.path.join(target_folder_1, filename))

        else:
            print(f"Uyarı: {filename} için eşleşen etiket bulunamadı.")

print("İşlem tamamlandı.")