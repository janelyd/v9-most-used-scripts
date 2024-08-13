# Gerekli kütüphaneleri içe aktarıyoruz
import os  # Dosya ve klasör işlemleri için
import numpy as np  # Sayısal işlemler için

# Koordinatlardan bounding box oluşturan fonksiyon
def get_bounding_box(coordinates):
    # Koordinat sayısı tek ise son koordinatı tekrarlıyoruz
    # Çünkü koordinatlar (x,y) çiftleri halinde olmalı, tek sayıda koordinat olması bir hataya işaret eder
    if len(coordinates) % 2 != 0:
        coordinates.append(coordinates[-1])
    
    # Koordinatları (x,y) çiftleri halinde yeniden şekillendiriyoruz
    # Örneğin, [x1, y1, x2, y2, x3, y3] listesini [[x1, y1], [x2, y2], [x3, y3]] şekline dönüştürüyoruz
    # Bu, koordinatları daha kolay işlememizi sağlar
    coords = np.array(coordinates).reshape(-1, 2)
    
    # En küçük x ve y değerlerini buluyoruz
    # Bu, bounding box'un sol alt köşesini temsil eder
    min_x, min_y = coords.min(axis=0)
    
    # En büyük x ve y değerlerini buluyoruz
    # Bu, bounding box'un sağ üst köşesini temsil eder
    max_x, max_y = coords.max(axis=0)
    
    # Bounding box'u döndürüyoruz [min_x, min_y, max_x, max_y]
    # Bu format, bir dikdörtgeni tanımlamak için yaygın olarak kullanılır
    return [min_x, min_y, max_x, max_y]

# Etiket dosyasını işleyen fonksiyon
def process_label_file(file_path):
    # Dosyayı açıp içeriğini okuyoruz
    # 'r' modu, dosyayı okuma modunda açar
    with open(file_path, 'r') as f:
        content = f.read().strip().split()
    
    # İlk değeri sınıf ID'si olarak alıyoruz
    # Sınıf ID'si, genellikle nesnenin türünü temsil eder (örneğin, 0 = araba, 1 = insan)
    class_id = int(content[0])
    
    # Geri kalan değerleri koordinatlar olarak alıyoruz
    # Bu koordinatlar, nesnenin konumunu belirtir
    coordinates = [float(coord) for coord in content[1:]]
    
    # Koordinatlardan bounding box oluşturuyoruz
    bounding_box = get_bounding_box(coordinates)
    
    # Sınıf ID'si ve bounding box'u döndürüyoruz
    return class_id, bounding_box

# Klasördeki tüm dosyaları işleyen fonksiyon
def process_folder(folder_path):
    results = {}
    # Klasördeki her dosya için
    for filename in os.listdir(folder_path):
        # Eğer dosya .txt uzantılı ise
        if filename.endswith('.txt'):
            # Dosyanın tam yolunu oluşturuyoruz
            file_path = os.path.join(folder_path, filename)
            try:
                # Dosyayı işliyoruz
                # "Dosyayı işlemek", dosyanın içeriğini okuyup, sınıf ID'si ve bounding box bilgilerini çıkarmak anlamına gelir
                # Bu işlem, yukarıda tanımladığımız process_label_file fonksiyonu tarafından yapılır
                class_id, bounding_box = process_label_file(file_path)
                
                # Sonuçları dictionary'e ekliyoruz
                # Her dosya adı için, ilgili sınıf ID'si ve bounding box bilgilerini saklıyoruz
                results[filename] = (class_id, bounding_box)
            except Exception as e:
                # Hata durumunda hata mesajını yazdırıyoruz
                print(f"Error processing file {filename}: {str(e)}")
    # Tüm sonuçları döndürüyoruz
    return results

