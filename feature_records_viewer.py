#!/usr/bin/env python3
"""
功能实现记录查看器 - Web界面
提供Web界面来查看和管理功能实现记录
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from feature_recorder import FeatureRecorder

app = Flask(__name__)
recorder = FeatureRecorder()


@app.route('/')
def index():
    """功能记录列表页面"""
    features = recorder.get_feature_list()
    
    # 统计信息
    total_features = len(features)
    completed_features = len([f for f in features if f["status"] == "completed"])
    in_progress_features = len([f for f in features if f["status"] == "in_progress"])
    
    return render_template('feature_records.html', 
                         features=features,
                         total_features=total_features,
                         completed_features=completed_features,
                         in_progress_features=in_progress_features)


@app.route('/feature/<feature_id>')
def feature_detail(feature_id):
    """功能详情页面"""
    feature_data = recorder.get_feature_details(feature_id)
    
    if not feature_data:
        return "功能记录不存在", 404
    
    # 计算时间信息
    if feature_data.get("end_time"):
        time_spent = feature_data["actual_time_spent"]
    else:
        time_spent = (int(time.time()) - feature_data["start_time"]) // 60
    
    return render_template('feature_detail.html', 
                         feature=feature_data,
                         time_spent=time_spent)


@app.route('/api/features')
def api_features():
    """API: 获取功能列表"""
    features = recorder.get_feature_list()
    return jsonify(features)


@app.route('/api/feature/<feature_id>')
def api_feature_detail(feature_id):
    """API: 获取功能详情"""
    feature_data = recorder.get_feature_details(feature_id)
    
    if not feature_data:
        return jsonify({"error": "功能记录不存在"}), 404
    
    return jsonify(feature_data)


@app.route('/api/feature/<feature_id>/markdown')
def download_markdown(feature_id):
    """下载markdown格式的报告"""
    md_file = recorder.records_dir / f"{feature_id}.md"
    
    if not md_file.exists():
        return "文件不存在", 404
    
    return send_file(md_file, as_attachment=True, 
                    download_name=f"{feature_id}.md")


@app.route('/api/feature/<feature_id>/json')
def download_json(feature_id):
    """下载JSON格式的原始数据"""
    json_file = recorder.records_dir / f"{feature_id}.json"
    
    if not json_file.exists():
        return "文件不存在", 404
    
    return send_file(json_file, as_attachment=True, 
                    download_name=f"{feature_id}.json")


@app.route('/api/start_feature', methods=['POST'])
def api_start_feature():
    """API: 开始记录新功能"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "缺少必要参数"}), 400
    
    feature_id = recorder.start_feature(
        data['name'],
        data.get('description', ''),
        data.get('priority', 'medium')
    )
    
    return jsonify({
        "feature_id": feature_id,
        "message": "功能记录已开始"
    })


@app.route('/api/add_step', methods=['POST'])
def api_add_step():
    """API: 添加实现步骤"""
    data = request.get_json()
    
    if not data or 'description' not in data:
        return jsonify({"error": "缺少必要参数"}), 400
    
    recorder.add_step(
        data['description'],
        data.get('type', 'implementation'),
        data.get('details', ''),
        data.get('code_snippet', '')
    )
    
    return jsonify({"message": "步骤已添加"})


@app.route('/api/complete_feature', methods=['POST'])
def api_complete_feature():
    """API: 完成功能记录"""
    data = request.get_json()
    
    recorder.complete_feature(
        data.get('summary', ''),
        data.get('time_spent_minutes', 0)
    )
    
    return jsonify({"message": "功能记录已完成"})


