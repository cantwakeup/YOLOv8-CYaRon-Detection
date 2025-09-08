import os
import sys

# --- 配置区 ---
# 你的数据集标签目录
# 请确保使用你实际的路径
LABELS_DIR = r'/home/huiwei/sy/yolo/dataset/labels/train'

# 你的类别名称字典，和你的my.yaml文件一致
CLASS_NAMES = {
    0: 'You_Watanabe',
    1: 'Chika_Takami',
    2: 'Ruby_Kurosawa'
}
# -----------------

def count_labels():
    if not os.path.isdir(LABELS_DIR):
        print(f"Error: Directory not found at {LABELS_DIR}")
        return

    print(f"Counting labels in: {LABELS_DIR}")
    
    label_counts = {class_id: 0 for class_id in CLASS_NAMES.keys()}
    total_labels = 0

    # 递归遍历所有标签文件，包括子文件夹
    for root, _, files in os.walk(LABELS_DIR):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        for line in f:
                            if line.strip(): # 确保行不为空
                                class_id = int(line.split()[0])
                                if class_id in label_counts:
                                    label_counts[class_id] += 1
                                    total_labels += 1
                                else:
                                    print(f"Warning: Unknown class ID {class_id} found in {filepath}")
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")
                    
    print("\n" + "="*50)
    print("Label Distribution Report")
    print("="*50)
    
    if total_labels > 0:
        for class_id, count in label_counts.items():
            class_name = CLASS_NAMES.get(class_id, "UNKNOWN")
            percentage = (count / total_labels) * 100
            print(f"- {class_name} (ID: {class_id}): {count} instances ({percentage:.2f}%)")
        print("-" * 50)
        print(f"Total instances found: {total_labels}")
    else:
        print("No labels found. Please check your LABELS_DIR path.")
        
    print("="*50)


if __name__ == '__main__':
    count_labels()