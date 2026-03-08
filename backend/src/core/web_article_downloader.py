#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用网页文章下载工具

支持下载任意网页的文章内容，转换为Markdown格式，并保存文章中的图片等资源。
"""

import os
import re
import json
import time
import requests
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

class WebArticleDownloader:
    """通用网页文章下载器"""
    
    def __init__(self, output_dir: str = "web_output", user_id: int = None, db_connection=None):
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
        """下载网页文章"""
        print(f"正在下载网页文章: {url}")
        
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
                download_status='downloading',
                source_type='web'  # 标记为网页文章
            )
            record_id = self.download_dao.create_record(download_record)
            
            # 创建文章目录
            article_dir = self._create_article_directory(article_info['title'])
            
            # 下载多媒体资源
            media_info = self._download_media_resources(soup, article_dir, url)
            
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
            
            print(f"✓ 网页文章下载完成: {markdown_file}")
            return article_info
            
        except Exception as e:
            logger.error(f"下载网页文章失败: {url}, 错误: {e}")
            raise
    
    def _extract_article_info(self, soup: BeautifulSoup, url: str) -> Dict:
        """提取文章信息"""
        # 提取标题
        title = self._extract_title(soup)
        
        # 提取作者
        author = self._extract_author(soup)
        
        # 提取发布日期
        publish_date = self._extract_publish_date(soup)
        
        # 生成slug
        slug = slugify(title)
        
        return {
            'title': title,
            'author': author,
            'publish_date': publish_date,
            'url': url,
            'slug': slug
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取文章标题"""
        # 尝试多种标题选择器
        title_selectors = [
            'h1',
            'title',
            '.article-title',
            '.post-title',
            '.entry-title',
            '.title',
            'h1[class*="title"]',
            'h1[class*="headline"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()
        
        # 如果都没找到，使用页面title
        return soup.title.get_text().strip() if soup.title else '未知标题'
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者信息"""
        author_selectors = [
            '.author',
            '.byline',
            '.post-author',
            '.article-author',
            'meta[name="author"]',
            '[rel="author"]'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '未知作者')
                else:
                    text = element.get_text().strip()
                    if text:
                        return text
        
        return '未知作者'
    
    def _extract_publish_date(self, soup: BeautifulSoup) -> str:
        """提取发布日期"""
        date_selectors = [
            'time',
            '.publish-date',
            '.post-date',
            '.article-date',
            '.date',
            'meta[property="article:published_time"]',
            'meta[name="publish_date"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '')
                else:
                    text = element.get_text().strip()
                    if text:
                        return text
        
        return ''
    
    def _create_article_directory(self, title: str) -> Path:
        """创建文章目录"""
        slug = slugify(title)
        article_dir = self.output_dir / slug
        article_dir.mkdir(exist_ok=True)
        return article_dir
    
    def _download_media_resources(self, soup: BeautifulSoup, article_dir: Path, base_url: str) -> Dict:
        """下载多媒体资源"""
        media_info = {
            'images': [],
            'count': 0
        }
        
        # 下载图片
        images = soup.find_all('img')
        for i, img in enumerate(images):
            src = img.get('src')
            if src:
                try:
                    # 处理相对路径
                    if not src.startswith(('http://', 'https://')):
                        src = urljoin(base_url, src)
                    
                    # 下载图片
                    img_response = self.session.get(src, timeout=10)
                    img_response.raise_for_status()
                    
                    # 获取文件扩展名
                    content_type = img_response.headers.get('content-type', '')
                    ext = self._get_extension_from_content_type(content_type) or '.jpg'
                    
                    # 保存图片
                    img_filename = f"image_{i+1:03d}{ext}"
                    img_path = article_dir / img_filename
                    
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    # 更新图片src为本地路径
                    img['src'] = img_filename
                    
                    media_info['images'].append({
                        'original_url': src,
                        'local_path': str(img_path),
                        'filename': img_filename
                    })
                    media_info['count'] += 1
                    
                except Exception as e:
                    logger.warning(f"下载图片失败: {src}, 错误: {e}")
                    # 保留原始图片链接
        
        return media_info
    
    def _get_extension_from_content_type(self, content_type: str) -> str:
        """根据Content-Type获取文件扩展名"""
        extensions = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg'
        }
        return extensions.get(content_type.lower(), '.jpg')
    
    def _convert_to_markdown(self, soup: BeautifulSoup, media_info: Dict, article_dir: Path) -> str:
        """转换为Markdown格式"""
        # 提取主要内容区域
        content = self._extract_main_content(soup)
        
        if not content:
            # 如果没有找到主要内容，使用整个body
            content = soup.find('body') or soup
        
        # 转换为Markdown
        markdown_content = md(
            str(content),
            heading_style='ATX',
            bullets='-',
            strip=['script', 'style']
        )
        
        # 添加文章信息头部
        header = self._generate_markdown_header(soup, media_info)
        
        return header + '\n\n' + markdown_content
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """提取文章主要内容"""
        content_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            'main',
            '[role="main"]'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element
        
        return None
    
    def _generate_markdown_header(self, soup: BeautifulSoup, media_info: Dict) -> str:
        """生成Markdown文件头部信息"""
        title = self._extract_title(soup)
        author = self._extract_author(soup)
        publish_date = self._extract_publish_date(soup)
        
        header = f"""# {title}

**作者**: {author}
**发布日期**: {publish_date if publish_date else '未知'}
**下载时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**媒体资源数量**: {media_info['count']}

---

"""
        
        return header
    
    def batch_download(self, urls: List[str]) -> List[Dict]:
        """批量下载网页文章"""
        results = []
        
        for i, url in enumerate(urls):
            try:
                result = self.download_article(url)
                results.append({
                    'url': url,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'status': 'error',
                    'error': str(e)
                })
            
            # 添加延迟避免请求过于频繁
            time.sleep(1)
        
        return results