# İki bounding box arasındaki IoU'yu hesaplayan fonksiyon
def calculate_iou(box1, box2):
    # Her iki kutunun köşe koordinatlarını alıyoruz
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    
    # Kesişim alanının köşe koordinatlarını hesaplıyoruz
    # İki dikdörtgenin kesişim alanının sol üst köşesi, her iki dikdörtgenin sol üst köşelerinin maksimumudur
    x_left = max(x1, x3)
    y_top = max(y1, y3)
    # İki dikdörtgenin kesişim alanının sağ alt köşesi, her iki dikdörtgenin sağ alt köşelerinin minimumudur
    x_right = min(x2, x4)
    y_bottom = min(y2, y4)
    
    # Eğer kesişim yoksa 0 döndürüyoruz
    # Kesişim olmaması durumu, bir dikdörtgenin tamamen diğerinin dışında olması demektir
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    # Kesişim alanını hesaplıyoruz
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Her iki kutunun alanını hesaplıyoruz
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x4 - x3) * (y4 - y3)
    
    # IoU'yu hesaplayıp döndürüyoruz
    # IoU = Kesişim Alanı / Birleşim Alanı
    # Birleşim Alanı = Box1 Alanı + Box2 Alanı - Kesişim Alanı
    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

# Metrikleri hesaplayan fonksiyon
def calculate_metrics(gt_results, pred_results, iou_threshold=0.7):
    # Her sınıf için metrikleri tutacak dictionary
    # tp: True Positive, fp: False Positive, fn: False Negative
    metrics = {0: {"tp": 0, "fp": 0, "fn": 0}, 1: {"tp": 0, "fp": 0, "fn": 0}}
    
    # Her ground truth dosyası için
    for filename in gt_results:
        gt_class, gt_box = gt_results[filename]
        
        # Eğer bu dosya tahminlerde de varsa
        if filename in pred_results:
            pred_class, pred_box = pred_results[filename]
            # IoU'yu hesaplıyoruz
            iou = calculate_iou(gt_box, pred_box)
            
            # Eğer IoU eşik değerinden büyükse ve sınıflar aynıysa
            if iou >= iou_threshold and gt_class == pred_class:
                metrics[gt_class]["tp"] += 1  # True Positive
            else:
                metrics[gt_class]["fn"] += 1  # False Negative
                metrics[pred_class]["fp"] += 1  # False Positive
        else:
            metrics[gt_class]["fn"] += 1  # False Negative

    # Tahminlerde olup ground truth'ta olmayan dosyalar için
    for filename in pred_results:
        if filename not in gt_results:
            pred_class, _ = pred_results[filename]
            metrics[pred_class]["fp"] += 1  # False Positive

    return metrics

# Ana işlem
# Ground truth ve tahmin klasörlerinin yollarını belirliyoruz
gt_folder = r"D:\download\DOWNLOAD\testarttiroo\train\groundtruth"
pred_folder = r"D:\download\DOWNLOAD\labelasasasas\labels"

# Her iki klasörü işliyoruz
gt_results = process_folder(gt_folder)
pred_results = process_folder(pred_folder)

# Metrikleri hesaplıyoruz
metrics = calculate_metrics(gt_results, pred_results)

# Her sınıf için metrikleri yazdırıyoruz
for class_id in [0, 1]:
    tp = metrics[class_id]["tp"]
    fp = metrics[class_id]["fp"]
    fn = metrics[class_id]["fn"]

    print(f"\nMetrics for Class {class_id}:")
    print(f"True Positives: {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")

    # Precision, Recall ve F1-score hesaplama
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1_score:.4f}")

# Genel (macro-average) F1 skoru hesaplama
f1_scores = []
for class_id in [0, 1]:
    tp = metrics[class_id]["tp"]
    fp = metrics[class_id]["fp"]
    fn = metrics[class_id]["fn"]
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    f1_scores.append(f1)

# Macro-average F1 skorunu hesaplayıp yazdırıyoruz
macro_f1 = sum(f1_scores) / len(f1_scores)
print(f"\nMacro-average F1 score: {macro_f1:.4f}")