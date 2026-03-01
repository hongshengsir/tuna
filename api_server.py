#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章下载API服务器

提供RESTful API接口供前端调用下载功能
"""

import os
import json
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from wechat_downloader import WeChatDownloader
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局下载器实例
downloader = WeChatDownloader()

# 存储下载任务状态
download_tasks = {}

class DownloadTask:
    """下载任务类"""
    
    def __init__(self, task_id, url):
        self.task_id = task_id
        self.url = url
        self.status = 'pending'  # pending, downloading, completed, error
        self.progress = 0
        self.error_message = None
        self.result = None
        self.start_time = None
        self.end_time = None
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'task_id': self.task_id,
            'url': self.url,
            'status': self.status,
            'progress': self.progress,
            'error_message': self.error_message,
            'result': self.result,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'API服务器运行正常',
        'timestamp': time.time()
    })

@app.route('/api/download/single', methods=['POST'])
def download_single():
    """单个文章下载接口"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': '缺少URL参数'
            }), 400
        
        url = data['url'].strip()
        
        # 验证URL格式
        if not is_valid_wechat_url(url):
            return jsonify({
                'success': False,
                'error': '无效的微信文章链接'
            }), 400
        
        # 创建下载任务
        task_id = str(int(time.time() * 1000))
        task = DownloadTask(task_id, url)
        download_tasks[task_id] = task
        
        # 开始下载（异步执行）
        task.status = 'downloading'
        task.start_time = time.time()
        
        try:
            # 执行下载
            result = downloader.download_article(url)
            
            task.status = 'completed'
            task.progress = 100
            task.result = result
            task.end_time = time.time()
            
            logger.info(f"下载任务完成: {task_id}")
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'result': result
            })
            
        except Exception as e:
            task.status = 'error'
            task.error_message = str(e)
            task.end_time = time.time()
            
            logger.error(f"下载任务失败: {task_id}, 错误: {e}")
            
            return jsonify({
                'success': False,
                'task_id': task_id,
                'error': str(e)
            }), 500
            
    except Exception as e:
        logger.error(f"API调用异常: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/download/batch', methods=['POST'])
def download_batch():
    """批量下载接口"""
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'success': False,
                'error': '缺少URL列表参数'
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({
                'success': False,
                'error': 'URL列表不能为空'
            }), 400
        
        # 验证URL格式
        valid_urls = []
        for url in urls:
            url = url.strip()
            if url and is_valid_wechat_url(url):
                valid_urls.append(url)
        
        if len(valid_urls) == 0:
            return jsonify({
                'success': False,
                'error': '没有有效的微信文章链接'
            }), 400
        
        # 创建批量下载任务
        batch_id = str(int(time.time() * 1000))
        batch_tasks = []
        
        for url in valid_urls:
            task_id = f"{batch_id}_{len(batch_tasks)}"
            task = DownloadTask(task_id, url)
            download_tasks[task_id] = task
            batch_tasks.append(task)
        
        # 开始批量下载（简化实现，实际应该异步执行）
        results = []
        total = len(batch_tasks)
        
        for i, task in enumerate(batch_tasks):
            task.status = 'downloading'
            task.start_time = time.time()
            
            try:
                result = downloader.download_article(task.url)
                task.status = 'completed'
                task.progress = 100
                task.result = result
                task.end_time = time.time()
                results.append(result)
                
                # 更新进度
                progress = int((i + 1) / total * 100)
                
            except Exception as e:
                task.status = 'error'
                task.error_message = str(e)
                task.end_time = time.time()
                results.append({'error': str(e), 'url': task.url})
        
        logger.info(f"批量下载完成: {batch_id}, 成功: {len([r for r in results if 'error' not in r])}/{total}")
        
        return jsonify({
            'success': True,
            'batch_id': batch_id,
            'total': total,
            'completed': len([r for r in results if 'error' not in r]),
            'failed': len([r for r in results if 'error' in r]),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"批量下载API异常: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    if task_id not in download_tasks:
        return jsonify({
            'success': False,
            'error': '任务不存在'
        }), 404
    
    task = download_tasks[task_id]
    return jsonify({
        'success': True,
        'task': task.to_dict()
    })

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """列出所有任务"""
    tasks = [task.to_dict() for task in download_tasks.values()]
    return jsonify({
        'success': True,
        'tasks': tasks,
        'total': len(tasks)
    })

@app.route('/api/files/<path:filename>', methods=['GET'])
def download_file(filename):
    """下载文件接口"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return send_file(str(file_path))
        
    except Exception as e:
        logger.error(f"文件下载失败: {filename}, 错误: {e}")
        return jsonify({
            'success': False,
            'error': '文件下载失败'
        }), 500

def is_valid_wechat_url(url):
    """验证微信文章链接格式"""
    wechat_patterns = [
        r'^https?://mp\.weixin\.qq\.com/s/[\w-]+',
        r'^https?://mp\.weixin\.qq\.com/s\?',
        r'^https?://mp\.weixin\.qq\.com/s/.*',
        r'^https?://mp\.weixin\.qq\.com/.*',
        r'^https?://.*weixin.*',
    ]
    
    import re
    return any(re.match(pattern, url, re.IGNORECASE) for pattern in wechat_patterns)

if __name__ == '__main__':
    print("启动微信文章下载API服务器...")
    print("API地址: http://localhost:5000")
    print("健康检查: http://localhost:5000/api/health")
    
    app.run(host='0.0.0.0', port=5000, debug=True)