# 创建HTML模板目录和文件
def create_templates():
    """创建HTML模板文件"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # 主页面模板
    index_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>功能实现记录系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .feature-card {
            transition: transform 0.2s;
            margin-bottom: 1rem;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .status-badge {
            font-size: 0.8rem;
        }
        .priority-high { background-color: #dc3545; }
        .priority-medium { background-color: #ffc107; color: #000; }
        .priority-low { background-color: #28a745; }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <h1 class="mb-4">
                    <i class="fas fa-history"></i> 功能实现记录系统
                </h1>
                
                <!-- 统计卡片 -->
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card text-white bg-primary">
                            <div class="card-body">
                                <h5 class="card-title">{{ total_features }}</h5>
                                <p class="card-text">总功能数</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-success">
                            <div class="card-body">
                                <h5 class="card-title">{{ completed_features }}</h5>
                                <p class="card-text">已完成</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-warning">
                            <div class="card-body">
                                <h5 class="card-title">{{ in_progress_features }}</h5>
                                <p class="card-text">进行中</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 功能列表 -->
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-list"></i> 功能记录列表
                        </h5>
                    </div>
                    <div class="card-body">
                        {% if features %}
                            <div class="row">
                                {% for feature in features %}
                                <div class="col-md-6">
                                    <div class="card feature-card">
                                        <div class="card-body">
                                            <h6 class="card-title">
                                                <a href="/feature/{{ feature.id }}" class="text-decoration-none">
                                                    {{ feature.name }}
                                                </a>
                                            </h6>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <span class="badge status-badge {% if feature.status == 'completed' %}bg-success{% else %}bg-warning{% endif %}">
                                                    {{ '已完成' if feature.status == 'completed' else '进行中' }}
                                                </span>
                                                <span class="badge status-badge priority-{{ feature.priority }}">
                                                    {{ '高' if feature.priority == 'high' else '中' if feature.priority == 'medium' else '低' }}优先级
                                                </span>
                                            </div>
                                            <small class="text-muted">
                                                开始时间: {{ feature.start_time | datetime }}
                                            </small>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        {% else %}
                            <div class="text-center text-muted py-4">
                                <i class="fas fa-inbox fa-3x mb-3"></i>
                                <p>暂无功能记录</p>
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <!-- 操作按钮 -->
                <div class="mt-3 text-center">
                    <button class="btn btn-primary" onclick="startNewFeature()">
                        <i class="fas fa-plus"></i> 开始新功能记录
                    </button>
                    <a href="/api/features" class="btn btn-outline-secondary" download="features.json">
                        <i class="fas fa-download"></i> 导出JSON
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function startNewFeature() {
            const name = prompt('请输入功能名称:');
            if (name) {
                const description = prompt('请输入功能描述:');
                const priority = prompt('请输入优先级 (high/medium/low):', 'medium');
                
                fetch('/api/start_feature', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: name,
                        description: description || '',
                        priority: priority || 'medium'
                    })
                }).then(response => response.json())
                  .then(data => {
                      alert('功能记录已开始！ID: ' + data.feature_id);
                      location.reload();
                  });
            }
        }
        
        // 时间戳转换函数
        function formatTimestamp(timestamp) {
            return new Date(timestamp * 1000).toLocaleString('zh-CN');
        }
    </script>
</body>
</html>
"""
    
    # 详情页面模板
    detail_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ feature.name }} - 功能详情</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .timeline {
            position: relative;
            padding-left: 2rem;
        }
        .timeline::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #dee2e6;
        }
        .timeline-item {
            position: relative;
            margin-bottom: 1rem;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -2rem;
            top: 0.5rem;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #007bff;
        }
        .code-snippet {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 0.5rem;
            font-family: monospace;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <!-- 返回按钮 -->
                <a href="/" class="btn btn-outline-secondary mb-3">
                    <i class="fas fa-arrow-left"></i> 返回列表
                </a>
                
                <!-- 功能头部信息 -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h2 class="card-title">{{ feature.name }}</h2>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>功能ID:</strong> <code>{{ feature.id }}</code></p>
                                <p><strong>描述:</strong> {{ feature.description }}</p>
                                <p><strong>状态:</strong> 
                                    <span class="badge {% if feature.status == 'completed' %}bg-success{% else %}bg-warning{% endif %}">
                                        {{ '已完成' if feature.status == 'completed' else '进行中' }}
                                    </span>
                                </p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>优先级:</strong> 
                                    <span class="badge priority-{{ feature.priority }}">
                                        {{ '高' if feature.priority == 'high' else '中' if feature.priority == 'medium' else '低' }}
                                    </span>
                                </p>
                                <p><strong>开始时间:</strong> {{ feature.start_time_str }}</p>
                                {% if feature.end_time_str %}
                                <p><strong>结束时间:</strong> {{ feature.end_time_str }}</p>
                                <p><strong>耗时:</strong> {{ time_spent }} 分钟</p>
                                {% endif %}
                            </div>
                        </div>
                        
                        <!-- 操作按钮 -->
                        <div class="mt-3">
                            <a href="/api/feature/{{ feature.id }}/markdown" class="btn btn-primary">
                                <i class="fas fa-download"></i> 下载Markdown报告
                            </a>
                            <a href="/api/feature/{{ feature.id }}/json" class="btn btn-outline-secondary">
                                <i class="fas fa-code"></i> 下载JSON数据
                            </a>
                        </div>
                    </div>
                </div>
                
                <!-- 实现步骤 -->
                {% if feature.steps %}
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-list-ol"></i> 实现步骤</h5>
                    </div>
                    <div class="card-body">
                        <div class="timeline">
                            {% for step in feature.steps %}
                            <div class="timeline-item">
                                <h6>{{ step.description }}</h6>
                                <small class="text-muted">{{ step.timestamp_str }} - {{ step.type }}</small>
                                {% if step.details %}
                                <p class="mt-2">{{ step.details }}</p>
                                {% endif %}
                                {% if step.code_snippet %}
                                <pre class="code-snippet mt-2">{{ step.code_snippet }}</pre>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <!-- 代码变更 -->
                {% if feature.files_created or feature.files_modified %}
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-code"></i> 代码变更</h5>
                    </div>
                    <div class="card-body">
                        {% if feature.files_created %}
                        <h6>新增文件:</h6>
                        <ul>
                            {% for file in feature.files_created %}
                            <li><code>{{ file.file }}</code> - {{ file.description }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        
                        {% if feature.files_modified %}
                        <h6>修改文件:</h6>
                        <ul>
                            {% for file in feature.files_modified %}
                            <li><code>{{ file.file }}</code> - {{ file.description }}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                    </div>
                </div>
                {% endif %}
                
                <!-- 总结 -->
                {% if feature.summary %}
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-file-alt"></i> 总结</h5>
                    </div>
                    <div class="card-body">
                        <p>{{ feature.summary }}</p>
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    # 写入模板文件
    (templates_dir / "feature_records.html").write_text(index_template.strip(), encoding='utf-8')
    (templates_dir / "feature_detail.html").write_text(detail_template.strip(), encoding='utf-8')


# 自定义过滤器
@app.template_filter('datetime')
def format_datetime(timestamp):
    """时间戳格式化过滤器"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    # 创建模板文件
    create_templates()
    
    print("功能记录查看器启动中...")
    print("访问地址: http://localhost:5001")
    print("功能记录目录:", recorder.records_dir)
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5001, debug=True)