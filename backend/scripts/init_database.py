#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import create_tables, drop_tables

def main():
    """主函数"""
    print("正在初始化数据库...")
    
    try:
        # 删除现有表
        print("删除现有表...")
        drop_tables()
        
        # 创建新表
        print("创建新表...")
        create_tables()
        
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()