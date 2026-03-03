#!/usr/bin/env python3
"""
功能记录系统使用示例
演示如何自动记录功能实现过程
"""

import time
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.src.utils.feature_recorder import FeatureRecorder, record_feature

# 创建记录器实例
recorder = FeatureRecorder()


def example_manual_recording():
    """手动记录功能实现过程的示例"""
    
    # 开始记录一个新功能
    feature_id = recorder.start_feature(
        "手动记录示例功能",
        "演示如何手动记录功能实现过程",
        "medium"
    )
    
    print(f"开始记录功能: {feature_id}")
    
    # 添加实现步骤
    recorder.add_step("初始化设置", "setup", "配置基础环境和依赖")
    time.sleep(1)
    
    recorder.add_step("实现核心逻辑", "implementation", "编写主要功能代码")
    recorder.log_code_change("example.py", "created", "创建示例文件", 30, 0)
    time.sleep(2)
    
    recorder.add_step("添加测试用例", "testing", "编写单元测试")
    recorder.log_test("功能测试", "passed", "所有测试用例通过")
    time.sleep(1)
    
    recorder.add_step("优化性能", "optimization", "优化代码性能")
    recorder.log_code_change("example.py", "modified", "优化算法实现", 5, 3)
    
    # 记录遇到的问题和解决方案
    recorder.log_issue("遇到兼容性问题", "medium", "更新依赖版本", True)
    
    # 完成功能记录
    recorder.complete_feature("手动记录示例功能顺利完成", 5)
    
    print(f"功能记录完成！查看文件: {recorder.records_dir}")


@record_feature("自动记录示例功能", "演示使用装饰器自动记录功能实现过程")
def example_auto_recording():
    """使用装饰器自动记录功能实现过程的示例"""
    
    # 这些步骤会被自动记录
    print("执行自动记录示例功能...")
    
    # 模拟一些工作
    time.sleep(1)
    print("步骤1: 初始化完成")
    
    time.sleep(2)
    print("步骤2: 核心逻辑实现完成")
    
    time.sleep(1)
    print("步骤3: 测试验证完成")
    
    return "自动记录示例功能执行成功"


def example_integration_with_api():
    """与API服务器集成的示例"""
    
    # 开始记录API相关功能
    feature_id = recorder.start_feature(
        "API服务器集成测试",
        "测试功能记录系统与API服务器的集成",
        "high"
    )
    
    print(f"开始API集成测试: {feature_id}")
    
    # 模拟API调用步骤
    recorder.add_step("启动API服务器", "setup", "启动本地开发服务器")
    
    recorder.add_step("测试健康检查接口", "testing", "验证API服务器状态")
    recorder.log_test("健康检查API", "passed", "服务器响应正常")
    
    recorder.add_step("测试功能记录API", "testing", "验证功能记录相关接口")
    recorder.log_test("功能记录API", "passed", "所有接口工作正常")
    
    recorder.add_step("测试自动记录功能", "testing", "验证装饰器自动记录")
    
    # 完成记录
    recorder.complete_feature("API集成测试顺利完成", 3)
    
    print("API集成测试完成！")


def list_all_features():
    """列出所有功能记录"""
    
    features = recorder.get_feature_list()
    
    print("\n=== 所有功能记录 ===")
    print(f"总记录数: {len(features)}")
    
    for feature in features:
        status_emoji = "✅" if feature["status"] == "completed" else "🔄"
        priority_color = {
            "high": "🔴",
            "medium": "🟡", 
            "low": "🟢"
        }
        
        print(f"{status_emoji} {priority_color[feature['priority']]} {feature['name']}")
        print(f"   ID: {feature['id']}")
        print(f"   状态: {feature['status']}")
        print(f"   优先级: {feature['priority']}")
        print()


def main():
    """主函数"""
    
    print("=== 功能记录系统使用示例 ===\n")
    
    # 1. 手动记录示例
    print("1. 手动记录示例:")
    example_manual_recording()
    print()
    
    # 2. 自动记录示例
    print("2. 自动记录示例:")
    try:
        result = example_auto_recording()
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    print()
    
    # 3. API集成示例
    print("3. API集成示例:")
    example_integration_with_api()
    print()
    
    # 4. 列出所有功能记录
    list_all_features()
    
    print("=== 示例完成 ===")
    print(f"功能记录文件保存在: {recorder.records_dir}")
    print("可以使用以下方式查看记录:")
    print("1. 直接查看feature_records目录下的.md文件")
    print("2. 启动功能记录查看器: python feature_records_viewer.py")
    print("3. 通过API接口访问: http://localhost:5000/api/features")


if __name__ == "__main__":
    main()