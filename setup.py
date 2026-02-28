#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = [
        'requests',
        'beautifulsoup4', 
        'lxml',
        'markdownify',
        'python-slugify',
        'pillow',
        'click',
        'rich'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖包...")
    
    # 使用pip安装requirements.txt中的包
    requirements_file = Path(__file__).parent / 'requirements.txt'
    
    if requirements_file.exists():
        os.system(f'{sys.executable} -m pip install -r {requirements_file}')
    else:
        print("错误: 找不到requirements.txt文件")
        return False
    
    return True

def create_shortcut():
    """创建快捷方式（可选）"""
    print("\n快捷方式创建（可选）:")
    print("1. 将项目目录添加到PATH环境变量")
    print("2. 创建桌面快捷方式")
    print("3. 跳过")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == '1':
        print("请手动将以下路径添加到PATH环境变量:")
        print(str(Path(__file__).parent))
    elif choice == '2':
        print("桌面快捷方式创建功能暂未实现")
    else:
        print("跳过快捷方式创建")

def main():
    """主安装函数"""
    print("=" * 50)
    print("微信文章下载工具安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    print(f"Python版本: {sys.version}")
    
    # 检查依赖
    print("\n检查依赖...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"发现缺失的依赖包: {', '.join(missing_packages)}")
        
        install_choice = input("是否自动安装依赖? (y/n): ").strip().lower()
        if install_choice == 'y':
            if not install_dependencies():
                print("依赖安装失败，请手动安装")
                sys.exit(1)
        else:
            print("请手动安装缺失的依赖包:")
            print("pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✓ 所有依赖包都已安装")
    
    # 创建快捷方式
    create_shortcut()
    
    # 显示使用说明
    print("\n" + "=" * 50)
    print("安装完成!")
    print("=" * 50)
    print("\n使用方法:")
    print("1. 单个文章下载:")
    print("   python wechat_downloader.py --url '微信文章URL'")
    print("\n2. 批量下载:")
    print("   python batch_processor.py --file urls.txt")
    print("\n3. 交互式使用:")
    print("   python wechat_downloader.py")
    print("\n4. 运行测试:")
    print("   python test_downloader.py")
    print("\n详细说明请查看README.md文件")

if __name__ == "__main__":
    main()