import torch
from PIL import Image
import argparse
import os
import sys
from pathlib import Path
import re

from models.module_photo2pixel import Photo2PixelModel
from utils import img_common_util


def print_banner():
    """Print program banner"""
    print("=" * 60)
    print("🎨 Photo2Pixel - Photo to Pixel Art Converter")
    print("🎨 Photo2Pixel - 照片转像素画转换器")
    print("=" * 60)
    print("Convert your photos into beautiful pixel art!")
    print("将您的照片转换为精美的像素画！")
    print("Online demo: https://photo2pixel.co")
    print("在线演示: https://photo2pixel.co")
    print("=" * 60)


def print_presets():
    """Print available presets"""
    presets = {
        "retro": {"kernel_size": 8, "pixel_size": 12, "edge_thresh": 80, "desc": "Retro pixel art style", "desc_cn": "复古像素画风格"},
        "smooth": {"kernel_size": 16, "pixel_size": 20, "edge_thresh": 120, "desc": "Smooth color transitions", "desc_cn": "平滑颜色过渡"},
        "sharp": {"kernel_size": 6, "pixel_size": 8, "edge_thresh": 60, "desc": "Sharp pixel art with strong edges", "desc_cn": "锐利边缘像素画"},
        "classic": {"kernel_size": 10, "pixel_size": 16, "edge_thresh": 100, "desc": "Classic 8-bit style", "desc_cn": "经典8位风格"}
    }
    
    print("\n📋 Available Presets / 可用预设:")
    for name, config in presets.items():
        print(f"  {name:8} - {config['desc']}")
        print(f"           {config['desc_cn']}")
        print(f"           kernel_size: {config['kernel_size']}, pixel_size: {config['pixel_size']}, edge_thresh: {config['edge_thresh']}")
    print()


def get_preset_config(preset_name):
    """Get configuration for a preset"""
    presets = {
        "retro": {"kernel_size": 8, "pixel_size": 12, "edge_thresh": 80},
        "smooth": {"kernel_size": 16, "pixel_size": 20, "edge_thresh": 120},
        "sharp": {"kernel_size": 6, "pixel_size": 8, "edge_thresh": 60},
        "classic": {"kernel_size": 10, "pixel_size": 16, "edge_thresh": 100}
    }
    return presets.get(preset_name, {})


def clean_dragged_path(path):
    """Clean dragged file path from quotes and spaces"""
    # Remove extra spaces first
    cleaned = path.strip()
    
    # Handle macOS drag and drop format with quotes
    # Remove outer quotes if they exist
    if (cleaned.startswith('"') and cleaned.endswith('"')) or \
       (cleaned.startswith("'") and cleaned.endswith("'")):
        cleaned = cleaned[1:-1]
    
    # Remove any remaining quotes and spaces
    cleaned = cleaned.strip().strip('"').strip("'")
    
    # Handle escaped spaces in macOS paths
    cleaned = cleaned.replace('\\ ', ' ')
    
    return cleaned

def is_image_file(file_path):
    """Check if file is a supported image format"""
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    return Path(file_path).suffix.lower() in supported_extensions

def interactive_input():
    """Interactive parameter input"""
    print("\n🔧 Interactive Configuration / 交互式配置")
    print("-" * 30)
    
    # Input file
    while True:
        input_path = input("📁 Input image path / 输入图片路径 (or drag image here / 或拖拽图片到这里): ").strip()
        if not input_path:
            input_path = "./images/example_input_mountain.jpg"
        
        # Clean dragged path
        input_path = clean_dragged_path(input_path)
        
        if os.path.exists(input_path):
            if is_image_file(input_path):
                print(f"✅ Found image file / 找到图片文件: {input_path}")
                break
            else:
                print(f"❌ Not a supported image format / 不是支持的图片格式: {input_path}")
                print("💡 Supported formats / 支持的格式: jpg, jpeg, png, bmp, tiff, tif")
        else:
            print(f"❌ File not found / 文件未找到: {input_path}")
            print("💡 Please enter a valid image file path or drag an image / 请输入有效的图片文件路径或拖拽图片")
    
    # Output file
    output_path = input("💾 Output image path / 输出图片路径 (or press Enter for auto / 或按回车自动生成): ").strip()
    if not output_path:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_pixel.png"
    
    # Preset selection
    print_presets()
    preset = input("🎨 Choose preset / 选择预设 (retro/smooth/sharp/classic) or press Enter for custom / 或按回车自定义: ").strip().lower()
    
    if preset in ["retro", "smooth", "sharp", "classic"]:
        config = get_preset_config(preset)
        print(f"✅ Using '{preset}' preset / 使用 '{preset}' 预设")
        return input_path, output_path, config
    
    # Custom parameters
    print("\n⚙️  Custom Parameters / 自定义参数:")
    print("💡 Kernel Size: Controls color smoothness (1-50, higher = smoother)")
    print("💡 核大小: 控制颜色平滑度 (1-50, 数值越大越平滑)")
    kernel_size = int(input("   Kernel Size / 核大小 (default 10 / 默认 10): ") or "10")
    
    print("💡 Pixel Size: Controls pixel block size (1-64, higher = larger pixels)")
    print("💡 像素大小: 控制像素块大小 (1-64, 数值越大像素块越大)")
    pixel_size = int(input("   Pixel Size / 像素大小 (default 16 / 默认 16): ") or "16")
    
    print("💡 Edge Threshold: Controls black line intensity (0-255, lower = more lines)")
    print("💡 边缘阈值: 控制黑线强度 (0-255, 数值越小黑线越多)")
    edge_thresh = int(input("   Edge Threshold / 边缘阈值 (default 100 / 默认 100): ") or "100")
    
    return input_path, output_path, {
        "kernel_size": kernel_size,
        "pixel_size": pixel_size,
        "edge_thresh": edge_thresh
    }


