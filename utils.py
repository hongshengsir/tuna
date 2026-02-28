#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数
"""

import re
import hashlib
import time
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """清理文件名，移除非法字符"""
    # 移除非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # 移除多余的空格和下划线
    filename = re.sub(r'\s+', ' ', filename)
    filename = re.sub(r'_+', '_', filename)
    
    # 限制长度
    if len(filename) > max_length:
        name, ext = Path(filename).stem, Path(filename).suffix
        filename = name[:max_length-len(ext)] + ext
    
    return filename.strip()

def get_file_extension(url: str, default: str = '.bin') -> str:
    """从URL获取文件扩展名"""
    parsed = urlparse(url)
    path = parsed.path
    
    # 从路径中提取扩展名
    ext = Path(path).suffix.lower()
    
    # 如果没有扩展名，尝试从Content-Type推断
    if not ext:
        # 这里可以添加根据Content-Type推断扩展名的逻辑
        ext = default
    
    return ext

def generate_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """生成唯一的文件名"""
    counter = 1
    while True:
        if counter == 1:
            filename = directory / f"{base_name}{extension}"
        else:
            filename = directory / f"{base_name}_{counter}{extension}"
        
        if not filename.exists():
            return filename
        counter += 1

def is_valid_url(url: str) -> bool:
    """检查URL是否有效"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def extract_domain(url: str) -> str:
    """从URL提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def extract_wechat_article_id(url: str) -> Optional[str]:
    """从微信文章URL提取文章ID"""
    # 微信文章URL模式
    patterns = [
        r'src="(https?://mp\.weixin\.qq\.com/s/[_\-\w]+)"',
        r'(https?://mp\.weixin\.qq\.com/s/[_\-\w]+)',
        r'__biz=[^&]+&mid=([^&]+)&',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1) if match.lastindex else match.group(0)
    
    return None

def clean_html_content(html: str) -> str:
    """清理HTML内容"""
    # 移除script和style标签
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # 移除注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    return html

def detect_content_type(content: bytes) -> str:
    """检测内容类型"""
    # 简单的文件类型检测
    if content.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    elif content.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif content.startswith(b'GIF8'):
        return 'image/gif'
    elif content.startswith(b'RIFF') and content[8:12] == b'WEBP':
        return 'image/webp'
    elif content.startswith(b'ID3'):
        return 'audio/mpeg'
    elif content.startswith(b'\x00\x00\x00 ftyp'):
        return 'video/mp4'
    else:
        return 'application/octet-stream'

def create_progress_callback(description: str, total: int):
    """创建进度回调函数"""
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.console import Console
    
    console = Console()
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    )
    
    task = progress.add_task(description, total=total)
    progress.start()
    
    def callback(current: int):
        progress.update(task, completed=current)
    
    def finish():
        progress.stop()
    
    return callback, finish