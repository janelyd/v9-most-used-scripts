import os

def count_total_lines_in_folder(folder_path):
    """Bir klasördeki tüm .txt dosyalarındaki toplam satır sayısını hesaplar."""
    total_lines = 0

    # Klasördeki tüm dosyalar arasında dolaş
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Sadece .txt dosyalarını dikkate al
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_lines += len(lines)

    return total_lines

# Kullanım
folder = r"C:\Users\ceren\Desktop\yarenemirhan\30_0_100_lr_cls\labels"
total_lines = count_total_lines_in_folder(folder)

print(f"Klasördeki toplam satır sayısı: {total_lines}")