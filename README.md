# Tuna - 微信文章下载与处理系统

一个完整的全栈应用，提供微信文章下载、媒体资源提取、功能记录和可视化界面。

## 项目结构

```
tuna/
├── backend/          # 后端服务（Python Flask）
│   ├── src/         # 源代码
│   ├── tests/       # 测试文件
│   ├── main.py      # 后端入口点
│   └── README.md    # 后端详细文档
├── frontend/        # 前端界面（Vue.js）
│   ├── src/         # 前端源代码
│   └── README.md    # 前端详细文档
├── requirements.txt # 项目依赖说明
└── README.md       # 项目总说明
```

## 功能特性

### 后端功能
- ✅ RESTful API接口
- ✅ 微信文章内容解析和下载
- ✅ 批量URL处理
- ✅ 多媒体资源下载
- ✅ 功能使用记录系统
- ✅ Markdown格式转换

### 前端功能
- ✅ 现代化Web界面
- ✅ 实时下载状态监控
- ✅ 批量URL上传
- ✅ 下载历史查看
- ✅ 功能记录可视化

## 快速开始

### 1. 安装依赖

```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
npm install
```

### 2. 启动服务

```bash
# 启动后端服务（终端1）
cd backend
python main.py

# 启动前端服务（终端2）
cd frontend
npm run dev
```

### 3. 访问应用

- 前端界面：http://localhost:3000
- 后端API：http://localhost:5000

## 详细文档

- [后端详细说明](./backend/README.md)
- [前端详细说明](./frontend/README.md)

## API接口

### 后端API
- `GET /api/health` - 健康检查
- `POST /api/download/single` - 单个文章下载
- `POST /api/download/batch` - 批量文章下载
- `GET /api/features` - 获取功能记录
- `POST /api/record-feature` - 记录功能使用

### 前端界面
- 主界面：文章下载和批量处理
- 历史记录：查看下载历史
- 功能记录：查看系统使用统计

## 开发

### 后端开发
```bash
cd backend
# 运行测试
python -m pytest tests/
# 代码格式化
black src/
# 代码检查
flake8 src/
```

### 前端开发
```bash
cd frontend
# 开发模式
npm run dev
# 构建生产版本
npm run build
# 代码检查
npm run lint
```

## 许可证

MIT License