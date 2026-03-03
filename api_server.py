#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章下载API服务器

提供RESTful API接口供前端调用下载功能
集成功能实现过程记录系统
"""

import os
import json
import time
import zipfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from wechat_downloader import WeChatDownloader
from pathlib import Path
import logging
import tempfile
import shutil
import glob
from feature_recorder import FeatureRecorder, record_feature

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局下载器实例
downloader = WeChatDownloader()

# 功能记录器实例
feature_recorder = FeatureRecorder()

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

@app.route('/api/download/zip/<path:directory>', methods=['GET'])
def download_zip(directory):
    """将目录打包成ZIP文件下载"""
    try:
        dir_path = Path(directory)
        
        # 验证目录是否存在
        if not dir_path.exists() or not dir_path.is_dir():
            return jsonify({
                'success': False,
                'error': '目录不存在'
            }), 404
        
        # 创建临时ZIP文件
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
            zip_filename = temp_zip.name
        
        # 创建ZIP文件
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历目录中的所有文件
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    # 计算在ZIP文件中的相对路径
                    arcname = file_path.relative_to(dir_path)
                    zipf.write(file_path, arcname)
        
        # 获取目录名作为ZIP文件名
        zip_basename = f"{dir_path.name}.zip"
        
        logger.info(f"创建ZIP文件: {zip_filename}, 包含目录: {directory}")
        
        # 发送ZIP文件
        response = send_file(
            zip_filename,
            as_attachment=True,
            download_name=zip_basename,
            mimetype='application/zip'
        )
        
        # 设置响应头，确保浏览器正确处理下载
        response.headers['Content-Disposition'] = f'attachment; filename="{zip_basename}"'
        
        # 在响应完成后删除临时文件
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(zip_filename)
                logger.info(f"清理临时ZIP文件: {zip_filename}")
            except Exception as e:
                logger.error(f"清理临时文件失败: {e}")
        
        return response
        
    except Exception as e:
        logger.error(f"ZIP文件创建失败: {directory}, 错误: {e}")
        return jsonify({
            'success': False,
            'error': 'ZIP文件创建失败'
        }), 500

@app.route('/api/download/zip/batch', methods=['POST'])
def download_batch_zip():
    """将多个目录打包成一个ZIP文件下载"""
    try:
        data = request.get_json()
        
        if not data or 'directories' not in data:
            return jsonify({
                'success': False,
                'error': '缺少目录列表参数'
            }), 400
        
        directories = data['directories']
        
        if not isinstance(directories, list) or len(directories) == 0:
            return jsonify({
                'success': False,
                'error': '目录列表不能为空'
            }), 400
        
        # 验证所有目录是否存在
        valid_dirs = []
        for directory in directories:
            dir_path = Path(directory)
            if dir_path.exists() and dir_path.is_dir():
                valid_dirs.append(dir_path)
            else:
                logger.warning(f"目录不存在或不是目录: {directory}")
        
        if len(valid_dirs) == 0:
            return jsonify({
                'success': False,
                'error': '没有有效的目录'
            }), 400
        
        # 创建临时ZIP文件
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
            zip_filename = temp_zip.name
        
        # 创建ZIP文件
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dir_path in valid_dirs:
                # 遍历目录中的所有文件
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = Path(root) / file
                        # 计算在ZIP文件中的相对路径，包含目录名
                        arcname = Path(dir_path.name) / file_path.relative_to(dir_path)
                        zipf.write(file_path, arcname)
        
        # 生成ZIP文件名
        zip_basename = f"wechat_articles_batch_{int(time.time())}.zip"
        
        logger.info(f"创建批量ZIP文件: {zip_filename}, 包含 {len(valid_dirs)} 个目录")
        
        # 发送ZIP文件
        response = send_file(
            zip_filename,
            as_attachment=True,
            download_name=zip_basename,
            mimetype='application/zip'
        )
        
        # 设置响应头
        response.headers['Content-Disposition'] = f'attachment; filename="{zip_basename}"'
        
        # 在响应完成后删除临时文件
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(zip_filename)
                logger.info(f"清理临时批量ZIP文件: {zip_filename}")
            except Exception as e:
                logger.error(f"清理临时批量文件失败: {e}")
        
        return response
        
    except Exception as e:
        logger.error(f"批量ZIP文件创建失败: {e}")
        return jsonify({
            'success': False,
            'error': '批量ZIP文件创建失败'
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

@app.route('/api/markdown/files', methods=['GET'])
def list_markdown_files():
    """获取所有markdown文件列表"""
    try:
        # 获取当前工作目录下的所有markdown文件
        current_dir = Path.cwd()
        markdown_files = []
        
        # 查找所有.md文件
        for md_file in current_dir.glob('**/*.md'):
            # 跳过node_modules等目录
            if 'node_modules' in str(md_file) or 'frontend' in str(md_file):
                continue
                
            # 获取文件信息
            file_info = {
                'name': md_file.name,
                'path': str(md_file),
                'relative_path': str(md_file.relative_to(current_dir)),
                'directory': str(md_file.parent.name),
                'size': md_file.stat().st_size,
                'modified_time': md_file.stat().st_mtime
            }
            markdown_files.append(file_info)
        
        # 按修改时间倒序排序
        markdown_files.sort(key=lambda x: x['modified_time'], reverse=True)
        
        logger.info(f"找到 {len(markdown_files)} 个markdown文件")
        
        return jsonify({
            'success': True,
            'files': markdown_files,
            'total': len(markdown_files)
        })
        
    except Exception as e:
        logger.error(f"获取markdown文件列表失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取文件列表失败'
        }), 500

@app.route('/api/markdown/read/<path:filepath>', methods=['GET'])
def read_markdown_file(filepath):
    """读取markdown文件内容"""
    try:
        file_path = Path(filepath)
        
        # 验证文件是否存在
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        # 验证文件扩展名
        if file_path.suffix.lower() != '.md':
            return jsonify({
                'success': False,
                'error': '不是markdown文件'
            }), 400
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件信息
        file_info = {
            'name': file_path.name,
            'path': str(file_path),
            'size': file_path.stat().st_size,
            'modified_time': file_path.stat().st_mtime
        }
        
        logger.info(f"读取markdown文件: {filepath}, 大小: {len(content)} 字符")
        
        return jsonify({
            'success': True,
            'content': content,
            'file_info': file_info
        })
        
    except Exception as e:
        logger.error(f"读取markdown文件失败: {filepath}, 错误: {e}")
        return jsonify({
            'success': False,
            'error': '读取文件失败'
        }), 500

@app.route('/api/markdown/directories', methods=['GET'])
def list_markdown_directories():
    """获取包含markdown文件的目录列表"""
    try:
        current_dir = Path.cwd()
        directories = {}
        
        # 查找所有包含.md文件的目录
        for md_file in current_dir.glob('**/*.md'):
            # 跳过node_modules等目录
            if 'node_modules' in str(md_file) or 'frontend' in str(md_file):
                continue
            
            dir_path = md_file.parent
            dir_name = dir_path.name
            
            if dir_name not in directories:
                # 获取目录信息
                dir_info = {
                    'name': dir_name,
                    'path': str(dir_path),
                    'file_count': 0,
                    'files': []
                }
                directories[dir_name] = dir_info
            
            # 添加文件信息
            file_info = {
                'name': md_file.name,
                'path': str(md_file),
                'size': md_file.stat().st_size,
                'modified_time': md_file.stat().st_mtime
            }
            directories[dir_name]['files'].append(file_info)
            directories[dir_name]['file_count'] += 1
        
        # 转换为列表并按文件数量排序
        directories_list = list(directories.values())
        directories_list.sort(key=lambda x: x['file_count'], reverse=True)
        
        logger.info(f"找到 {len(directories_list)} 个包含markdown文件的目录")
        
        return jsonify({
            'success': True,
            'directories': directories_list,
            'total': len(directories_list)
        })
        
    except Exception as e:
        logger.error(f"获取markdown目录列表失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取目录列表失败'
        }), 500

# ===========================================================================
# 功能记录系统API端点
# ===========================================================================

@app.route('/api/features', methods=['GET'])
def list_features():
    """获取功能记录列表"""
    try:
        features = feature_recorder.get_feature_list()
        
        return jsonify({
            'success': True,
            'features': features,
            'total': len(features)
        })
        
    except Exception as e:
        logger.error(f"获取功能记录列表失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取功能记录列表失败'
        }), 500

@app.route('/api/features/<feature_id>', methods=['GET'])
def get_feature_detail(feature_id):
    """获取功能详情"""
    try:
        feature_data = feature_recorder.get_feature_details(feature_id)
        
        if not feature_data:
            return jsonify({
                'success': False,
                'error': '功能记录不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'feature': feature_data
        })
        
    except Exception as e:
        logger.error(f"获取功能详情失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取功能详情失败'
        }), 500

@app.route('/api/features', methods=['POST'])
def start_feature():
    """开始记录新功能"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': '缺少功能名称参数'
            }), 400
        
        feature_id = feature_recorder.start_feature(
            data['name'],
            data.get('description', ''),
            data.get('priority', 'medium')
        )
        
        logger.info(f"开始记录新功能: {data['name']}, ID: {feature_id}")
        
        return jsonify({
            'success': True,
            'feature_id': feature_id,
            'message': '功能记录已开始'
        })
        
    except Exception as e:
        logger.error(f"开始功能记录失败: {e}")
        return jsonify({
            'success': False,
            'error': '开始功能记录失败'
        }), 500

