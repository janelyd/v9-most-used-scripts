# train_label_0 ve train_label_1 klasörlerine ayırma

import os # os ile etkileşim kurmak için,dosya ve dizin işlemleri
import shutil # yüksek seviyeli dosya işlemleri için(kopyalama,taşıma,silme)


#2 ayrı klasöre ayıracağımız kaynak klasör
label_path_source = r"C:\Users\ceren\Desktop\YOLODataset\YOLODataset\labels\test"


# oluşturalacak 2 hedef klasör
test_label_0 = r"C:\Users\ceren\Desktop\yolodataset2\labels\test_0"
test_label_1 = r"C:\Users\ceren\Desktop\yolodataset2\labels\test_1"



# hedef klasörler yok ise oluştur
os.makedirs(test_label_0, exist_ok=True)
os.makedirs(test_label_1, exist_ok=True)



# kaynak klasördeki tüm .txt dosyalarını tara
# belirtilen klasördeki dosya isimlerini liste olarak döndürür
for filename in os.listdir(label_path_source): 

    if filename.endswith('.txt'):
        # dosya txt ile bitiyosa, dosyanın tam path oluştur:
        file_path = os.path.join(label_path_source,filename)

        # dosya txt ile bitti ve txt dosyasının full path'i = file_path oldu:
        
        # file_path'in ilk karakterini oku
        with open(file_path, 'r') as file: # r read modu
            # okunan ilk karakter, first_char değişkenine atandı
            first_char = file.read(1) # 1, sadece 1 karakter okunacagını belirt


            # with: okuma bittikten sonra işlemi kapatıyor
            


        # ilk karaktere göre dosyayı uygun klasöre taşı
        if first_char == '0':
            shutil.move(file_path, os.path.join(test_label_0,filename))
        elif first_char == '1':
            shutil.move(file_path, os.path.join(test_label_1,filename))


print("succesed splitting")



















