import os
import matplotlib.pyplot as plt

# Klasör yolları
folders = {
    "Train": [r"C:\Users\ceren\Desktop\lower_1_class_dataset\images\train"],
    "Test": [r"C:\Users\ceren\Desktop\lower_1_class_dataset\images\train"],
    "Validation": [r"C:\Users\ceren\Desktop\lower_1_class_dataset\images\train"]
}

# Her set için görsel sayılarını tutmak için bir sözlük
image_counts = {
    "Train": [0],
    "Test": [0],
    "Validation": [0]
}

# Görsel sayılarını hesapla
for set_name, set_paths in folders.items():
    for i, folder in enumerate(set_paths):
        image_counts[set_name][i] = len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

# Grafikleri çizdir
for set_name, counts in image_counts.items():
    plt.figure(figsize=(6, 4))
    bars = plt.bar(["Class 0", "Class 1"], counts, color=['blue', 'orange'])
    plt.title(f'{set_name} Setindeki Görsel Sayıları')
    plt.xlabel('Sınıf')
    plt.ylabel('Görsel Sayısı')

    # Her bar'ın üzerine görsel sayısını yazdır
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), 
                 ha='center', va='bottom', fontsize=12, color='black')

    plt.show()