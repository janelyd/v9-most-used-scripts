# 0 olan etiketleri 1 yapma
import os

# Etiket dosyalarının bulunduğu klasör yolu
folder_path = r"D:\download\DOWNLOAD\testarttiroo\train\labels"

# Klasördeki tüm .txt dosyalarını işle
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        # Dosyayı oku
        with open(file_path, 'r') as file:
            content = file.read()
        
        # İlk karakteri değiştir
        if content and content[0] == '0':
            modified_content = '1' + content[1:]
            
            # Değiştirilmiş içeriği dosyaya yaz
            with open(file_path, 'w') as file:
                file.write(modified_content)
        
        print(f"{filename} işlendi.")

print("Tüm dosyalar işlendi.")