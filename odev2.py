import cv2
import mediapipe as mp
import numpy as np
import RPi.GPIO as GPIO  # Raspberry Pi GPIO kütüphanesi
import time

# GPIO pinlerini ayarla
GPIO.setmode(GPIO.BCM)  # BCM numaralandırma sistemini kullan

# Motor sürücü pinleri (L298N motor sürücü için örnek)
# Sağa dönüş için pinler
RIGHT_PIN1 = 17  # GPIO pin numaralarını kendi kurulumunuza göre değiştirin
RIGHT_PIN2 = 27

# Sola dönüş için pinler
LEFT_PIN1 = 22
LEFT_PIN2 = 23

# Pinleri çıkış olarak tanımla
GPIO.setup(RIGHT_PIN1, GPIO.OUT)
GPIO.setup(RIGHT_PIN2, GPIO.OUT)
GPIO.setup(LEFT_PIN1, GPIO.OUT)
GPIO.setup(LEFT_PIN2, GPIO.OUT)

# Tüm pinleri başlangıçta LOW (kapalı) yap
GPIO.output(RIGHT_PIN1, GPIO.LOW)
GPIO.output(RIGHT_PIN2, GPIO.LOW)
GPIO.output(LEFT_PIN1, GPIO.LOW)
GPIO.output(LEFT_PIN2, GPIO.LOW)

# MediaPipe el modeli başlat
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # sadece 1 el takip edilecek
mp_draw = mp.solutions.drawing_utils  # landmark'ları çizmek için

# Webcam başlat
cap = cv2.VideoCapture(0)  # 0 = default webcam

try:
    while True:
        success, img = cap.read()
        if not success:
            break

        # Görüntüyü başta yatayda çevir (ayna görüntüsü)
        img = cv2.flip(img, 1)

        # Görüntünün boyutlarını al
        height, width, _ = img.shape
        
        # Görüntünün merkez noktasını bul
        center_x = width // 2
        center_y = height // 2
        
        # Ana dikdörtgenin köşe koordinatlarını hesapla
        # Merkez ± 50 piksel yatay, merkez ± 50 piksel dikey
        top_left = (center_x - 50, center_y - 50)
        bottom_right = (center_x + 50, center_y + 50)
        
        # Ana dikdörtgeni çiz
        cv2.rectangle(img, top_left, bottom_right, (66, 230, 245), 2)
        
        # El takibi kısmı 
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)  # el takibi yap

        # Varsayılan olarak tüm motor pinlerini kapat
        GPIO.output(RIGHT_PIN1, GPIO.LOW)
        GPIO.output(RIGHT_PIN2, GPIO.LOW)
        GPIO.output(LEFT_PIN1, GPIO.LOW)
        GPIO.output(LEFT_PIN2, GPIO.LOW)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # MediaPipe el landmark'larını çiz
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Bounding box oluşturmak için koordinatları belirle
                x_coords = []
                y_coords = []
                
                # Tüm landmark'ların koordinatlarını topla
                for landmark in hand_landmarks.landmark:
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    x_coords.append(cx)
                    y_coords.append(cy)
                
                # Minimum ve maksimum koordinatları bul
                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)
                
                # Bounding box'a biraz boşluk ekle
                padding = 20
                min_x = max(0, min_x - padding)
                min_y = max(0, min_y - padding)
                max_x = min(img.shape[1], max_x + padding)
                max_y = min(img.shape[0], max_y + padding)
                
                # Elin bounding box'ını çiz (yeşil renkte)
                cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
                
                # Elin bounding box'ının merkez noktasını hesapla
                hand_center_x = (min_x + max_x) // 2
                hand_center_y = (min_y + max_y) // 2
                
                # Elin merkez noktasını göster 
                cv2.circle(img, (hand_center_x, hand_center_y), 5, (254,243,74), -1)
                
                # Elin merkez noktası ana dikdörtgenin içinde mi kontrol et
                if (top_left[0] <= hand_center_x <= bottom_right[0] and 
                    top_left[1] <= hand_center_y <= bottom_right[1]):
                    print("El İÇERDE - Hedefe ulaşıldı")
                    # Hedefte olduğunda motorları durdur
                    GPIO.output(RIGHT_PIN1, GPIO.LOW)
                    GPIO.output(RIGHT_PIN2, GPIO.LOW)
                    GPIO.output(LEFT_PIN1, GPIO.LOW)
                    GPIO.output(LEFT_PIN2, GPIO.LOW)
                else:
                    # Elin hedef kutuya göre dışarıda kaldığı mesafeyi hesapla
                    dx = 0
                    dy = 0
                    
                    # X koordinatı: Eğer elin merkezi kutunun solundaysa, sağa hareket etmeli
                    if hand_center_x < top_left[0]:
                        dx = top_left[0] - hand_center_x  # Sağa gitmesi gereken piksel
                        # SAĞA dönüş pinlerini aktif et
                        GPIO.output(RIGHT_PIN1, GPIO.HIGH)
                        GPIO.output(RIGHT_PIN2, GPIO.HIGH)
                        print(f"El DIŞARDA: {abs(dx)} piksel SAĞA git")
                    # X koordinatı: Eğer elin merkezi kutunun sağındaysa, sola hareket etmeli
                    elif hand_center_x > bottom_right[0]:
                        dx = bottom_right[0] - hand_center_x  # Sola gitmesi gereken piksel (negatif değer)
                        # SOLA dönüş pinlerini aktif et
                        GPIO.output(LEFT_PIN1, GPIO.HIGH)
                        GPIO.output(LEFT_PIN2, GPIO.HIGH)
                        print(f"El DIŞARDA: {abs(dx)} piksel SOLA git")
                    
                    # Y koordinatı kontrolünü de ekleyebilirsiniz, ancak soruda sadece sağ/sol motor kontrolü istendiği için basit tutuyorum
                    if hand_center_y < top_left[1]:
                        dy = top_left[1] - hand_center_y
                        print(f"El DIŞARDA: {abs(dy)} piksel AŞAĞI git")
                    elif hand_center_y > bottom_right[1]:
                        dy = bottom_right[1] - hand_center_y
                        print(f"El DIŞARDA: {abs(dy)} piksel YUKARI git")

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program kullanıcı tarafından sonlandırıldı")
finally:
    # Program sonlandığında temizlik işlemleri
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()  # GPIO pinlerini temizle
