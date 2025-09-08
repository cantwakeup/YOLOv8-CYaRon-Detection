import os
import cv2
from tqdm import tqdm

# --- 配置区 ---
# 你的数据集根目录
DATASET_ROOT = 'aqours_datasets'
# 你想检查的文件夹 (比如 'train' 或 'val')
SPLIT_TO_CHECK = 'train'
# 保存可视化结果的文件夹
OUTPUT_DIR = 'label_check_visualization'

# 从你的 my.yaml 文件中获取类别名称
# ！！请确保这里的类别和你 .yaml 文件里完全一致！！
CLASS_NAMES = {
    0: 'character_a',
    1: 'character_b',
    2: 'character_c'
}
# -----------------

def visualize():
    images_base_dir = os.path.join(DATASET_ROOT, 'images', SPLIT_TO_CHECK)
    labels_base_dir = os.path.join(DATASET_ROOT, 'labels', SPLIT_TO_CHECK)
    output_base_dir = os.path.join(OUTPUT_DIR, SPLIT_TO_CHECK)

    if not os.path.isdir(images_base_dir):
        print(f"Error: Image directory not found at {images_base_dir}")
        return

    print(f"Starting visualization for '{SPLIT_TO_CHECK}' split...")

    image_files = []
    for root, _, files in os.walk(images_base_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))

    for image_path in tqdm(image_files, desc="Processing images"):
        # 构建对应的标签文件路径
        relative_path = os.path.relpath(image_path, images_base_dir)
        label_path = os.path.join(labels_base_dir, os.path.splitext(relative_path)[0] + '.txt')

        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not read image {image_path}")
            continue
        h, w, _ = image.shape

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    class_id = int(parts[0])
                    x_center = float(parts[1]) * w
                    y_center = float(parts[2]) * h
                    box_w = float(parts[3]) * w
                    box_h = float(parts[4]) * h

                    x1 = int(x_center - box_w / 2)
                    y1 = int(y_center - box_h / 2)
                    x2 = int(x_center + box_w / 2)
                    y2 = int(y_center + box_h / 2)

                    class_name = CLASS_NAMES.get(class_id, "UNKNOWN")
                    color = (0, 255, 0) # Green for known classes
                    if class_name == "UNKNOWN":
                        color = (0, 0, 255) # Red for unknown class IDs

                    # 画框和标签
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # 创建输出目录并保存图片
        output_image_path = os.path.join(output_base_dir, relative_path)
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        cv2.imwrite(output_image_path, image)

    print("\n" + "="*50)
    print("✅ Visualization complete!")
    print(f"Check the results in the '{output_base_dir}' folder.")
    print("="*50)

if __name__ == '__main__':
    visualize()