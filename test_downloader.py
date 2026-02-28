#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 用于测试微信文章下载功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from wechat_downloader import WeChatDownloader
from batch_processor import BatchProcessor

def test_single_download():
    """测试单个文章下载"""
    print("=== 测试单个文章下载 ===")
    
    # 这里可以替换为实际的微信文章URL进行测试
    test_url = "https://mp.weixin.qq.com/s/example"
    
    downloader = WeChatDownloader("test_output")
    
    try:
        result = downloader.download_article(test_url)
        print("✓ 测试成功!")
        print(f"标题: {result['title']}")
        print(f"文件: {result['markdown_file']}")
        print(f"媒体文件数: {result['media_count']}")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_batch_download():
    """测试批量下载"""
    print("\n=== 测试批量下载 ===")
    
    # 创建测试URL文件
    test_urls = [
        "https://mp.weixin.qq.com/s/test1",
        "https://mp.weixin.qq.com/s/test2", 
        "https://mp.weixin.qq.com/s/test3"
    ]
    
    test_file = "test_urls.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        for url in test_urls:
            f.write(url + '\n')
    
    processor = BatchProcessor("test_batch_output")
    result = processor.process_urls_file(test_file)
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print(f"批量处理结果: {result['success']} 成功, {result['failed']} 失败")
    return result['success'] > 0

def test_media_downloader():
    """测试媒体下载器"""
    print("\n=== 测试媒体下载器 ===")
    
    try:
        import requests
        from media_downloader import MediaDownloader
        from bs4 import BeautifulSoup
        
        # 创建一个简单的测试HTML
        test_html = """
        <html>
        <body>
            <img src="https://via.placeholder.com/150" alt="测试图片">
            <img data-src="https://via.placeholder.com/200" alt="延迟加载图片">
            <audio src="https://example.com/audio.mp3"></audio>
            <video src="https://example.com/video.mp4"></video>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(test_html, 'lxml')
        session = requests.Session()
        
        # 创建测试目录
        test_dir = Path("test_media")
        test_dir.mkdir(exist_ok=True)
        
        downloader = MediaDownloader(session, test_dir)
        
        # 注意：这里不会实际下载，因为URL是示例的
        # 在实际使用中，需要提供真实的URL
        
        print("⚠ 媒体下载器测试需要真实的URL才能完整测试")
        print("✓ 媒体下载器初始化成功")
        
        # 清理测试目录
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)
            
        return True
        
    except Exception as e:
        print(f"✗ 媒体下载器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("微信文章下载工具测试脚本")
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("单个文章下载", test_single_download),
        ("批量下载", test_batch_download), 
        ("媒体下载器", test_media_downloader)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"测试 {test_name} 时发生错误: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n=== 测试结果摘要 ===")
    
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
    
    # 总结
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n测试完成: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过!")
    else:
        print("⚠ 部分测试未通过，请检查配置和网络连接")

if __name__ == "__main__":
    main()