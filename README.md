# 微信文章下载工具

一个强大的工具，用于下载微信文章并将其保存为Markdown格式，同时保存文章中的图片、音频、视频等多媒体资源。

## 功能特性

- ✅ 解析微信文章URL并提取内容
- ✅ 将文章内容转换为Markdown格式
- ✅ 下载并保存文章中的图片资源
- ✅ 下载并保存文章中的音频和视频资源
- ✅ 格式化代码块（如果文章包含代码）
- ✅ 友好的命令行界面
- ✅ 支持批量下载

## 安装

### 方法一：使用安装脚本（推荐）
```bash
# 运行安装脚本
python setup.py
```

### 方法二：手动安装
1. 确保已安装Python 3.7或更高版本
2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 方法三：使用conda（如果已安装）
```bash
conda create -n wechat-downloader python=3.9
conda activate wechat-downloader
pip install -r requirements.txt
```

## 使用方法

### 基本使用
```bash
python wechat_downloader.py --url "微信文章URL" --output "输出目录"
```

### 批量下载
```bash
python wechat_downloader.py --file "urls.txt" --output "输出目录"
```

### 交互式使用
```bash
python wechat_downloader.py
```

## 配置选项

- `--url`: 单个微信文章URL
- `--file`: 包含多个URL的文件路径
- `--output`: 输出目录路径
- `--format`: 输出格式（默认：markdown）
- `--download-media`: 是否下载多媒体资源（默认：true）

## 输出结构

```
输出目录/
├── article_title.md
├── images/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── audio/
│   └── audio1.mp3
└── video/
    └── video1.mp4
```

## 许可证

MIT License