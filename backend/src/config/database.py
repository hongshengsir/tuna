#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库配置模块 - 使用PyMySQL连接
"""

import os
import pymysql
from pymysql import cursors

# 数据库配置
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'database': os.getenv('DB_NAME', 'wechat_downloader'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'pool_name': 'wechat_pool',
    'pool_size': 5
}

# 创建数据库连接
def get_db():
    """获取数据库连接"""
    # 移除连接池相关配置
    db_config = {k: v for k, v in DATABASE_CONFIG.items() if k not in ['pool_name', 'pool_size']}
    return pymysql.connect(**db_config)

def create_tables():
    """创建所有数据表"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                phone VARCHAR(20),
                avatar VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                is_superuser BOOLEAN DEFAULT FALSE,
                last_login TIMESTAMP NULL,
                permissions JSON,
                settings JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # 创建下载记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS download_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                url VARCHAR(500) NOT NULL,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(100),
                download_status VARCHAR(20) DEFAULT 'pending',
                markdown_file VARCHAR(500),
                media_count INT DEFAULT 0,
                file_size BIGINT DEFAULT 0,
                download_time TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_user_id (user_id),
                INDEX idx_url (url),
                INDEX idx_status (download_status),
                INDEX idx_created_at (created_at)
            )
        """)
        
        conn.commit()
        print("✅ 所有数据表创建成功")
        
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def drop_tables():
    """删除用户表"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        print("✅ 用户表删除成功")
        
    except Exception as e:
        print(f"❌ 删除表失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()