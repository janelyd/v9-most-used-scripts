import os
import shutil

# Kaynak klasör yolu
kaynak_klasor = r"C:\Users\ceren\Desktop\EVSTEK\hormondataset\00_labels_splitted\train_label_0"

# Hedef klasör yolu
hedef_klasor = r"C:\Users\ceren\Desktop\EVSTEK\hormondataset\00_labels_splitted\train_label_000"

# Hedef klasörü oluştur (eğer yoksa)
if not os.path.exists(hedef_klasor):
    os.makedirs(hedef_klasor)

# Kaynak klasördeki tüm dosyaları döngüyle kontrol et
for dosya_adi in os.listdir(kaynak_klasor):
    # Sadece .txt uzantılı dosyaları işle
    if dosya_adi.endswith(".txt"):
        kaynak_dosya = os.path.join(kaynak_klasor, dosya_adi)
        hedef_dosya = os.path.join(hedef_klasor, dosya_adi)
        
        # Dosyayı kopyala
        shutil.copy2(kaynak_dosya, hedef_dosya)
        print(f"{dosya_adi} kopyalandı.")

print("İşlem tamamlandı.")