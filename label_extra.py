import os
import matplotlib.pyplot as plt
from collections import defaultdict

# Klasör yolları
real_labels_path = '/home/ceren/Desktop/label_karşılaştırma/0_label_gercek'

# Sonuçları saklamak için sözlükler
results = defaultdict(lambda: {'real': None, 'detected': None, 'extra': False})
stats = {'correct': 0, 'incorrect': 0, 'missed': 0, 'extra': 0}
extra_files = []  # Fazladan sınıf içeren dosyaları saklamak için liste
incorrect_files = []  # Yanlış tespit edilen dosyaları saklamak için liste
missed_files = []  # Tespit edilemeyen dosyaları saklamak için liste



def check_extra_detections(content):
    # Dosya içeriğinde birden fazla sınıf var mı kontrol et
    lines = content.strip().split('\n')
    classes = set()
    for line in lines:
        parts = line.split()
        if parts:
            classes.add(parts[0])
    return len(classes) > 1




# Gerçek etiketleri oku
for filename in os.listdir(real_labels_path):
    if filename.endswith('.txt'):
        with open(os.path.join(real_labels_path, filename), 'r') as f:
            content = f.read().strip()
            first_char = content.split()[0] if content else None
        if first_char in ['0', '1']:
            results[filename]['real'] = int(first_char)

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


print(f"Fazladan tespit edilen: {stats['extra']}")


# Fazladan sınıf içeren dosyaları listele
print("\nFazladan sınıf içeren dosyalar:")
for i, filename in enumerate(extra_files, 1):
    print(f"{i}) {filename.replace('.txt', '.png')}")
