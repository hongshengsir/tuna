#!/usr/bin/env python3
"""
功能实现过程记录模块
自动记录每次功能实现的详细过程，并保存为markdown文件
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import inspect


class FeatureRecorder:
    """功能实现过程记录器"""
    
    def __init__(self, records_dir: str = "feature_records"):
        self.records_dir = Path(records_dir)
        self.records_dir.mkdir(exist_ok=True)
        self.current_feature = None
        self.feature_data = {}
    
    def start_feature(self, feature_name: str, description: str, priority: str = "medium") -> str:
        """开始记录一个新功能实现过程"""
        
        # 生成唯一的功能ID
        timestamp = int(time.time())
        feature_id = f"{timestamp}_{feature_name.replace(' ', '_').lower()}"
        
        # 初始化功能数据
        self.current_feature = feature_id
        self.feature_data = {
            "id": feature_id,
            "name": feature_name,
            "description": description,
            "priority": priority,
            "start_time": timestamp,
            "start_time_str": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "status": "in_progress",
            "steps": [],
            "code_changes": [],
            "files_created": [],
            "files_modified": [],
            "dependencies_added": [],
            "tests_performed": [],
            "issues_encountered": [],
            "screenshots": [],
            "related_features": [],
            "estimated_complexity": "",
            "actual_time_spent": 0
        }
        
        # 创建初始记录文件
        self._save_feature_record()
        
        return feature_id
    
    def add_step(self, step_description: str, step_type: str = "implementation", 
                 details: str = "", code_snippet: str = "") -> None:
        """添加一个实现步骤"""
        
        if not self.current_feature:
            return
        
        step = {
            "timestamp": int(time.time()),
            "timestamp_str": datetime.now().strftime('%H:%M:%S'),
            "description": step_description,
            "type": step_type,
            "details": details,
            "code_snippet": code_snippet
        }
        
        self.feature_data["steps"].append(step)
        self._save_feature_record()
    
    def log_code_change(self, file_path: str, change_type: str, 
                       description: str, lines_added: int = 0, 
                       lines_removed: int = 0) -> None:
        """记录代码变更"""
        
        if not self.current_feature:
            return
        
        change = {
            "file": file_path,
            "type": change_type,  # created, modified, deleted
            "description": description,
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "timestamp": int(time.time())
        }
        
        if change_type == "created":
            self.feature_data["files_created"].append(change)
        elif change_type == "modified":
            self.feature_data["files_modified"].append(change)
        
        self._save_feature_record()
    
    def log_dependency(self, package_name: str, version: str = "", 
                      purpose: str = "") -> None:
        """记录依赖添加"""
        
        if not self.current_feature:
            return
        
        dependency = {
            "package": package_name,
            "version": version,
            "purpose": purpose,
            "timestamp": int(time.time())
        }
        
        self.feature_data["dependencies_added"].append(dependency)
        self._save_feature_record()
    
    def log_test(self, test_description: str, result: str, 
                details: str = "") -> None:
        """记录测试执行"""
        
        if not self.current_feature:
            return
        
        test = {
            "description": test_description,
            "result": result,  # passed, failed, skipped
            "details": details,
            "timestamp": int(time.time())
        }
        
        self.feature_data["tests_performed"].append(test)
        self._save_feature_record()
    
    def log_issue(self, issue_description: str, severity: str = "low", 
                 solution: str = "", resolved: bool = False) -> None:
        """记录遇到的问题"""
        
        if not self.current_feature:
            return
        
        issue = {
            "description": issue_description,
            "severity": severity,  # low, medium, high, critical
            "solution": solution,
            "resolved": resolved,
            "timestamp": int(time.time())
        }
        
        self.feature_data["issues_encountered"].append(issue)
        self._save_feature_record()
    
    def complete_feature(self, summary: str = "", 
                        time_spent_minutes: int = 0) -> None:
        """完成功能实现记录"""
        
        if not self.current_feature:
            return
        
        self.feature_data["status"] = "completed"
        self.feature_data["end_time"] = int(time.time())
        self.feature_data["end_time_str"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.feature_data["summary"] = summary
        self.feature_data["actual_time_spent"] = time_spent_minutes
        
        # 计算实际花费时间
        if time_spent_minutes == 0:
            start_time = self.feature_data["start_time"]
            end_time = self.feature_data["end_time"]
            self.feature_data["actual_time_spent"] = (end_time - start_time) // 60
        
        self._save_feature_record()
        self._generate_markdown_report()
        
        # 重置当前功能
        self.current_feature = None
    
    def _save_feature_record(self) -> None:
        """保存功能记录到JSON文件"""
        
        if not self.current_feature:
            return
        
        record_file = self.records_dir / f"{self.current_feature}.json"
        
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(self.feature_data, f, ensure_ascii=False, indent=2)
    
    def _generate_markdown_report(self) -> None:
        """生成markdown格式的报告"""
        
        if not self.current_feature:
            return
        
        md_file = self.records_dir / f"{self.current_feature}.md"
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(self._format_markdown())
    
    def _format_markdown(self) -> str:
        """格式化markdown报告"""
        
        data = self.feature_data
        
        markdown = f"""# {data['name']}

