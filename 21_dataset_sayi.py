import matplotlib.pyplot as plt

# Veri
classes = ['min 0', 'min 1','0+100 seti 0 ','0+100 seti 1 ','0_1 aug 0','0_1 aug 1']
counts = [227, 227,327,227,681,681]

# Grafik oluşturma
plt.figure(figsize=(8, 5))
bars = plt.bar(classes, counts, color=['blue', 'orange'])

# Başlık ve etiketler
plt.title('Train seti', fontsize=16)
plt.xlabel('Sınıf', fontsize=12)
plt.ylabel('Görsel Sayısı', fontsize=12)

# Her çubuğun üzerine sayıları yazdırma
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom', fontsize=12)

# Grafik gösterme
plt.show()