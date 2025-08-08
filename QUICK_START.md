# 🎨 Photo2Pixel 快速启动指南

## 快速启动脚本

我们为你提供了多个快速启动脚本，让你可以更方便地使用 Photo2Pixel：

### 1. 最简单的启动方式
```bash
./quick.sh
```
或
```bash
source .venv/bin/activate && python convert.py --interactive
```

### 2. 高级启动脚本
```bash
# 交互模式（推荐）
python3 start.py

# 使用预设
python3 start.py --preset retro --input image.jpg

# 自定义参数
python3 start.py --input image.jpg -k 12 -p 16 -e 80
```

### 3. Bash 脚本启动
```bash
./run.sh
```

## 🚀 使用方式

### 交互模式（推荐新手）
```bash
python3 start.py
```
- 支持拖拽图片
- 引导式参数设置
- 实时帮助提示

### 预设模式（推荐常用）
```bash
# 复古风格
python3 start.py --preset retro --input photo.jpg

# 平滑风格
python3 start.py --preset smooth --input photo.jpg

# 锐利风格
python3 start.py --preset sharp --input photo.jpg

# 经典风格
python3 start.py --preset classic --input photo.jpg
```

### 自定义模式（高级用户）
```bash
python3 start.py --input photo.jpg -k 12 -p 16 -e 80 --output result.png
```

## 📋 预设说明

| 预设 | 风格 | 核大小 | 像素大小 | 边缘阈值 |
|------|------|--------|----------|----------|
| retro | 复古像素画 | 8 | 12 | 80 |
| smooth | 平滑过渡 | 16 | 20 | 120 |
| sharp | 锐利边缘 | 6 | 8 | 60 |
| classic | 经典8位 | 10 | 16 | 100 |

## 💡 拖拽功能

在交互模式下，你可以：
1. 直接从 Finder 拖拽图片到终端
2. 程序会自动清理路径格式
3. 验证文件格式和存在性
4. 支持 macOS 拖拽格式

## 🔧 环境管理

启动脚本会自动：
- ✅ 检查虚拟环境
- 📦 安装依赖
- 🚀 启动程序
- 💬 提供中英双语界面

## 📁 文件结构

```
photo2pixel/
├── quick.sh          # 最简单的启动脚本
├── run.sh            # Bash 启动脚本
├── start.py          # Python 高级启动脚本
├── convert.py        # 主程序
└── requirements.txt  # 依赖列表
```

## 🎯 快速开始

1. **克隆项目**
   ```bash
   git clone https://github.com/your-repo/photo2pixel.git
   cd photo2pixel
   ```

2. **快速启动**
   ```bash
   ./quick.sh
   ```

3. **拖拽图片**
   - 在交互模式下直接拖拽图片到终端
   - 选择预设或自定义参数
   - 等待转换完成

## 🆘 常见问题

### Q: 虚拟环境不存在？
A: 启动脚本会自动创建并安装依赖

### Q: 拖拽图片不工作？
A: 确保在交互模式下使用，程序会自动清理路径格式

### Q: 想要更多控制？
A: 使用 `python3 start.py --help` 查看所有选项

## 📞 支持

- 在线演示：https://photo2pixel.co
- 项目地址：https://github.com/your-repo/photo2pixel
- 问题反馈：请提交 Issue