@app.route('/api/features/<feature_id>/steps', methods=['POST'])
def add_feature_step(feature_id):
    """为功能添加实现步骤"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                'success': False,
                'error': '缺少步骤描述参数'
            }), 400
        
        feature_recorder.add_step(
            data['description'],
            data.get('type', 'implementation'),
            data.get('details', ''),
            data.get('code_snippet', '')
        )
        
        logger.info(f"为功能 {feature_id} 添加步骤: {data['description']}")
        
        return jsonify({
            'success': True,
            'message': '步骤已添加'
        })
        
    except Exception as e:
        logger.error(f"添加功能步骤失败: {e}")
        return jsonify({
            'success': False,
            'error': '添加功能步骤失败'
        }), 500

@app.route('/api/features/<feature_id>/complete', methods=['POST'])
def complete_feature(feature_id):
    """完成功能记录"""
    try:
        data = request.get_json() or {}
        
        feature_recorder.complete_feature(
            data.get('summary', ''),
            data.get('time_spent_minutes', 0)
        )
        
        logger.info(f"完成功能记录: {feature_id}")
        
        return jsonify({
            'success': True,
            'message': '功能记录已完成'
        })
        
    except Exception as e:
        logger.error(f"完成功能记录失败: {e}")
        return jsonify({
            'success': False,
            'error': '完成功能记录失败'
        }), 500

@app.route('/api/features/<feature_id>/markdown', methods=['GET'])
def download_feature_markdown(feature_id):
    """下载功能记录的markdown报告"""
    try:
        md_file = feature_recorder.records_dir / f"{feature_id}.md"
        
        if not md_file.exists():
            return jsonify({
                'success': False,
                'error': 'markdown文件不存在'
            }), 404
        
        return send_file(
            md_file,
            as_attachment=True,
            download_name=f"{feature_id}.md",
            mimetype='text/markdown'
        )
        
    except Exception as e:
        logger.error(f"下载markdown报告失败: {e}")
        return jsonify({
            'success': False,
            'error': '下载markdown报告失败'
        }), 500

# ===========================================================================
# 自动记录装饰器示例
# ===========================================================================

@record_feature("自动记录测试", "测试功能记录系统的自动记录功能")
def test_auto_recording():
    """测试自动记录功能的示例函数"""
    logger.info("执行自动记录测试函数")
    return "测试完成"

@app.route('/api/test/auto-record', methods=['GET'])
def test_auto_record():
    """测试自动记录功能"""
    try:
        result = test_auto_recording()
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logger.error(f"自动记录测试失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("启动微信文章下载API服务器...")
    print("API地址: http://localhost:5000")
    print("健康检查: http://localhost:5000/api/health")
    print("功能记录API: http://localhost:5000/api/features")
    
    app.run(host='0.0.0.0', port=5000, debug=True)