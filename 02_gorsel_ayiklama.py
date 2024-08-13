# train_label_0 klasöründe yer alan hem etiketli hem görselli klasördeki
#  dosyaları train_gorsel_0 veya train_gorsel_1  klasörüne sadece görselleri taşıma


import os
import shutil

# Kaynak klasör (hem PNG hem TXT dosyalarının bulunduğu klasör)
source_folder = r"C:\Users\ceren\Desktop\etiket_görsel_ayri dataset\images+labels\train_1"

# Hedef klasör (PNG dosyalarının kopyalanacağı klasör)
target_folder = r"C:\Users\ceren\Desktop\etiket_görsel_ayri dataset\images\train_1"

# Hedef klasörün var olduğundan emin olun
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Kaynak klasördeki tüm .png dosyalarını tara ve kopyala
for filename in os.listdir(source_folder):
    if filename.endswith('.png'):
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)
        shutil.copy2(source_path, target_path)
        print(f"{filename} kopyalandı.")

print("İşlem tamamlandı.")