#!/usr/bin/env python3
"""
Photo2Pixel Quick Start Script
照片转像素画快速启动脚本
"""

import os
import sys
import subprocess
import argparse

def check_venv():
    """Check and setup virtual environment"""
    if not os.path.exists(".venv"):
        print("❌ Virtual environment not found. Creating...")
        print("❌ 虚拟环境未找到，正在创建...")
        
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print("✅ Virtual environment created")
            print("✅ 虚拟环境已创建")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            print("❌ 创建虚拟环境失败")
            return False
    
    return True

def install_dependencies():
    """Install dependencies if needed"""
    try:
        # Check if requirements.txt exists
        if os.path.exists("requirements.txt"):
            print("📦 Installing dependencies...")
            print("📦 正在安装依赖...")
            
            # Use the virtual environment's pip
            pip_cmd = os.path.join(".venv", "bin", "pip")
            if os.name == "nt":  # Windows
                pip_cmd = os.path.join(".venv", "Scripts", "pip.exe")
            
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed")
            print("✅ 依赖已安装")
        else:
            print("⚠️  requirements.txt not found, skipping dependency installation")
            print("⚠️  未找到 requirements.txt，跳过依赖安装")
            
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("❌ 安装依赖失败")
        return False
    
    return True

def run_photo2pixel(mode="interactive", **kwargs):
    """Run Photo2Pixel with specified mode"""
    python_cmd = os.path.join(".venv", "bin", "python")
    if os.name == "nt":  # Windows
        python_cmd = os.path.join(".venv", "Scripts", "python.exe")
    
    cmd = [python_cmd, "convert.py"]
    
    if mode == "interactive":
        cmd.append("--interactive")
    elif mode == "preset":
        cmd.extend(["--preset", kwargs.get("preset", "classic")])
        if kwargs.get("input"):
            cmd.extend(["--input", kwargs.get("input")])
        if kwargs.get("output"):
            cmd.extend(["--output", kwargs.get("output")])
    elif mode == "custom":
        if kwargs.get("input"):
            cmd.extend(["--input", kwargs.get("input")])
        if kwargs.get("output"):
            cmd.extend(["--output", kwargs.get("output")])
        if kwargs.get("kernel_size"):
            cmd.extend(["-k", str(kwargs.get("kernel_size"))])
        if kwargs.get("pixel_size"):
            cmd.extend(["-p", str(kwargs.get("pixel_size"))])
        if kwargs.get("edge_thresh"):
            cmd.extend(["-e", str(kwargs.get("edge_thresh"))])
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run Photo2Pixel: {e}")
        print(f"❌ 运行 Photo2Pixel 失败: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="🎨 Photo2Pixel Quick Start / 照片转像素画快速启动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / 使用示例:
  python start.py                    # Interactive mode / 交互模式
  python start.py --preset retro     # Use retro preset / 使用复古预设
  python start.py --help             # Show this help / 显示帮助
        """
    )
    
    parser.add_argument("--mode", choices=["interactive", "preset", "custom"], 
                       default="interactive",
                       help="Run mode / 运行模式 (default: interactive / 默认: 交互模式)")
    
    # Preset mode arguments
    parser.add_argument("--preset", choices=["retro", "smooth", "sharp", "classic"],
                       help="Preset to use / 使用的预设")
    parser.add_argument("--input", type=str,
                       help="Input image path / 输入图片路径")
    parser.add_argument("--output", type=str,
                       help="Output image path / 输出图片路径")
    
    # Custom mode arguments
    parser.add_argument("-k", "--kernel_size", type=int,
                       help="Kernel size / 核大小")
    parser.add_argument("-p", "--pixel_size", type=int,
                       help="Pixel size / 像素大小")
    parser.add_argument("-e", "--edge_thresh", type=int,
                       help="Edge threshold / 边缘阈值")
    
    args = parser.parse_args()
    
    print("🎨 Photo2Pixel Quick Start")
    print("🎨 照片转像素画快速启动")
    print("=" * 40)
    
    # Check and setup environment
    if not check_venv():
        return 1
    
    if not install_dependencies():
        return 1
    
    # Determine mode
    if args.preset:
        mode = "preset"
        kwargs = {"preset": args.preset, "input": args.input, "output": args.output}
    elif args.input or args.kernel_size or args.pixel_size or args.edge_thresh:
        mode = "custom"
        kwargs = {
            "input": args.input,
            "output": args.output,
            "kernel_size": args.kernel_size,
            "pixel_size": args.pixel_size,
            "edge_thresh": args.edge_thresh
        }
    else:
        mode = "interactive"
        kwargs = {}
    
    print(f"🚀 Starting Photo2Pixel in {mode} mode...")
    print(f"🚀 正在以 {mode} 模式启动 Photo2Pixel...")
    
    if mode == "interactive":
        print("💡 You can drag and drop images directly!")
        print("💡 你可以直接拖拽图片！")
    
    return 0 if run_photo2pixel(mode, **kwargs) else 1

if __name__ == "__main__":
    sys.exit(main())
