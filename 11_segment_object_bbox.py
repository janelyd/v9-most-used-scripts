# segmentasyon etiketlerini , object detectiona uygun olması için BBOX formatına çevirme


# segmentasyon etiketlerini bbox formatına çevirme ve kaydetme
import os

def convert_segmentation_to_yolo(segmentation_label):
    # Sınıf numarasını al
    class_id = segmentation_label.split()[0]
    
    # Koordinatları al ve float'a çevir
    coords = list(map(float, segmentation_label.split()[1:]))
    
    # X ve Y koordinatlarını ayır
    x_coords = coords[::2]
    y_coords = coords[1::2]
    
    # Sınırlayıcı kutuyu hesapla
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    # YOLO formatı için merkez koordinatları ve boyutları hesapla
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min
    
    # YOLO formatında etiketi oluştur
    yolo_label = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    
    return yolo_label

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            yolo_label = convert_segmentation_to_yolo(line.strip())
            outfile.write(yolo_label + '\n')

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            process_file(input_file, output_file)

# Kullanım örneği
input_directory = r"C:\Users\ceren\Desktop\labels_compare\grountruth_labels"
output_directory = r"C:\Users\ceren\Desktop\labels_compare\gt_object"
process_directory(input_directory, output_directory)