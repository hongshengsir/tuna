#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章下载工具

将微信文章下载保存为Markdown格式，并保存文章中的图片、声音、视频等多媒体资源。
"""

import os
import re
import json
import time
import requests
import click
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from slugify import slugify
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# 导入数据库相关模块
from ..models.download_record import DownloadRecord
from ..models.download_record_dao import DownloadRecordDAO

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeChatDownloader:
    """微信文章下载器"""
    
    def __init__(self, output_dir: str = "output", user_id: int = None, db_connection=None):
        self.output_dir = Path(output_dir)
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化下载记录DAO
        self.download_dao = DownloadRecordDAO(db_connection)
        
    def download_article(self, url: str) -> Dict:
        """下载微信文章"""
        print(f"正在下载文章: {url}")
        
        try:
            # 获取文章HTML
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # 提取文章信息
            article_info = self._extract_article_info(soup, url)
            
            # 创建下载记录
            download_record = DownloadRecord(
                user_id=self.user_id,
                url=url,
                title=article_info.get('title', '未知标题'),
                author=article_info.get('author', '未知作者'),
                download_status='downloading'
            )
            record_id = self.download_dao.create_record(download_record)
            
            # 创建文章目录
            article_dir = self._create_article_directory(article_info['title'])
            
            # 下载多媒体资源
            media_info = self._download_media_resources(soup, article_dir)
            
            # 转换为Markdown
            markdown_content = self._convert_to_markdown(soup, media_info, article_dir)
            
            # 保存Markdown文件
            markdown_file = article_dir / f"{article_info['slug']}.md"
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            article_info['markdown_file'] = str(markdown_file)
            article_info['media_count'] = media_info['count']
            article_info['download_time'] = time.time()
            
            # 更新下载记录状态
            self.download_dao.update_record_status(
                record_id=record_id,
                status='completed',
                markdown_file=str(markdown_file),
                media_count=media_info['count'],
                file_size=markdown_file.stat().st_size
            )
            
            print(f"✓ 文章下载完成: {markdown_file}")
            return {"success": True, "data": article_info}
            
        except Exception as e:
            logger.error(f"下载文章失败: {e}")
            print(f"✗ 下载失败: {e}")
            # 更新下载记录状态为失败
            if 'record_id' in locals():
                self.download_dao.update_record_status(
                    record_id=record_id,
                    status='failed'
                )
            return {"success": False, "error": str(e)}
    
    def _extract_article_info(self, soup: BeautifulSoup, url: str) -> Dict:
        """提取文章基本信息"""
        # 提取标题
        title_elem = soup.find('h1') or soup.find('title')
        title = title_elem.get_text().strip() if title_elem else "未命名文章"
        
        # 提取作者
        author_elem = soup.find('meta', attrs={'name': 'author'}) or soup.find('span', class_=re.compile('author'))
        author = author_elem.get('content') if author_elem and author_elem.get('content') else "未知作者"
        
        # 提取发布时间
        publish_time_elem = soup.find('meta', attrs={'property': 'article:published_time'}) or soup.find('span', class_=re.compile('time'))
        publish_time = publish_time_elem.get('content') if publish_time_elem else ""
        
        # 生成slug
        slug = slugify(title)
        
        return {
            'title': title,
            'author': author,
            'publish_time': publish_time,
            'url': url,
            'slug': slug
        }
    
    def _create_article_directory(self, title: str) -> Path:
        """创建文章目录"""
        slug = slugify(title)
        article_dir = self.output_dir / slug
        
        # 创建子目录
        (article_dir / 'images').mkdir(parents=True, exist_ok=True)
        (article_dir / 'audio').mkdir(parents=True, exist_ok=True)
        (article_dir / 'video').mkdir(parents=True, exist_ok=True)
        
        return article_dir
    
    def _download_media_resources(self, soup: BeautifulSoup, article_dir: Path) -> Dict:
        """下载多媒体资源"""
        media_info = {
            'images': [],
            'audio': [],
            'video': [],
            'count': 0
        }
        
        # 下载图片
        images = soup.find_all('img')
        print(f"发现 {len(images)} 张图片，开始下载...")
        
        for i, img in enumerate(images):
            src = img.get('data-src') or img.get('src')
            if src and not src.startswith('data:'):
                try:
                    image_info = self._download_image(src, article_dir / 'images', i)
                    if image_info:
                        media_info['images'].append(image_info)
                        media_info['count'] += 1
                        img['data-local'] = image_info['local_path']
                        print(f"  下载图片 {i+1}/{len(images)}: {image_info['filename']}")
                except Exception as e:
                    logger.warning(f"下载图片失败 {src}: {e}")
        
        # 下载音频和视频（简化实现）
        # 实际项目中需要更复杂的解析逻辑
        
        print(f"图片下载完成，共下载 {len(media_info['images'])} 张图片")
        return media_info
    
    def _download_image(self, image_url: str, image_dir: Path, index: int) -> Optional[Dict]:
        """下载单张图片"""
        try:
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 获取文件扩展名
            parsed_url = urlparse(image_url)
            ext = Path(parsed_url.path).suffix
            if not ext:
                ext = '.jpg'
            
            filename = f"image_{index:03d}{ext}"
            filepath = image_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {
                'original_url': image_url,
                'local_path': f"images/{filename}",
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"下载图片失败: {image_url}, 错误: {e}")
            return None
    
    def _convert_to_markdown(self, soup: BeautifulSoup, media_info: Dict, article_dir: Path) -> str:
        """转换为Markdown格式"""
        # 获取文章主要内容区域
        content_elem = soup.find('div', class_=re.compile('rich_media_content')) or soup.find('article')
        
        if not content_elem:
            # 如果没有找到特定区域，使用body
            content_elem = soup.find('body')
        
        # 转换为Markdown
        markdown_text = md(str(content_elem) if content_elem else str(soup))
        
        # 后处理：修复图片链接
        for image_info in media_info['images']:
            markdown_text = markdown_text.replace(
                image_info['original_url'], 
                image_info['local_path']
            )
        
        # 添加文章元信息
        title = soup.find('h1') or soup.find('title')
        if title:
            title_text = title.get_text().strip()
            markdown_text = f"# {title_text}\n\n{markdown_text}"
        
        return markdown_text

@click.command()
@click.option('--url', '-u', help='微信文章URL')
@click.option('--file', '-f', help='包含多个URL的文件路径')
@click.option('--output', '-o', default='output', help='输出目录')
@click.option('--format', '-fmt', default='markdown', help='输出格式')
@click.option('--download-media/--no-download-media', default=True, help='是否下载多媒体资源')
def main(url, file, output, format, download_media):
    """微信文章下载工具主函数"""
    
    print("=" * 50)
    print("微信文章下载工具")
    print("=" * 50)
    
    downloader = WeChatDownloader(output)
    
    urls = []
    
    if url:
        urls.append(url)
    elif file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"错误: 文件不存在: {file}")
            return
    else:
        # 交互式输入
        print("请输入微信文章URL（输入空行结束）:")
        while True:
            input_url = input("> ").strip()
            if not input_url:
                break
            urls.append(input_url)
    
    if not urls:
        print("警告: 没有提供有效的URL")
        return
    
    # 批量下载
    success_count = 0
    for i, article_url in enumerate(urls, 1):
        print(f"\n处理第 {i}/{len(urls)} 篇文章")
        
        try:
            result = downloader.download_article(article_url)
            success_count += 1
            
            # 显示下载结果
            print("-" * 30)
            print("下载完成:")
            print(f"  标题: {result['title']}")
            print(f"  作者: {result['author']}")
            print(f"  文件: {result['markdown_file']}")
            print(f"  媒体文件: {result['media_count']} 个")
            print("-" * 30)
            
        except Exception as e:
            print(f"处理失败: {article_url}")
            logger.error(f"处理失败 {article_url}: {e}")
    
    print(f"\n✓ 完成! 成功下载 {success_count}/{len(urls)} 篇文章")

if __name__ == "__main__":
    main()