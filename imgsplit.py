import os
import shutil

# Kaynak klasör (resimler)
source_folder = '/home/ceren/Desktop/model_2/labels_sonuc_2/etiketelenen_test_2'

# Hedef klasörler (etiketler)
target_folder_0 = '/home/ceren/Desktop/model_2/labels_sonuc_2/test_0'
target_folder_1 = '/home/ceren/Desktop/model_2/labels_sonuc_2/test_1'

# Kaynak klasördeki tüm .png dosyalarını tara
for filename in os.listdir(source_folder):
    if filename.endswith('.png'):
        image_path = os.path.join(source_folder, filename)
        base_name = os.path.splitext(filename)[0]  # Uzantısız dosya adı

        # test_0 klasöründe eşleşen .txt dosyası var mı kontrol et
        if os.path.exists(os.path.join(target_folder_0, base_name + '.txt')):
            # Resmi test_0 klasörüne kopyala
            shutil.copy(image_path, os.path.join(target_folder_0, filename))

        # test_1 klasöründe eşleşen .txt dosyası var mı kontrol et
        elif os.path.exists(os.path.join(target_folder_1, base_name + '.txt')):
            # Resmi test_1 klasörüne kopyala
            shutil.copy(image_path, os.path.join(target_folder_1, filename))

        else:
            print(f"Uyarı: {filename} için eşleşen etiket bulunamadı.")

print("İşlem tamamlandı.")
