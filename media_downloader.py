#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
媒体下载器 - 专门处理图片、音频、视频等多媒体资源的下载
"""

import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import logging

from utils import sanitize_filename, get_file_extension, generate_unique_filename, format_file_size

logger = logging.getLogger(__name__)

class MediaDownloader:
    """媒体下载器"""
    
    def __init__(self, session: requests.Session, base_dir: Path):
        self.session = session
        self.base_dir = base_dir
        
        # 创建媒体目录
        self.image_dir = base_dir / 'images'
        self.audio_dir = base_dir / 'audio'
        self.video_dir = base_dir / 'video'
        
        self.image_dir.mkdir(exist_ok=True)
        self.audio_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)
        
        # 下载统计
        self.stats = {
            'images': {'downloaded': 0, 'failed': 0, 'total_size': 0},
            'audio': {'downloaded': 0, 'failed': 0, 'total_size': 0},
            'video': {'downloaded': 0, 'failed': 0, 'total_size': 0}
        }
    
    def download_all_media(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """下载所有媒体资源"""
        media_info = {
            'images': [],
            'audio': [],
            'video': [],
            'mapping': {}  # 原始URL到本地路径的映射
        }
        
        # 下载图片
        media_info['images'] = self._download_images(soup, base_url)
        
        # 下载音频
        media_info['audio'] = self._download_audio(soup, base_url)
        
        # 下载视频
        media_info['video'] = self._download_videos(soup, base_url)
        
        # 创建映射表
        for image in media_info['images']:
            if image['success']:
                media_info['mapping'][image['original_url']] = image['local_path']
        
        for audio in media_info['audio']:
            if audio['success']:
                media_info['mapping'][audio['original_url']] = audio['local_path']
        
        for video in media_info['video']:
            if video['success']:
                media_info['mapping'][video['original_url']] = video['local_path']
        
        return media_info
    
    def _download_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """下载图片资源"""
        images = []
        img_elements = soup.find_all('img')
        
        for i, img in enumerate(img_elements):
            src = img.get('data-src') or img.get('src')
            if not src:
                continue
            
            # 处理相对URL
            if not src.startswith(('http://', 'https://')):
                src = urljoin(base_url, src)
            
            # 跳过data URL和内联图片
            if src.startswith('data:'):
                continue
            
            try:
                result = self._download_single_file(src, self.image_dir, 'image', i)
                images.append(result)
                
                if result['success']:
                    self.stats['images']['downloaded'] += 1
                    self.stats['images']['total_size'] += result['size']
                    # 更新img标签的src属性
                    img['src'] = result['local_path']
                else:
                    self.stats['images']['failed'] += 1
                    
            except Exception as e:
                logger.error(f"下载图片失败 {src}: {e}")
                images.append({
                    'original_url': src,
                    'success': False,
                    'error': str(e),
                    'type': 'image'
                })
                self.stats['images']['failed'] += 1
        
        return images
    
    def _download_audio(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """下载音频资源"""
        audio_files = []
        
        # 查找音频元素
        audio_elements = soup.find_all('audio')
        audio_links = soup.find_all('a', href=re.compile(r'\.(mp3|wav|m4a|aac)$', re.I))
        
        for i, audio in enumerate(audio_elements):
            src = audio.get('src')
            if src:
                audio_files.extend(self._process_audio_source(src, base_url, i))
        
        for i, link in enumerate(audio_links, len(audio_elements)):
            href = link.get('href')
            if href:
                audio_files.extend(self._process_audio_source(href, base_url, i))
        
        return audio_files
    
    def _process_audio_source(self, src: str, base_url: str, index: int) -> List[Dict]:
        """处理单个音频源"""
        results = []
        
        if not src.startswith(('http://', 'https://')):
            src = urljoin(base_url, src)
        
        try:
            result = self._download_single_file(src, self.audio_dir, 'audio', index)
            results.append(result)
            
            if result['success']:
                self.stats['audio']['downloaded'] += 1
                self.stats['audio']['total_size'] += result['size']
            else:
                self.stats['audio']['failed'] += 1
                
        except Exception as e:
            logger.error(f"下载音频失败 {src}: {e}")
            results.append({
                'original_url': src,
                'success': False,
                'error': str(e),
                'type': 'audio'
            })
            self.stats['audio']['failed'] += 1
        
        return results
    
    def _download_videos(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """下载视频资源"""
        video_files = []
        
        # 查找视频元素
        video_elements = soup.find_all('video')
        video_links = soup.find_all('a', href=re.compile(r'\.(mp4|avi|mov|wmv)$', re.I))
        
        for i, video in enumerate(video_elements):
            src = video.get('src')
            if src:
                video_files.extend(self._process_video_source(src, base_url, i))
        
        for i, link in enumerate(video_links, len(video_elements)):
            href = link.get('href')
            if href:
                video_files.extend(self._process_video_source(href, base_url, i))
        
        return video_files
    
    def _process_video_source(self, src: str, base_url: str, index: int) -> List[Dict]:
        """处理单个视频源"""
        results = []
        
        if not src.startswith(('http://', 'https://')):
            src = urljoin(base_url, src)
        
        try:
            result = self._download_single_file(src, self.video_dir, 'video', index)
            results.append(result)
            
            if result['success']:
                self.stats['video']['downloaded'] += 1
                self.stats['video']['total_size'] += result['size']
            else:
                self.stats['video']['failed'] += 1
                
        except Exception as e:
            logger.error(f"下载视频失败 {src}: {e}")
            results.append({
                'original_url': src,
                'success': False,
                'error': str(e),
                'type': 'video'
            })
            self.stats['video']['failed'] += 1
        
        return results
    
    def _download_single_file(self, url: str, directory: Path, file_type: str, index: int) -> Dict:
        """下载单个文件"""
        try:
            # 发送请求
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # 获取文件信息
            content_type = response.headers.get('content-type', '')
            content_length = int(response.headers.get('content-length', 0))
            
            # 生成文件名
            ext = get_file_extension(url)
            if not ext:
                # 根据Content-Type推断扩展名
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'mp3' in content_type:
                    ext = '.mp3'
                elif 'mp4' in content_type:
                    ext = '.mp4'
                else:
                    ext = '.bin'
            
            # 生成基础文件名
            parsed_url = urlparse(url)
            base_name = Path(parsed_url.path).stem or f"{file_type}_{index:03d}"
            base_name = sanitize_filename(base_name)
            
            # 生成唯一文件名
            filename = generate_unique_filename(directory, base_name, ext)
            
            # 下载文件
            file_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)
            
            # 计算相对路径
            relative_path = filename.relative_to(self.base_dir)
            
            return {
                'original_url': url,
                'local_path': str(relative_path),
                'filename': filename.name,
                'size': file_size,
                'content_type': content_type,
                'success': True,
                'type': file_type
            }
            
        except Exception as e:
            logger.error(f"下载文件失败 {url}: {e}")
            return {
                'original_url': url,
                'success': False,
                'error': str(e),
                'type': file_type
            }
    
    def get_stats(self) -> Dict:
        """获取下载统计信息"""
        total_downloaded = (
            self.stats['images']['downloaded'] + 
            self.stats['audio']['downloaded'] + 
            self.stats['video']['downloaded']
        )
        total_failed = (
            self.stats['images']['failed'] + 
            self.stats['audio']['failed'] + 
            self.stats['video']['failed']
        )
        total_size = (
            self.stats['images']['total_size'] + 
            self.stats['audio']['total_size'] + 
            self.stats['video']['total_size']
        )
        
        return {
            'total': {
                'downloaded': total_downloaded,
                'failed': total_failed,
                'total_size': format_file_size(total_size)
            },
            'images': {
                'downloaded': self.stats['images']['downloaded'],
                'failed': self.stats['images']['failed'],
                'total_size': format_file_size(self.stats['images']['total_size'])
            },
            'audio': {
                'downloaded': self.stats['audio']['downloaded'],
                'failed': self.stats['audio']['failed'],
                'total_size': format_file_size(self.stats['audio']['total_size'])
            },
            'video': {
                'downloaded': self.stats['video']['downloaded'],
                'failed': self.stats['video']['failed'],
                'total_size': format_file_size(self.stats['video']['total_size'])
            }
        }