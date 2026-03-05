#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据库连接
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """测试数据库连接"""
    configs = [
        {'password': ''},      # 空密码
        {'password': 'root'},  # root密码
        {'password': '123456'}, # 常见密码
        {'password': 'password'} # 常见密码
    ]
    
    base_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root'
    }
    
    for config in configs:
        try:
            test_config = base_config.copy()
            test_config.update(config)
            
            print(f"尝试连接: user=root, password={config['password']}")
            
            # 先尝试不指定数据库连接
            connection = mysql.connector.connect(**test_config)
            if connection.is_connected():
                print("✅ 连接到MySQL服务器成功!")
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"MySQL版本: {version[0]}")
                
                # 检查数据库是否存在
                cursor.execute("SHOW DATABASES LIKE 'wechat_downloader'")
                db_exists = cursor.fetchone()
                
                if not db_exists:
                    print("⚠️ 数据库wechat_downloader不存在，正在创建...")
                    cursor.execute("CREATE DATABASE wechat_downloader CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    print("✅ 数据库wechat_downloader创建成功")
                else:
                    print("✅ 数据库wechat_downloader已存在")
                
                cursor.close()
                connection.close()
                return config['password']
                
        except Error as e:
            print(f"❌ 连接失败: {e}")
    
    return None

if __name__ == "__main__":
    print("正在测试数据库连接...")
    password = test_connection()
    if password:
        print(f"\n✅ 成功连接到数据库，密码为: {password}")
    else:
        print("\n❌ 无法连接到数据库，请检查MySQL服务状态和密码")