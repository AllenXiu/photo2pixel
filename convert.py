import torch
from PIL import Image
import argparse
import os
import sys
from pathlib import Path

from models.module_photo2pixel import Photo2PixelModel
from utils import img_common_util


def print_banner():
    """Print program banner"""
    print("=" * 60)
    print("🎨 Photo2Pixel - Photo to Pixel Art Converter")
    print("=" * 60)
    print("Convert your photos into beautiful pixel art!")
    print("Online demo: https://photo2pixel.co")
    print("=" * 60)


def print_presets():
    """Print available presets"""
    presets = {
        "retro": {"kernel_size": 8, "pixel_size": 12, "edge_thresh": 80, "desc": "Retro pixel art style"},
        "smooth": {"kernel_size": 16, "pixel_size": 20, "edge_thresh": 120, "desc": "Smooth color transitions"},
        "sharp": {"kernel_size": 6, "pixel_size": 8, "edge_thresh": 60, "desc": "Sharp pixel art with strong edges"},
        "classic": {"kernel_size": 10, "pixel_size": 16, "edge_thresh": 100, "desc": "Classic 8-bit style"}
    }
    
    print("\n📋 Available Presets:")
    for name, config in presets.items():
        print(f"  {name:8} - {config['desc']}")
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


def interactive_input():
    """Interactive parameter input"""
    print("\n🔧 Interactive Configuration")
    print("-" * 30)
    
    # Input file
    while True:
        input_path = input("📁 Input image path (or press Enter for default): ").strip()
        if not input_path:
            input_path = "./images/example_input_mountain.jpg"
        if os.path.exists(input_path):
            break
        print(f"❌ File not found: {input_path}")
        print("💡 Please enter a valid image file path")
    
    # Output file
    output_path = input("💾 Output image path (or press Enter for auto): ").strip()
    if not output_path:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_pixel.png"
    
    # Preset selection
    print_presets()
    preset = input("🎨 Choose preset (retro/smooth/sharp/classic) or press Enter for custom: ").strip().lower()
    
    if preset in ["retro", "smooth", "sharp", "classic"]:
        config = get_preset_config(preset)
        print(f"✅ Using '{preset}' preset")
        return input_path, output_path, config
    
    # Custom parameters
    print("\n⚙️  Custom Parameters:")
    print("💡 Kernel Size: Controls color smoothness (1-50, higher = smoother)")
    kernel_size = int(input("   Kernel Size (default 10): ") or "10")
    
    print("💡 Pixel Size: Controls pixel block size (1-64, higher = larger pixels)")
    pixel_size = int(input("   Pixel Size (default 16): ") or "16")
    
    print("💡 Edge Threshold: Controls black line intensity (0-255, lower = more lines)")
    edge_thresh = int(input("   Edge Threshold (default 100): ") or "100")
    
    return input_path, output_path, {
        "kernel_size": kernel_size,
        "pixel_size": pixel_size,
        "edge_thresh": edge_thresh
    }


def validate_parameters(kernel_size, pixel_size, edge_thresh):
    """Validate parameter ranges"""
    errors = []
    
    if not 1 <= kernel_size <= 50:
        errors.append(f"Kernel size must be between 1-50, got {kernel_size}")
    if not 1 <= pixel_size <= 64:
        errors.append(f"Pixel size must be between 1-64, got {pixel_size}")
    if not 0 <= edge_thresh <= 255:
        errors.append(f"Edge threshold must be between 0-255, got {edge_thresh}")
    
    if errors:
        print("❌ Parameter validation errors:")
        for error in errors:
            print(f"   {error}")
        return False
    return True


def print_parameters(kernel_size, pixel_size, edge_thresh):
    """Print current parameters"""
    print("\n📊 Current Parameters:")
    print(f"   Kernel Size: {kernel_size} (color smoothness)")
    print(f"   Pixel Size: {pixel_size} (pixel block size)")
    print(f"   Edge Threshold: {edge_thresh} (black line intensity)")
    print()


