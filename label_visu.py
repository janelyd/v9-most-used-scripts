import os
import matplotlib.pyplot as plt
from collections import defaultdict

# Klasör yolları
real_labels_path = '/home/ceren/Desktop/label_karşılaştırma/0_label_gercek'
detected_labels_path = '/home/ceren/Desktop/label_karşılaştırma/1_label_tespit'

# Sonuçları saklamak için sözlükler
results = defaultdict(lambda: {'real': None, 'detected': None, 'extra': False})
stats = {'correct': 0, 'incorrect': 0, 'missed': 0, 'extra': 0, 'total_test_data': 0}
extra_files = []
incorrect_files = []
missed_files = []

def check_extra_detections(content):
    lines = content.strip().split('\n')
    classes = set()
    for line in lines:
        parts = line.split()
        if parts:
            classes.add(parts[0])
    return len(classes) > 1

# Gerçek etiketleri oku ve toplam test veri sayısını hesapla
for filename in os.listdir(real_labels_path):
    if filename.endswith('.txt'):
        stats['total_test_data'] += 1
        with open(os.path.join(real_labels_path, filename), 'r') as f:
            content = f.read().strip()
            first_char = content.split()[0] if content else None
        if first_char in ['0', '1']:
            results[filename]['real'] = int(first_char)

# Tespit edilen etiketleri oku
for filename in os.listdir(detected_labels_path):
    if filename.endswith('.txt'):
        with open(os.path.join(detected_labels_path, filename), 'r') as f:
            content = f.read().strip()
            first_char = content.split()[0] if content else None
        if first_char in ['0', '1']:
            results[filename]['detected'] = int(first_char)
        results[filename]['extra'] = check_extra_detections(content)
        if results[filename]['extra']:
            extra_files.append(filename)

# Sonuçları analiz et
for filename, data in results.items():
    if data['real'] is not None and data['detected'] is not None:
        if data['real'] == data['detected'] and not data['extra']:
            stats['correct'] += 1
        else:
            stats['incorrect'] += 1
            incorrect_files.append(filename)
    elif data['real'] is not None:
        stats['missed'] += 1
        missed_files.append(filename)

    if data['extra']:
        stats['extra'] += 1

# Sonuçları yazdır
print(f"Toplam test verisi: {stats['total_test_data']}")
print(f"Doğru tespit edilen: {stats['correct']}")
print(f"Yanlış tespit edilen: {stats['incorrect']}")
print(f"Tespit edilemeyen: {stats['missed']}")
print(f"Fazladan tespit edilen: {stats['extra']}")

# Sonuçları görselleştir
categories = ['Toplam Test Görseli', 'Doğru tespit edilen görsel sayısı', 'Yanlış tespit edilen görsel sayısı ', 'Tespit Edilemeyen', 'Fazladan tespit bulunan görsel sayısı']
values = [stats['total_test_data'], stats['correct'], stats['incorrect'], stats['missed'], stats['extra']]
colors = ['#ffcc99', '#66b3ff', '#ff9999', '#99ff99', '#ff99cc']

plt.figure(figsize=(14, 6))
bars = plt.bar(categories, values, color=colors)

# Çubukların üzerine sayıları ekle
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

plt.title('YOLOv9 yanlış-eksik-fazla tespit sonuçları')
plt.ylabel('Sayı')
plt.ylim(0, max(values) * 1.1)  # Y eksenini en yüksek değerin %10 üzerine ayarla

plt.tight_layout()
plt.show()

# Yanlış tespit edilen dosyaları listele
print("\nYanlış tespit edilen dosyalar:")
for i, filename in enumerate(incorrect_files, 1):
    data = results[filename]
    print(f"{i}) {filename.replace('.txt', '.png')}: Gerçek: {data['real']}, Tespit: {data['detected']}, Fazladan: {'Evet' if data['extra'] else 'Hayır'}")

# Tespit edilemeyen dosyaları listele
print("\nTespit edilemeyen dosyalar:")
for i, filename in enumerate(missed_files, 1):
    print(f"{i}) {filename.replace('.txt', '.png')}")

# Fazladan sınıf içeren dosyaları listele
print("\nFazladan sınıf içeren dosyalar:")
for i, filename in enumerate(extra_files, 1):
    print(f"{i}) {filename.replace('.txt', '.png')}")
