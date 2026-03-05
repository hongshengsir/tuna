#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理API测试脚本
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """测试健康检查"""
    print("🧪 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_user_apis():
    """测试用户管理API"""
    
    # 1. 获取用户列表
    print("1️⃣ 测试获取用户列表...")
    response = requests.get(f"{BASE_URL}/users")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"用户数量: {len(data.get('data', []))}")
    else:
        print(f"响应: {response.text}")
    print()
    
    # 2. 创建新用户
    print("2️⃣ 测试创建新用户...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "full_name": "测试用户",
        "phone": "13800138000"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"状态码: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"创建成功: {data.get('message')}")
        user_id = data['data']['id']
    else:
        print(f"响应: {response.text}")
        user_id = None
    print()
    
    if user_id:
        # 3. 获取用户详情
        print("3️⃣ 测试获取用户详情...")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"用户信息: {data['data']['username']} - {data['data']['email']}")
        else:
            print(f"响应: {response.text}")
        print()
        
        # 4. 更新用户信息
        print("4️⃣ 测试更新用户信息...")
        update_data = {
            "full_name": "更新后的测试用户",
            "phone": "13900139000"
        }
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"更新成功: {data.get('message')}")
        else:
            print(f"响应: {response.text}")
        print()
        
        # 5. 测试用户登录
        print("5️⃣ 测试用户登录...")
        login_data = {
            "username": "testuser",
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"登录成功: {data.get('message')}")
        else:
            print(f"响应: {response.text}")
        print()
        
        # 6. 删除用户
        print("6️⃣ 测试删除用户...")
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"删除成功: {data.get('message')}")
        else:
            print(f"响应: {response.text}")
        print()

def main():
    """主函数"""
    print("🚀 开始测试用户管理API...\n")
    
    try:
        test_health_check()
        test_user_apis()
        print("✅ 测试完成！")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    main()