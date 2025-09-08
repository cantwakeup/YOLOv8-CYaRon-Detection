from ultralytics import YOLO

def main():
    # 1. 加载你训练好的模型
    model = YOLO('/home/huiwei/sy/yolo/runs/detect/3_classes_yolov8m_ddp_run2/weights/best.pt')

    # 2. 定义你要推理的视频文件路径
    # 请务必替换为你自己的视频文件路径！
    video_path = '/home/huiwei/sy/yolo/test_for_joy/test/Aquarium.mp4'

    # 3. 运行推理，并指定参数
    #   'device' 参数指定要使用的GPU设备，例如 '0,1' 或 '0,1,2,3'
    #   YOLO会自动将视频的每一帧分配到这些GPU上进行处理
    results = model(
        source=video_path,
        save=True,
        conf=0.7,
        iou=0.4,
        
        # --- 关键修改在这里 ---
        # 启用多GPU并行推理
        device=[0, 1, 2, 3] # 指定使用设备0, 1, 2, 3
    )

    print("视频推理完成！")

if __name__ == '__main__':
    main()