def validate_parameters(kernel_size, pixel_size, edge_thresh):
    """Validate parameter ranges"""
    errors = []
    
    if not 1 <= kernel_size <= 50:
        errors.append(f"Kernel size must be between 1-50, got {kernel_size} / 核大小必须在1-50之间，当前值: {kernel_size}")
    if not 1 <= pixel_size <= 64:
        errors.append(f"Pixel size must be between 1-64, got {pixel_size} / 像素大小必须在1-64之间，当前值: {pixel_size}")
    if not 0 <= edge_thresh <= 255:
        errors.append(f"Edge threshold must be between 0-255, got {edge_thresh} / 边缘阈值必须在0-255之间，当前值: {edge_thresh}")
    
    if errors:
        print("❌ Parameter validation errors / 参数验证错误:")
        for error in errors:
            print(f"   {error}")
        return False
    return True


def print_parameters(kernel_size, pixel_size, edge_thresh):
    """Print current parameters"""
    print("\n📊 Current Parameters / 当前参数:")
    print(f"   Kernel Size / 核大小: {kernel_size} (color smoothness / 颜色平滑度)")
    print(f"   Pixel Size / 像素大小: {pixel_size} (pixel block size / 像素块大小)")
    print(f"   Edge Threshold / 边缘阈值: {edge_thresh} (black line intensity / 黑线强度)")
    print()


def convert_with_progress(input_path, output_path, kernel_size, pixel_size, edge_thresh):
    """Convert image with progress feedback"""
    try:
        print(f"\n🔄 Loading image / 加载图片: {input_path}")
        img_input = Image.open(input_path)
        print(f"   Image size / 图片尺寸: {img_input.size}")
        
        print("🔄 Converting to tensor / 转换为张量...")
        img_pt_input = img_common_util.convert_image_to_tensor(img_input)
        
        print("🔄 Initializing model / 初始化模型...")
        model = Photo2PixelModel()
        model.eval()
        
        print("🔄 Processing image / 处理图片...")
        with torch.no_grad():
            img_pt_output = model(
                img_pt_input,
                param_kernel_size=kernel_size,
                param_pixel_size=pixel_size,
                param_edge_thresh=edge_thresh
            )
        
        print("🔄 Saving result / 保存结果...")
        img_output = img_common_util.convert_tensor_to_image(img_pt_output)
        img_output.save(output_path)
        
        print(f"✅ Conversion completed / 转换完成!")
        print(f"   Output saved to / 输出保存至: {output_path}")
        
        # Show file info
        file_size = os.path.getsize(output_path) / 1024  # KB
        print(f"   File size / 文件大小: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error during conversion / 转换过程中出错: {str(e)}")
        return False
    
    return True


