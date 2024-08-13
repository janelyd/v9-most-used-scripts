# 1 sınıfına ait görsellerin sol orta köşesine 1 yazma

import cv2
import os
import shutil


# üstüne 0 yazağım gorsel setinin yolu
# kaynak 
source_path = 'C:/Users/ceren/Desktop/hormondataset/01_labela_gore_gorsel_split/test_folder_1'


# yazılacak rakam
number = "1"

# klasördeki tüm png dosyaları listele
for filename in os.listdir(source_path):
    # görsel dosyasının tam yolu
    image_path = os.path.join(source_path,filename)

    # görseli oku
    image = cv2.imread(image_path)

    # görsel boyutlarını al
    height, width = image.shape[:2]

    # yazı özellikleri
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = min(width,height) / 200.0 # görsel boyutuna göre otomatik ayarla
    color = (255,255,255) # beyaz
    thickness = max(int(min(width,height)/250), 1 )

    # yazı konumu
    text_x = 10
    text_y = 30

    # rakam ekle
    cv2.putText(image, number,(text_x,text_y), font, font_scale,color,thickness)

    # değiştirilen görseli kaydet
    cv2.imwrite(image_path,image)
    print(f"{filename} işlendi.")

print("successed all pics")





























