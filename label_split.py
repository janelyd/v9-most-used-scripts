import os
import shutil

# Kaynak klasör
source_folder = '/home/ceren/Desktop/hormondataset/YOLODataset/labels/train'

# Hedef klasörler
target_folder_0 = '/home/ceren/Desktop/hormondataset/YOLODataset/labels/test_0'
target_folder_1 = '/home/ceren/Desktop/hormondataset/YOLODataset/labels/test_1'

# Hedef klasörleri oluştur
os.makedirs(target_folder_0, exist_ok=True)
os.makedirs(target_folder_1, exist_ok=True)

# Kaynak klasördeki tüm .txt dosyalarını tara
for filename in os.listdir(source_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(source_folder, filename)

        # Dosyanın ilk karakterini oku
        with open(file_path, 'r') as file:
            first_char = file.read(1)

        # İlk karaktere göre dosyayı uygun klasöre taşı
        if first_char == '0':
            shutil.move(file_path, os.path.join(target_folder_0, filename))
        elif first_char == '1':
            shutil.move(file_path, os.path.join(target_folder_1, filename))

print("İşlem tamamlandı.")
