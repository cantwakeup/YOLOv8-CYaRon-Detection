from ultralytics import YOLO

def main():
    # ------------------- 关键升级 -------------------
    # 1. 升级模型：任务变复杂了，我们使用M模型以获得更好的区分能力。
    #    如果 yolov8m.pt 不存在，YOLO会自动尝试下载。
    #    如果下载失败，请像之前一样手动下载它。
    model = YOLO('yolov8m.pt')
    # ----------------------------------------------

    # 开始训练
    results = model.train(
        data='my.yaml',         # 确保指向你更新后的yaml文件
        epochs=200,             # 数据量和类别都增加了，我们给模型更长的学习时间
        patience=40,            # 耐心值也相应增加，给模型更多机会突破瓶颈
        imgsz=640,
        batch=32,               # 在单张A100上这个值很安全，可以根据需要调大
        device=0,
        cache=True,             # 数据量大了之后，开启缓存能极大加速训练
        workers=8,
        # --- 增强数据增强的强度 ---
        degrees=5.0,        # 随机旋转5度
        flipud=0.5,         # 50%概率上下翻转
        scale=0.8,          # 随机缩放80%
        perspective=0.0005, # 轻微的透视变换
        # 2. 为这次重要的多类别训练起一个新名字
        name='3_classes_yolov8m_run1'
    )

if __name__ == '__main__':
    main()