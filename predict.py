from ultralytics import YOLO
import os
import subprocess

def predict_with_audio(source_path, model_path, output_dir, output_name):
    """
    YOLO推理并保留音频的函数
    """
    # 1. 加载模型
    model = YOLO(model_path)
    
    # 2. 检查输入是视频还是图片文件夹
    is_video = source_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'))
    
    if is_video:
        print(f"🎬 检测到视频文件: {source_path}")
        
        # 3. YOLO推理（会生成无音频的视频）
        print("📊 正在进行YOLO推理...")
        results = model(
            source=source_path,
            save=True,
            project=output_dir,
            name=output_name,
            exist_ok=True,
            conf=0.6,
            max_det=3
        )
        
        # 4. 获取YOLO输出的无音频视频路径
        if results and hasattr(results[0], 'save_dir'):
            yolo_output_dir = results[0].save_dir
            # 找到输出视频文件
            video_files = [f for f in os.listdir(yolo_output_dir) if f.lower().endswith(('.mp4', '.avi'))]
            if video_files:
                yolo_video_path = os.path.join(yolo_output_dir, video_files[0])
                
                # 5. 使用ffmpeg合并音频
                print("🔊 正在添加原始音频...")
                final_output_path = os.path.join(yolo_output_dir, f"final_with_audio_{video_files[0]}")
                
                # ffmpeg命令：合并视频和音频
                ffmpeg_cmd = [
                    'ffmpeg', '-y',                    # -y 覆盖输出文件
                    '-i', yolo_video_path,             # 输入视频（YOLO处理后的）
                    '-i', source_path,                 # 输入音频（原始视频）
                    '-c:v', 'copy',                    # 复制视频流，不重新编码
                    '-c:a', 'aac',                     # 音频编码为aac
                    '-map', '0:v:0',                   # 使用第一个输入的视频流
                    '-map', '1:a:0',                   # 使用第二个输入的音频流
                    '-shortest',                       # 以最短流为准
                    final_output_path
                ]
                
                try:
                    subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
                    print(f"✅ 视频处理完成！带音频版本保存为: {final_output_path}")
                    
                    # 可选：删除无音频版本
                    # os.remove(yolo_video_path)
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ 音频合并失败: {e}")
                    print("📝 原始YOLO输出（无音频）仍可用")
                except FileNotFoundError:
                    print("❌ 未找到ffmpeg，请安装: sudo apt install ffmpeg")
                    print("📝 原始YOLO输出（无音频）仍可用")
        
    else:
        print(f"📁 检测到图片文件夹: {source_path}")
        # 对于图片，直接使用YOLO推理
        results = model(
            source=source_path,
            save=True,
            project=output_dir,
            name=output_name,
            exist_ok=True,
            conf=0.4,
            iou=0.4,
            max_det=3
        )
    
    return results

# 主程序
if __name__ == "__main__":
    # 1. 模型路径
    model_path = '/home/huiwei/sy/yolo/runs/detect/anime_600imgs_single_gpu_gpu1/weights/best.pt'
    
    # 2. 输入路径（可以是视频文件或图片文件夹）
    # 视频示例: '/path/to/your/video.mp4'
    # 图片文件夹示例: '/home/huiwei/sy/yolo/test_for_joy/test'
    source_path = '/home/huiwei/sy/yolo/test_for_joy/test'  # 请根据需要修改
    
    # 3. 输出设置
    output_project_path = '/home/huiwei/sy/yolo/test_for_joy'
    output_folder_name = 'predict'
    
    # 4. 执行推理
    results = predict_with_audio(source_path, model_path, output_project_path, output_folder_name)
    
    # 打印结果
    print("-" * 50)
    print(f"✅ Prediction complete.")
    if results and hasattr(results[0], 'save_dir'):
        print(f"Results saved to: {results[0].save_dir}")
    print("-" * 50)