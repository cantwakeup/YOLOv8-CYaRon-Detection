import os
import sys

# =========================================================
# ✅ 1. 请将这里的文件路径替换为你想要修改的目录
#    这里使用你提供的路径作为示例
# =========================================================
TARGET_DIR = r'D:\Desktop\aqours\aqours_dataset\labels\val\Ruby'

def update_labels():
    """
    遍历指定目录下的所有.txt文件，将每一行的第一个字符从 '1' 改为 '2'。
    """
    if not os.path.isdir(TARGET_DIR):
        print(f"Error: Directory not found at {TARGET_DIR}")
        return

    print(f"Starting to update labels in: {TARGET_DIR}")
    print("-" * 50)

    try:
        # 遍历目录中的所有文件
        for filename in os.listdir(TARGET_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(TARGET_DIR, filename)

                # 以读模式打开文件，读取所有内容
                with open(filepath, 'r') as f_in:
                    lines = f_in.readlines()
                
                updated_lines = []
                num_modified = 0
                
                # 遍历每一行，进行修改
                for line in lines:
                    line = line.strip() # 去掉行首尾的空白
                    if line.startswith('1'):
                        # 将第一个字符 '1' 替换为 '2'
                        new_line = '2' + line[1:]
                        updated_lines.append(new_line + '\n')
                        num_modified += 1
                    else:
                        updated_lines.append(line + '\n')
                
                # 如果有内容被修改，就覆盖原始文件
                if num_modified > 0:
                    with open(filepath, 'w') as f_out:
                        f_out.writelines(updated_lines)
                    print(f"  - Modified {num_modified} lines in {filename}")
                else:
                    # 如果没有以 '0' 开头的行，也打印出来
                    print(f"  - No '1' labels found in {filename}, skipping.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The script was stopped to prevent data corruption.")

    print("-" * 50)
    print("Label update script finished.")

if __name__ == '__main__':
    update_labels()