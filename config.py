#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 默认配置
DEFAULT_CONFIG = {
    # 输出配置
    'output_dir': 'output',
    'image_quality': 85,
    'max_image_size': (1920, 1080),
    
    # 网络配置
    'timeout': 30,
    'retry_times': 3,
    'retry_delay': 2,
    
    # 用户代理
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # 文件格式
    'supported_image_formats': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'supported_audio_formats': ['.mp3', '.wav', '.m4a', '.aac'],
    'supported_video_formats': ['.mp4', '.avi', '.mov', '.wmv'],
    
    # 内容处理
    'code_formatting': True,
    'remove_ads': True,
    'preserve_links': True,
}

class Config:
    """配置管理器"""
    
    def __init__(self, config_file=None):
        self.config = DEFAULT_CONFIG.copy()
        self.config_file = config_file or PROJECT_ROOT / 'config.json'
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                import json
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                self.config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置文件"""
        try:
            import json
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value

# 全局配置实例
config = Config()