def convert_with_progress(input_path, output_path, kernel_size, pixel_size, edge_thresh):
    """Convert image with progress feedback"""
    try:
        print(f"\n🔄 Loading image: {input_path}")
        img_input = Image.open(input_path)
        print(f"   Image size: {img_input.size}")
        
        print("🔄 Converting to tensor...")
        img_pt_input = img_common_util.convert_image_to_tensor(img_input)
        
        print("🔄 Initializing model...")
        model = Photo2PixelModel()
        model.eval()
        
        print("🔄 Processing image...")
        with torch.no_grad():
            img_pt_output = model(
                img_pt_input,
                param_kernel_size=kernel_size,
                param_pixel_size=pixel_size,
                param_edge_thresh=edge_thresh
            )
        
        print("🔄 Saving result...")
        img_output = img_common_util.convert_tensor_to_image(img_pt_output)
        img_output.save(output_path)
        
        print(f"✅ Conversion completed!")
        print(f"   Output saved to: {output_path}")
        
        # Show file info
        file_size = os.path.getsize(output_path) / 1024  # KB
        print(f"   File size: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        return False
    
    return True


def main():
    """Main function with enhanced CLI"""
    parser = argparse.ArgumentParser(
        description='🎨 Photo2Pixel - Convert photos to pixel art',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input photo.jpg --output result.png
  %(prog)s --preset retro --input photo.jpg
  %(prog)s --interactive
  %(prog)s -k 12 -p 16 -e 80 --input photo.jpg

Presets:
  retro   - Retro pixel art style (k=8, p=12, e=80)
  smooth  - Smooth color transitions (k=16, p=20, e=120)
  sharp   - Sharp pixel art with strong edges (k=6, p=8, e=60)
  classic - Classic 8-bit style (k=10, p=16, e=100)
        """
    )
    
    # File arguments
    parser.add_argument('--input', type=str, 
                       help='📁 Input image path (supports: jpg, png, bmp, tiff)')
    parser.add_argument('--output', type=str,
                       help='💾 Output image path (default: auto-generated)')
    
    # Parameter arguments
    parser.add_argument('-k', '--kernel_size', type=int, default=10,
                       help='🎨 Kernel size: Controls color smoothness (1-50, default: 10)')
    parser.add_argument('-p', '--pixel_size', type=int, default=16,
                       help='🔲 Pixel size: Controls pixel block size (1-64, default: 16)')
    parser.add_argument('-e', '--edge_thresh', type=int, default=100,
                       help='✏️ Edge threshold: Controls black line intensity (0-255, default: 100)')
    
    # Mode arguments
    parser.add_argument('--preset', choices=['retro', 'smooth', 'sharp', 'classic'],
                       help='🎨 Use predefined parameter preset')
    parser.add_argument('--interactive', action='store_true',
                       help='💬 Interactive mode: guided parameter input')
    
    # Device argument
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda', 'mps'], default='auto',
                       help='⚙️ Device to use for processing (default: auto)')
    
    # Info arguments
    parser.add_argument('--presets', action='store_true',
                       help='📋 Show available presets and exit')
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
            print("❌ Error: Input image path is required!")
            print("💡 Use --interactive for guided setup or specify --input")
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
            print(f"✅ Using '{args.preset}' preset")
        else:
            kernel_size = args.kernel_size
            pixel_size = args.pixel_size
            edge_thresh = args.edge_thresh
    
    # Validate parameters
    if not validate_parameters(kernel_size, pixel_size, edge_thresh):
        return
    
    # Validate input file
    if not os.path.exists(input_path):
        print(f"❌ Error: Input file not found: {input_path}")
        return
    
    # Print parameters
    print_parameters(kernel_size, pixel_size, edge_thresh)
    
    # Convert image
    success = convert_with_progress(input_path, output_path, kernel_size, pixel_size, edge_thresh)
    
    if success:
        print("\n🎉 Conversion successful!")
        print("💡 Try different presets or parameters for different styles!")
    else:
        print("\n💥 Conversion failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