**功能ID**: `{data['id']}`  
**优先级**: {data['priority']}  
**状态**: {data['status']}  
**开始时间**: {data['start_time_str']}  
**结束时间**: {data.get('end_time_str', '进行中')}  
**实际耗时**: {data.get('actual_time_spent', 0)} 分钟

## 功能描述

{data['description']}

## 实现过程

"""
        
        # 添加实现步骤
        if data["steps"]:
            markdown += "### 实现步骤\n\n"
            for i, step in enumerate(data["steps"], 1):
                markdown += f"**{i}. {step['timestamp_str']} - {step['description']}**  \n"
                if step["details"]:
                    markdown += f"   *详情*: {step['details']}  \n"
                if step["code_snippet"]:
                    markdown += f"\n```python\n{step['code_snippet']}\n```\n\n"
        
        # 添加代码变更
        if data["files_created"] or data["files_modified"]:
            markdown += "### 代码变更\n\n"
            
            if data["files_created"]:
                markdown += "#### 新增文件\n\n"
                for file in data["files_created"]:
                    markdown += f"- **{file['file']}** - {file['description']}  \n"
            
            if data["files_modified"]:
                markdown += "#### 修改文件\n\n"
                for file in data["files_modified"]:
                    markdown += f"- **{file['file']}** - {file['description']}  \n"
        
        # 添加依赖信息
        if data["dependencies_added"]:
            markdown += "### 依赖添加\n\n"
            for dep in data["dependencies_added"]:
                markdown += f"- **{dep['package']}**"
                if dep["version"]:
                    markdown += f" ({dep['version']})"
                if dep["purpose"]:
                    markdown += f" - {dep['purpose']}"
                markdown += "\n"
        
        # 添加测试信息
        if data["tests_performed"]:
            markdown += "### 测试执行\n\n"
            for test in data["tests_performed"]:
                status_emoji = "✅" if test["result"] == "passed" else "❌" if test["result"] == "failed" else "⚠️"
                markdown += f"- {status_emoji} **{test['description']}** - {test['result']}  \n"
                if test["details"]:
                    markdown += f"  *详情*: {test['details']}  \n"
        
        # 添加问题记录
        if data["issues_encountered"]:
            markdown += "### 问题与解决\n\n"
            for issue in data["issues_encountered"]:
                resolved_emoji = "✅" if issue["resolved"] else "❌"
                markdown += f"- {resolved_emoji} **[{issue['severity'].upper()}]** {issue['description']}  \n"
                if issue["solution"]:
                    markdown += f"  *解决方案*: {issue['solution']}  \n"
        
        # 添加总结
        if data.get("summary"):
            markdown += f"## 总结\n\n{data['summary']}\n\n"
        
        markdown += f"---\n*记录生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        return markdown
    
    def get_feature_list(self) -> List[Dict]:
        """获取所有功能记录列表"""
        
        features = []
        for json_file in self.records_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    feature_data = json.load(f)
                    features.append({
                        "id": feature_data["id"],
                        "name": feature_data["name"],
                        "status": feature_data["status"],
                        "start_time": feature_data["start_time"],
                        "priority": feature_data["priority"]
                    })
            except:
                continue
        
        # 按时间倒序排序
        features.sort(key=lambda x: x["start_time"], reverse=True)
        return features
    
    def get_feature_details(self, feature_id: str) -> Optional[Dict]:
        """获取特定功能的详细信息"""
        
        json_file = self.records_dir / f"{feature_id}.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None


# 全局记录器实例
_recorder = None

def get_recorder() -> FeatureRecorder:
    """获取全局记录器实例"""
    global _recorder
    if _recorder is None:
        _recorder = FeatureRecorder()
    return _recorder


def record_feature(feature_name: str, description: str, priority: str = "medium"):
    """装饰器：自动记录函数执行过程"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            recorder = get_recorder()
            feature_id = recorder.start_feature(feature_name, description, priority)
            
            # 记录函数调用
            recorder.add_step(f"执行函数: {func.__name__}", "function_call", 
                            f"参数: {args}, {kwargs}")
            
            try:
                result = func(*args, **kwargs)
                recorder.add_step("函数执行成功", "completion", "函数返回正常")
                recorder.complete_feature(f"函数 {func.__name__} 执行完成")
                return result
            except Exception as e:
                recorder.log_issue(f"函数执行失败: {str(e)}", "high", "", False)
                recorder.complete_feature(f"函数 {func.__name__} 执行失败")
                raise
        
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试功能
    recorder = FeatureRecorder()
    
    # 开始记录一个功能
    feature_id = recorder.start_feature(
        "测试功能记录",
        "这是一个测试功能，用于验证功能记录系统的工作情况",
        "low"
    )
    
    # 添加一些步骤
    recorder.add_step("初始化设置", "setup", "配置基础环境")
    recorder.add_step("实现核心逻辑", "implementation", "编写主要功能代码")
    recorder.log_code_change("test.py", "created", "创建测试文件", 50, 0)
    recorder.log_dependency("requests", "2.28.0", "HTTP请求处理")
    recorder.log_test("功能测试", "passed", "所有测试用例通过")
    recorder.log_issue("遇到一个小的兼容性问题", "low", "更新依赖版本", True)
    
    # 完成功能
    recorder.complete_feature("测试功能顺利完成", 5)
    
    print(f"功能记录完成！文件保存在: {recorder.records_dir}")