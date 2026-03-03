# Tuna Backend

微信文章下载与处理系统后端服务

## 项目结构

```
backend/
├── src/                    # 源代码目录
│   ├── api/               # API接口层
│   │   └── app.py         # Flask应用主文件
│   ├── config/            # 配置文件
│   │   └── config.py      # 应用配置
│   ├── core/              # 核心业务逻辑
│   │   └── wechat_downloader.py  # 微信文章下载器
│   ├── services/          # 服务层
│   │   ├── batch_processor.py    # 批量处理器
│   │   └── media_downloader.py   # 媒体下载器
│   ├── utils/             # 工具模块
│   │   ├── file_utils.py         # 文件工具函数
│   │   └── feature_recorder.py   # 功能记录器
│   └── models/            # 数据模型（预留）
├── tests/                 # 测试文件
│   ├── test_wechat_downloader.py
│   └── test_feature_records.py
├── docs/                  # 文档（预留）
├── scripts/               # 脚本文件（预留）
├── main.py               # 应用入口点
├── requirements.txt      # 依赖包列表
└── README.md            # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行后端服务

```bash
python main.py
```

或者使用原有的启动方式：

```bash
python api_server.py
```

### 3. 访问API

服务启动后，可以通过以下地址访问：
- API文档: http://localhost:5000/
- 健康检查: http://localhost:5000/health

## 主要功能

### 微信文章下载
- 支持单个微信文章URL下载
- 支持批量URL文件下载
- 自动提取文章标题、内容、图片等信息
- 支持多种输出格式（Markdown、HTML、JSON）

### 媒体文件下载
- 自动下载文章中的图片和视频
- 支持文件重命名和去重
- 提供文件大小格式化功能

### 功能记录
- 记录每次下载操作
- 支持手动和自动记录模式
- 提供功能列表查看接口

## API接口

### 健康检查
- `GET /health` - 检查服务状态

### 文章下载
- `POST /download` - 下载单个文章
- `POST /batch-download` - 批量下载文章

### 功能记录
- `GET /features` - 获取功能记录列表
- `POST /record-feature` - 记录功能使用

## 测试

运行测试：

```bash
cd tests
python -m pytest
```

## 开发说明

### 代码规范
- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用isort进行导入排序

### 模块说明
- **core/**: 核心业务逻辑，包含微信文章下载器
- **services/**: 服务层，包含批处理和媒体下载服务
- **utils/**: 工具函数模块
- **api/**: API接口层，基于Flask框架

## 部署

### 生产环境部署

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.app:app"
```

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "main.py"]
```