def main():
    """Main function with enhanced CLI"""
    parser = argparse.ArgumentParser(
        description='🎨 Photo2Pixel - Convert photos to pixel art / 照片转像素画转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / 使用示例:
  %(prog)s --input photo.jpg --output result.png
  %(prog)s --preset retro --input photo.jpg
  %(prog)s --interactive
  %(prog)s -k 12 -p 16 -e 80 --input photo.jpg

Presets / 预设:
  retro   - Retro pixel art style / 复古像素画风格 (k=8, p=12, e=80)
  smooth  - Smooth color transitions / 平滑颜色过渡 (k=16, p=20, e=120)
  sharp   - Sharp pixel art with strong edges / 锐利边缘像素画 (k=6, p=8, e=60)
  classic - Classic 8-bit style / 经典8位风格 (k=10, p=16, e=100)
        """
    )
    
    # File arguments
    parser.add_argument('--input', type=str, 
                       help='📁 Input image path / 输入图片路径 (supports: jpg, png, bmp, tiff / 支持: jpg, png, bmp, tiff)')
    parser.add_argument('--output', type=str,
                       help='💾 Output image path / 输出图片路径 (default: auto-generated / 默认: 自动生成)')
    
    # Parameter arguments
    parser.add_argument('-k', '--kernel_size', type=int, default=10,
                       help='🎨 Kernel size: Controls color smoothness / 核大小: 控制颜色平滑度 (1-50, default: 10 / 默认: 10)')
    parser.add_argument('-p', '--pixel_size', type=int, default=16,
                       help='🔲 Pixel size: Controls pixel block size / 像素大小: 控制像素块大小 (1-64, default: 16 / 默认: 16)')
    parser.add_argument('-e', '--edge_thresh', type=int, default=100,
                       help='✏️ Edge threshold: Controls black line intensity / 边缘阈值: 控制黑线强度 (0-255, default: 100 / 默认: 100)')
    
    # Mode arguments
    parser.add_argument('--preset', choices=['retro', 'smooth', 'sharp', 'classic'],
                       help='🎨 Use predefined parameter preset / 使用预定义参数预设')
    parser.add_argument('--interactive', action='store_true',
                       help='💬 Interactive mode: guided parameter input / 交互模式: 引导式参数输入')
    
    # Device argument
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda', 'mps'], default='auto',
                       help='⚙️ Device to use for processing / 处理设备 (default: auto / 默认: 自动)')
    
    # Info arguments
    parser.add_argument('--presets', action='store_true',
                       help='📋 Show available presets and exit / 显示可用预设并退出')
    parser.add_argument('--version', action='version', version='Photo2Pixel 1.0.0')
    
    args = parser.parse_args()
    
    # Show banner
    print_banner()
    
    # Handle special cases
    if args.presets:
        print_presets()
        return
    
    # Interactive mode
    if args.interactive:
        input_path, output_path, config = interactive_input()
        kernel_size = config['kernel_size']
        pixel_size = config['pixel_size']
        edge_thresh = config['edge_thresh']
    else:
        # Validate required arguments
        if not args.input:
            print("❌ Error: Input image path is required! / 错误: 需要输入图片路径!")
            print("💡 Use --interactive for guided setup or specify --input / 使用 --interactive 进行引导设置或指定 --input")
            parser.print_help()
            return
        
        input_path = args.input
        output_path = args.output or f"{os.path.splitext(input_path)[0]}_pixel.png"
        
        # Handle preset
        if args.preset:
            config = get_preset_config(args.preset)
            kernel_size = config['kernel_size']
            pixel_size = config['pixel_size']
            edge_thresh = config['edge_thresh']
            print(f"✅ Using '{args.preset}' preset / 使用 '{args.preset}' 预设")
        else:
            kernel_size = args.kernel_size
            pixel_size = args.pixel_size
            edge_thresh = args.edge_thresh
    
    # Validate parameters
    if not validate_parameters(kernel_size, pixel_size, edge_thresh):
        return
    
    # Clean and validate input file
    input_path = clean_dragged_path(input_path)
    
    if not os.path.exists(input_path):
        print(f"❌ Error: Input file not found / 错误: 输入文件未找到: {input_path}")
        return
    
    if not is_image_file(input_path):
        print(f"❌ Error: Not a supported image format / 错误: 不是支持的图片格式: {input_path}")
        print("💡 Supported formats / 支持的格式: jpg, jpeg, png, bmp, tiff, tif")
        return
    
    # Print parameters
    print_parameters(kernel_size, pixel_size, edge_thresh)
    
    # Convert image
    success = convert_with_progress(input_path, output_path, kernel_size, pixel_size, edge_thresh)
    
    if success:
        print("\n🎉 Conversion successful / 转换成功!")
        print("💡 Try different presets or parameters for different styles! / 尝试不同的预设或参数以获得不同风格!")
    else:
        print("\n💥 Conversion failed / 转换失败!")
        sys.exit(1)


if __name__ == '__main__':
    main()
