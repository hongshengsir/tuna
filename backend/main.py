#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tuna Backend - 微信文章下载与处理系统主入口

启动API服务器和相关的后端服务
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """主函数"""
    from src.api.app import app
    
    print("=== Tuna Backend 启动 ===")
    print("微信文章下载与处理系统")
    print("版本: 1.0.0")
    print("作者: Tuna Team")
    print("=" * 40)
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()