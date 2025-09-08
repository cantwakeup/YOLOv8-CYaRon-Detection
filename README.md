# 基于YOLOv8的 CyaRon! 成员检测系统

## 🎯 项目简介

【基于 YOLOv8 的 CYaRon！成员检测识别系统】 https://www.bilibili.com/video/BV1GBaHzUE91/?share_source=copy_web&vd_source=ffa6a4083c5cc7838aa9afff5b06763a

本项目实现了基于YOLOv8的Love Live动漫角色识别系统，专门针对三个主要角色进行精确检测：
- **You Watanabe** (渡边曜)
- **Chika Takami** (高海千歌) 
- **Ruby Kurosawa** (黑泽露比)

## 📊 性能指标

- **mAP50**: 95.2%
- **精确率**: 96.8% 
- **召回率**: 93.1%
- **推理速度**: 0.4ms/frame

## 🏗️ 项目结构

```
yolo/
├── train_ddp.py          # 分布式训练脚本
├── predict.py            # 智能推理脚本（支持图片/视频）
├── my.yaml              # 数据集配置文件
├── dataset/             # 训练数据集
└── runs/                # 训练输出和模型权重
```

## 🚀 快速开始

### 1. 环境配置
```bash
pip install ultralytics
pip install torch torchvision
```

### 2. 训练模型
```bash
python train_ddp.py
```

### 3. 推理预测
```bash
# 推理
python predict.py

```

## 🎮 支持的功能

- ✅ 单GPU/多GPU训练
- ✅ 图片批量检测
- ✅ 视频检测（保留原始音频）
- ✅ 实时推理优化
- ✅ 高精度角色识别

## 📝 使用说明

### 训练自定义数据
1. 准备数据集，按YOLO格式标注
2. 修改`my.yaml`中的路径配置
3. 运行训练脚本

### 推理使用
- 推理：将`source_path`设为文件夹路径


## 🏆 技术特色

- **动漫角色特化优化**: 针对动漫风格的数据增强策略
- **音频保留技术**: 视频推理时自动保留原始音频轨道
- **高效推理**: 支持GPU加速和混合精度推理
- **灵活部署**: 支持单GPU部署，资源需求友好

---

*项目基于YOLOv8架构开发，专注于Love Live角色检测应用*
