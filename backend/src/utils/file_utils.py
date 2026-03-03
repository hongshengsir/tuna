#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块
提供文件操作相关的工具函数
"""

import os
import re
from pathlib import Path
from typing import Optional


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除连续的下划线
    filename = re.sub(r'_+', '_', filename)
    # 移除首尾的下划线和空格
    filename = filename.strip(' _')
    # 如果文件名为空，使用默认名称
    if not filename:
        filename = 'unnamed'
    
    return filename


def get_file_extension(url: str) -> str:
    """
    从URL中获取文件扩展名
    
    Args:
        url: 文件URL
        
    Returns:
        文件扩展名（包含点号，如.jpg）
    """
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # 获取扩展名
    ext = Path(path).suffix.lower()
    
    # 如果没有扩展名，尝试从路径中推断
    if not ext:
        # 常见的图片扩展名
        if any(img_ext in path.lower() for img_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
            ext = '.jpg' if '.jpg' in path.lower() or '.jpeg' in path.lower() else Path(path).suffix
        # 常见的音频扩展名
        elif any(audio_ext in path.lower() for audio_ext in ['.mp3', '.wav', '.m4a', '.aac', '.ogg']):
            ext = '.mp3' if '.mp3' in path.lower() else Path(path).suffix
        # 常见的视频扩展名
        elif any(video_ext in path.lower() for video_ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']):
            ext = '.mp4' if '.mp4' in path.lower() else Path(path).suffix
    
    return ext


def generate_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """
    生成唯一的文件名
    
    Args:
        directory: 目标目录
        base_name: 基础文件名
        extension: 文件扩展名
        
    Returns:
        唯一的文件路径
    """
    # 确保扩展名以点号开头
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # 尝试基础文件名
    filename = directory / f"{base_name}{extension}"
    counter = 1
    
    # 如果文件已存在，添加数字后缀
    while filename.exists():
        filename = directory / f"{base_name}_{counter}{extension}"
        counter += 1
    
    return filename


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.2f} {size_names[i]}"