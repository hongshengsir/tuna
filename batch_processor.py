#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批处理处理器 - 支持批量下载多个微信文章
"""

import os
import time
from pathlib import Path
from typing import List, Dict

from wechat_downloader import WeChatDownloader

class BatchProcessor:
    """批处理处理器"""
    
    def __init__(self, output_dir: str = "batch_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.downloader = WeChatDownloader(output_dir)
    
    def process_urls_file(self, urls_file: str) -> Dict:
        """处理包含URL列表的文件"""
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            return self.process_urls(urls)
            
        except FileNotFoundError:
            print(f"错误: 文件不存在: {urls_file}")
            return {'success': 0, 'failed': 0, 'total': 0, 'results': []}
        except Exception as e:
            print(f"错误: 读取文件失败: {e}")
            return {'success': 0, 'failed': 0, 'total': 0, 'results': []}
    
    def process_urls(self, urls: List[str]) -> Dict:
        """处理URL列表"""
        if not urls:
            print("警告: 没有提供有效的URL")
            return {'success': 0, 'failed': 0, 'total': 0, 'results': []}
        
        total = len(urls)
        results = []
        success_count = 0
        failed_count = 0
        
        print(f"开始批量处理 {total} 篇文章...")
        
        for i, url in enumerate(urls, 1):
            print(f"处理第 {i}/{total} 篇文章: {url}")
            
            try:
                result = self.downloader.download_article(url)
                results.append({
                    'url': url,
                    'success': True,
                    'title': result['title'],
                    'file': result['markdown_file'],
                    'media_count': result['media_count']
                })
                success_count += 1
                print(f"  成功: {result['title']}")
                
            except Exception as e:
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })
                failed_count += 1
                print(f"  失败: {e}")
            
            # 添加短暂延迟，避免请求过于频繁
            time.sleep(1)
        
        # 显示结果摘要
        self._show_summary(success_count, failed_count, total, results)
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': total,
            'results': results
        }
    
    def _show_summary(self, success_count: int, failed_count: int, total: int, results: List[Dict]):
        """显示处理结果摘要"""
        
        print("\n" + "="*50)
        print("批量处理结果摘要")
        print("="*50)
        print(f"总文章数: {total}")
        print(f"成功下载: {success_count}")
        print(f"下载失败: {failed_count}")
        print(f"成功率: {success_count/total*100:.1f}%")
        print("="*50)
        
        # 显示失败的文章
        if failed_count > 0:
            print("\n下载失败的文章:")
            for result in results:
                if not result['success']:
                    print(f"- {result['url']}: {result['error']}")
        
        # 显示成功的文章
        if success_count > 0:
            print("\n成功下载的文章:")
            for result in results:
                if result['success']:
                    print(f"- {result['title']} ({result['file']})")

def main():
    """批处理主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信文章批量下载工具')
    parser.add_argument('--file', '-f', required=True, help='包含URL列表的文件路径')
    parser.add_argument('--output', '-o', default='batch_output', help='输出目录')
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.output)
    processor.process_urls_file(args.file)

if __name__ == "__main__":
    main()