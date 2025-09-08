#!/usr/bin/env python3
"""
CUDNN问题诊断和修复脚本
"""
import os
import torch
import subprocess

def check_environment():
    """检查当前环境"""
    print("=== 环境检查 ===")
    print(f"Python: {os.sys.version}")
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"CUDNN version: {torch.backends.cudnn.version()}")
        print(f"GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

def test_cudnn():
    """测试CUDNN是否正常工作"""
    print("\n=== CUDNN测试 ===")
    try:
        # 创建简单的卷积操作测试CUDNN
        x = torch.randn(1, 3, 224, 224).cuda()
        conv = torch.nn.Conv2d(3, 64, 3, padding=1).cuda()
        
        # 测试前向传播
        with torch.no_grad():
            y = conv(x)
        print("✓ CUDNN前向传播测试通过")
        
        # 测试反向传播
        y.sum().backward()
        print("✓ CUDNN反向传播测试通过")
        
        return True
    except Exception as e:
        print(f"❌ CUDNN测试失败: {e}")
        return False

def fix_cudnn_env():
    """设置CUDNN环境变量"""
    print("\n=== 修复CUDNN环境 ===")
    
    # 禁用CUDNN的一些优化选项
    os.environ['CUDNN_DETERMINISTIC'] = '1'
    os.environ['CUDNN_BENCHMARK'] = '0'
    
    # 禁用CUDNN引擎预编译
    os.environ['TORCH_CUDNN_V8_API_DISABLED'] = '1'
    
    print("✓ 设置环境变量:")
    print("  CUDNN_DETERMINISTIC=1")
    print("  CUDNN_BENCHMARK=0") 
    print("  TORCH_CUDNN_V8_API_DISABLED=1")

def suggest_solutions():
    """建议解决方案"""
    print("\n=== 解决方案建议 ===")
    print("1. 环境变量方案（已应用）:")
    print("   export TORCH_CUDNN_V8_API_DISABLED=1")
    print("   export CUDNN_DETERMINISTIC=1")
    
    print("\n2. 重装PyTorch（推荐）:")
    print("   pip uninstall torch torchvision")
    print("   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121")
    
    print("\n3. 降级到CPU训练:")
    print("   在训练代码中设置 device='cpu'")
    
    print("\n4. 使用不同的CUDA版本:")
    print("   conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia")

if __name__ == "__main__":
    print("CUDNN问题诊断和修复工具")
    print("=" * 50)
    
    check_environment()
    fix_cudnn_env()
    
    # 重新测试
    if test_cudnn():
        print("\n🎉 CUDNN问题已解决！可以继续训练。")
    else:
        print("\n⚠️  CUDNN问题仍然存在，请尝试其他解决方案。")
        suggest_solutions()
