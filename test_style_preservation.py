#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式保留测试脚本
测试优化后的markdown转换器是否能保留微信文章的原有样式和格式
"""

import os
import sys
from bs4 import BeautifulSoup
from markdown_converter import MarkdownConverter

def test_style_preservation():
    """测试样式保留功能"""
    print("=== 样式保留测试 ===")
    
    # 创建包含各种样式的测试HTML
    test_html = """
    <div class="rich_media_content" id="js_content">
        <h1 style="color: #333; font-size: 24px;">测试标题 - 样式保留测试</h1>
        
        <p style="color: #666; font-size: 16px; line-height: 1.6;">
            这是一个<strong>加粗</strong>的文本，<em>斜体</em>文本，<u>下划线</u>文本，
            <s>删除线</s>文本，<sup>上标</sup>和<sub>下标</sub>文本。
        </p>
        
        <p>普通段落文本，包含<code>内联代码</code>和<span style="color: red;">红色文本</span>。</p>
        
        <blockquote style="border-left: 3px solid #ccc; padding-left: 10px; margin-left: 0;">
            这是一个引用块，应该保留其特殊格式。
        </blockquote>
        
        <ul style="list-style-type: disc; margin-left: 20px;">
            <li>无序列表项1</li>
            <li>无序列表项2</li>
            <li>无序列表项3</li>
        </ul>
        
        <ol style="list-style-type: decimal; margin-left: 20px;">
            <li>有序列表项1</li>
            <li>有序列表项2</li>
            <li>有序列表项3</li>
        </ol>
        
        <table style="border-collapse: collapse; width: 100%;">
            <tr>
                <th style="border: 1px solid #ccc; padding: 8px;">表头1</th>
                <th style="border: 1px solid #ccc; padding: 8px;">表头2</th>
            </tr>
            <tr>
                <td style="border: 1px solid #ccc; padding: 8px;">单元格1</td>
                <td style="border: 1px solid #ccc; padding: 8px;">单元格2</td>
            </tr>
        </table>
        
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 4px;">
            <code class="language-python">
# 代码块示例
def hello_world():
    print("Hello, World!")
    return True
            </code>
        </pre>
        
        <p>包含特殊字符的文本：&amp; &lt; &gt; &quot; &apos;</p>
        
        <div style="text-align: center;">
            <p>居中对齐的文本</p>
        </div>
        
        <p>包含<span class="bold-text">类名加粗</span>和<span class="italic-text">类名斜体</span>的文本。</p>
    </div>
    """
    
    # 创建转换器实例
    converter = MarkdownConverter()
    
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(test_html, 'html.parser')
    
    # 转换HTML到Markdown
    markdown_content = converter.convert_to_markdown(soup, {}, {'title': '样式保留测试文章'})
    
    # 保存测试结果
    output_file = "style_preservation_test.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✓ 测试文章已生成: {output_file}")
    
    # 分析转换结果
    print("\n=== 样式保留分析 ===")
    
    # 检查关键样式是否保留
    checks = [
        ("加粗文本", "**加粗**", "加粗样式"),
        ("斜体文本", "*斜体*", "斜体样式"),
        ("下划线文本", "<u>下划线</u>", "下划线样式"),
        ("删除线文本", "~~删除线~~", "删除线样式"),
        ("引用块", "> ", "引用格式"),
        ("无序列表", "- ", "无序列表格式"),
        ("有序列表", "1. ", "有序列表格式"),
        ("代码块", "```", "代码块格式"),
        ("表格", "| ", "表格格式"),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, marker, description in checks:
        if marker in markdown_content:
            print(f"✓ {description} 保留成功")
            passed += 1
        else:
            print(f"✗ {description} 未保留")
    
    # 检查特殊字符处理
    special_chars = ["&amp;", "&lt;", "&gt;", "&quot;", "&apos;"]
    for char in special_chars:
        if char not in markdown_content:
            print(f"✓ 特殊字符 {char} 已正确处理")
        else:
            print(f"✗ 特殊字符 {char} 未正确处理")
    
    print(f"\n=== 测试结果 ===")
    print(f"样式保留成功率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    # 显示部分转换结果
    print("\n=== 转换结果预览 ===")
    lines = markdown_content.split('\n')
    for i, line in enumerate(lines[:20]):
        print(f"{i+1:2d}: {line}")
    
    if len(lines) > 20:
        print("... (更多内容)")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = test_style_preservation()
        if success:
            print("\n🎉 所有样式保留测试通过!")
        else:
            print("\n⚠ 部分样式保留测试未通过，需要进一步优化")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()