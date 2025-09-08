from ultralytics import YOLO

def main():
    # 🚀 使用预训练权重从头开始训练，充分利用扩展后的600张数据集
    model = YOLO('yolov8m.pt')  # 🔥 重新使用官方预训练权重
    
    # 开始训练
    results = model.train(
        data='my.yaml',       
        epochs=400,             # 🔥 数据集扩展，可以训练更多轮次
        patience=80,            # 🔥 增加patience，给模型更多学习时间
        imgsz=640,
        
        # --- 单GPU优化配置（600张数据集，GPU 0） ---
        device=0,                # 🔥 使用GPU 0进行训练
        batch=32,                # 🔥 单GPU适配的batch size
        workers=8,               # 🔥 适度CPU并行
        cache='ram',             # 🔥 600张图片全部缓存到内存
        
        # --- 训练策略优化 ---
        close_mosaic=20,        # 🔥 最后20轮关闭mosaic，提升精度
        amp=True,               # 🔥 重新启用AMP，环境已修复
        fraction=1.0,           # 使用全部数据
        
        # --- 600张数据集优化的数据增强策略 ---
        # 🎯 数据扩展后，可以适当增强以提升泛化能力
        degrees=15.0,           # 随机旋转±15度，适合动漫角色
        translate=0.15,         # 随机平移15%，模拟不同位置
        scale=0.8,              # 随机缩放80%-120%，模拟远近景
        shear=2.0,              # 随机剪切变换±2度，轻微视角变化
        perspective=0.001,      # 轻微的透视变换
        flipud=0.3,             # 🔥 降低上下翻转，动漫角色有方向性
        fliplr=0.5,             # 🔥 适度左右翻转
        mosaic=1.0,             # 🔥 保持最大Mosaic增强
        mixup=0.1,              # 10%概率MixUp增强
        copy_paste=0.1,         # 🔥 添加copy_paste，模拟复杂场景
        
        # --- 颜色增强：针对动漫数据 ---
        hsv_h=0.01,             # 轻微色调变化
        hsv_s=0.4,              # 饱和度调整
        hsv_v=0.3,              # 亮度变化，适应不同光照
        
        # --- 600张数据集学习率策略 ---
        lr0=0.01,               # 🔥 标准学习率，从头训练
        lrf=0.01,               # 最终学习率衰减
        momentum=0.937,         # 标准动量
        weight_decay=0.0005,    # 🔥 适度权重衰减防过拟合
        warmup_epochs=3.0,      # warmup轮数
        
        # --- 损失函数优化 ---
        box=7.5,                # box回归损失权重
        cls=0.5,                # 分类损失权重  
        dfl=1.5,                # distribution focal loss
        
        # --- 验证和保存策略 ---
        val=True,               
        save=True,              
        save_period=25,         # 每25轮保存一次
        plots=True,             
        
        # 600张数据集单GPU训练版本
        name='anime_600imgs_single_gpu_gpu1'
    )

if __name__ == '__main__':
    main()