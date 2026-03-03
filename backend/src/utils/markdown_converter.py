#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转换器 - 将HTML内容转换为格式化的Markdown
"""

import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from typing import Dict, List

class MarkdownConverter:
    """Markdown转换器"""
    
    def __init__(self, code_formatting: bool = True):
        self.code_formatting = code_formatting
        
        # 配置markdownify选项 - 优化以保留更多样式
        self.md_options = {
            'heading_style': 'atx',
            'bullets': '-',
            'strong_em_symbol': '*',
            'sub_symbol': '~',
            'keep_inline_images_in': [],
            'convert': ['p', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                       'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'table',
                       'thead', 'tbody', 'tr', 'th', 'td', 'img', 'a', 'strong',
                       'em', 'br', 'hr', 'u', 's', 'sup', 'sub'],
            'autolinks': True,
            'default_title': False,
            'escape_asterisks': False,
            'escape_underscores': False,
            'keep_inline_styles': ['color', 'font-weight', 'font-style', 'text-decoration'],
            'wrap': False
        }
    
    def convert_to_markdown(self, soup: BeautifulSoup, media_mapping: Dict[str, str], 
                           article_info: Dict) -> str:
        """将HTML转换为Markdown"""
        
        # 获取文章主要内容
        content_elem = self._extract_main_content(soup)
        
        if not content_elem:
            # 如果没有找到主要内容，使用整个body
            content_elem = soup.find('body') or soup
        
        # 预处理HTML
        self._preprocess_html(content_elem, media_mapping)
        
        # 转换为Markdown
        markdown_content = md(str(content_elem), **self.md_options)
        
        # 后处理Markdown
        markdown_content = self._postprocess_markdown(markdown_content)
        
        # 添加文章元信息
        markdown_content = self._add_article_metadata(markdown_content, article_info)
        
        return markdown_content
    
    def _extract_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """提取文章主要内容"""
        # 微信文章常见的内容区域选择器
        content_selectors = [
            'div.rich_media_content',
            'article',
            'div.article-content',
            'div.content',
            'div.post-content',
            'div.entry-content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                return content_elem
        
        # 如果没有找到特定区域，尝试其他方法
        # 查找包含大量文本的div
        divs = soup.find_all('div')
        max_text_length = 0
        best_div = None
        
        for div in divs:
            text_length = len(div.get_text(strip=True))
            if text_length > max_text_length and text_length > 100:
                max_text_length = text_length
                best_div = div
        
        return best_div
    
    def _preprocess_html(self, element: BeautifulSoup, media_mapping: Dict[str, str]):
        """预处理HTML元素"""
        
        # 替换图片链接
        for img in element.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and src in media_mapping:
                img['src'] = media_mapping[src]
            elif src and src.startswith('data:'):
                # 移除base64编码的图片
                img.decompose()
            
            # 保留图片的alt文本和样式信息
            if not img.get('alt') and img.get('title'):
                img['alt'] = img.get('title')
        
        # 处理音频和视频链接
        for audio in element.find_all('audio'):
            src = audio.get('src')
            if src and src in media_mapping:
                audio['src'] = media_mapping[src]
        
        for video in element.find_all('video'):
            src = video.get('src')
            if src and src in media_mapping:
                video['src'] = media_mapping[src]
        
        # 保留重要的样式信息
        self._preserve_important_styles(element)
        
        # 移除广告和无关元素
        self._remove_unwanted_elements(element)
        
        # 格式化代码块
        if self.code_formatting:
            self._format_code_blocks(element)
    
    def _preserve_important_styles(self, element: BeautifulSoup):
        """保留重要的样式信息"""
        # 保留重要的内联样式
        for tag in element.find_all(['span', 'div', 'p', 'strong', 'em', 'u', 's']):
            style = tag.get('style', '')
            if style:
                # 保留重要的样式属性
                important_styles = ['color', 'font-weight', 'font-style', 'text-decoration', 'background-color']
                preserved_styles = []
                
                for style_attr in style.split(';'):
                    if ':' in style_attr:
                        prop, value = style_attr.split(':', 1)
                        prop = prop.strip()
                        value = value.strip()
                        if prop in important_styles:
                            preserved_styles.append(f"{prop}:{value}")
                
                if preserved_styles:
                    tag['style'] = '; '.join(preserved_styles)
        
        # 保留重要的类名
        for tag in element.find_all():
            class_list = tag.get('class', [])
            if class_list:
                # 保留与样式相关的类名
                style_classes = [cls for cls in class_list if any(keyword in cls for keyword in 
                    ['bold', 'italic', 'underline', 'color', 'font', 'text', 'align', 'center', 'left', 'right'])]
                if style_classes:
                    tag['class'] = style_classes

    def _remove_unwanted_elements(self, element: BeautifulSoup):
        """移除不需要的元素"""
        # 移除script和style标签
        for tag in element.find_all(['script', 'style']):
            tag.decompose()
        
        # 移除广告相关元素
        ad_selectors = [
            '.ad', '.ads', '.advertisement',
            '.sponsor', '.promo', '.banner'
        ]
        
        for selector in ad_selectors:
            for ad in element.select(selector):
                ad.decompose()
        
        # 移除空元素
        for tag in element.find_all():
            if not tag.get_text(strip=True) and not tag.find_all():
                tag.decompose()
    
    def _format_code_blocks(self, element: BeautifulSoup):
        """格式化代码块"""
        for pre in element.find_all('pre'):
            code = pre.find('code')
            if code:
                # 检测代码语言
                language = self._detect_code_language(code.get_text())
                if language:
                    # 添加语言标记
                    code['class'] = code.get('class', []) + [f'language-{language}']
    
    def _detect_code_language(self, code_text: str) -> str:
        """检测代码语言"""
        code_text = code_text.strip()
        
        # 简单的语言检测规则
        language_patterns = {
            'python': [r'^import\s+\w+', r'^def\s+\w+', r'^class\s+\w+', r'print\('],
            'javascript': [r'function\s+\w+', r'const\s+\w+', r'let\s+\w+', r'console\.log'],
            'java': [r'public\s+class', r'import\s+java', r'System\.out\.print'],
            'cpp': [r'#include', r'using\s+namespace', r'std::'],
            'html': [r'<!DOCTYPE html>', r'<html', r'<head', r'<body'],
            'css': [r'\.[\w-]+\s*{', r'#[\w-]+\s*{', r'@media'],
            'bash': [r'^#!/bin/bash', r'echo\s+', r'cd\s+', r'ls\s+']
        }
        
        for lang, patterns in language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code_text, re.IGNORECASE | re.MULTILINE):
                    return lang
        
        return ''
    
    def _postprocess_markdown(self, markdown_content: str) -> str:
        """后处理Markdown内容"""
        
        # 修复图片链接格式
        markdown_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', self._fix_image_links, markdown_content)
        
        # 修复代码块格式
        markdown_content = self._fix_code_blocks(markdown_content)
        
        # 修复表格格式
        markdown_content = self._fix_tables(markdown_content)
        
        # 修复列表格式
        markdown_content = self._fix_lists(markdown_content)
        
        # 修复引用格式
        markdown_content = self._fix_quotes(markdown_content)
        
        # 修复标题格式
        markdown_content = self._fix_headings(markdown_content)
        
        # 移除多余的空行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # 修复中文标点符号周围的空格
        markdown_content = re.sub(r'([。，；：！？])\s+', '\1', markdown_content)
        
        # 保留重要的换行和段落结构
        markdown_content = self._preserve_paragraph_structure(markdown_content)
        
        return markdown_content.strip()
    
    def _fix_lists(self, markdown_content: str) -> str:
        """修复列表格式"""
        # 确保列表项有正确的缩进
        lines = markdown_content.split('\n')
        result_lines = []
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            
            # 检测列表项
            if stripped.startswith(('-', '*', '+', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                if not in_list:
                    in_list = True
                    # 确保列表前有空行
                    if result_lines and result_lines[-1].strip():
                        result_lines.append('')
                
                # 确保列表项有正确的格式
                if stripped.startswith(('-', '*', '+')):
                    # 无序列表
                    if not stripped.startswith('- '):
                        line = line.replace(stripped[0], '-', 1)
                        if not stripped.startswith('- '):
                            line = line.replace(stripped[0] + ' ', '- ', 1)
                else:
                    # 有序列表
                    if not re.match(r'^\d+\. ', stripped):
                        match = re.match(r'^(\d+)\.?', stripped)
                        if match:
                            number = match.group(1)
                            line = line.replace(f'{number}.', f'{number}. ', 1)
                
                result_lines.append(line)
            else:
                if in_list and stripped:
                    # 列表中的内容行，添加缩进
                    result_lines.append('  ' + line)
                else:
                    result_lines.append(line)
                    in_list = False
        
        return '\n'.join(result_lines)
    
    def _fix_quotes(self, markdown_content: str) -> str:
        """修复引用格式"""
        # 确保引用块有正确的格式
        lines = markdown_content.split('\n')
        result_lines = []
        in_quote = False
        
        for line in lines:
            stripped = line.strip()
            
            # 检测引用行
            if stripped.startswith('>') or (in_quote and stripped):
                if not in_quote:
                    in_quote = True
                    # 确保引用前有空行
                    if result_lines and result_lines[-1].strip():
                        result_lines.append('')
                
                # 确保引用格式正确
                if stripped.startswith('>') and not stripped.startswith('> '):
                    line = line.replace('>', '> ', 1)
                
                result_lines.append(line)
            else:
                result_lines.append(line)
                in_quote = False
        
        return '\n'.join(result_lines)
    
    def _fix_headings(self, markdown_content: str) -> str:
        """修复标题格式"""
        # 确保标题前后有空行
        lines = markdown_content.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 检测标题行
            if stripped.startswith('#'):
                # 确保标题前有空行
                if i > 0 and lines[i-1].strip():
                    result_lines.append('')
                
                result_lines.append(line)
                
                # 确保标题后有空行
                if i < len(lines) - 1 and lines[i+1].strip():
                    result_lines.append('')
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _preserve_paragraph_structure(self, markdown_content: str) -> str:
        """保留段落结构"""
        # 确保段落之间有适当的空行
        lines = markdown_content.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                result_lines.append(line)
                continue
            
            # 如果是标题、列表、引用等特殊格式，保持原样
            if (stripped.startswith('#') or 
                stripped.startswith(('-', '*', '+', '1.', '2.', '3.')) or
                stripped.startswith('>') or
                stripped.startswith('```')):
                result_lines.append(line)
                continue
            
            # 普通段落，确保前后有空行
            if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith(('#', '-', '*', '+', '>', '```')):
                # 前一行不是特殊格式且不是空行，添加空行
                result_lines.append('')
            
            result_lines.append(line)
            
            if i < len(lines) - 1 and lines[i+1].strip() and not lines[i+1].strip().startswith(('#', '-', '*', '+', '>', '```')):
                # 后一行不是特殊格式且不是空行，添加空行
                result_lines.append('')
        
        return '\n'.join(result_lines)
    
    def _fix_image_links(self, match) -> str:
        """修复图片链接格式"""
        alt_text = match.group(1)
        url = match.group(2)
        
        # 如果alt文本为空，使用默认文本
        if not alt_text.strip():
            alt_text = '图片'
        
        return f'![{alt_text}]({url})'
    
    def _fix_code_blocks(self, markdown_content: str) -> str:
        """修复代码块格式"""
        
        # 检测并格式化代码块
        lines = markdown_content.split('\n')
        in_code_block = False
        code_block_lines = []
        result_lines = []
        
        for line in lines:
            if line.strip().startswith('```'):
                if in_code_block:
                    # 结束代码块
                    if code_block_lines:
                        # 检测语言
                        first_line = code_block_lines[0] if code_block_lines else ''
                        language = self._detect_code_language('\n'.join(code_block_lines))
                        
                        if language and not first_line.strip():
                            # 如果第一行是空的，添加语言标记
                            result_lines.append(f'```{language}')
                            result_lines.extend(code_block_lines)
                        else:
                            result_lines.append('```')
                            result_lines.extend(code_block_lines)
                    
                    result_lines.append('```')
                    in_code_block = False
                    code_block_lines = []
                else:
                    # 开始代码块
                    in_code_block = True
                    result_lines.append(line)
            elif in_code_block:
                code_block_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _fix_tables(self, markdown_content: str) -> str:
        """修复表格格式"""
        # 简单的表格格式修复
        lines = markdown_content.split('\n')
        result_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 检测表格行
            if '|' in line and not line.strip().startswith('|'):
                # 可能是表格分隔符行
                if re.match(r'^[\s|:-]+$', line.strip()):
                    # 确保表格格式正确
                    if i > 0 and '|' in lines[i-1]:
                        # 前一行是表头，确保分隔符格式正确
                        header_cells = lines[i-1].strip().split('|')
                        separator_cells = ['---'] * (len(header_cells) - 2)  # 减去首尾的空单元格
                        separator_line = '| ' + ' | '.join(separator_cells) + ' |'
                        result_lines[-1] = lines[i-1]  # 重新添加表头
                        result_lines.append(separator_line)
                        i += 1  # 跳过原始分隔符行
                        continue
            
            result_lines.append(line)
            i += 1
        
        return '\n'.join(result_lines)
    
    def _add_article_metadata(self, markdown_content: str, article_info: Dict) -> str:
        """添加文章元信息"""
        metadata = []
        
        if article_info.get('title'):
            metadata.append(f"# {article_info['title']}")
        
        if article_info.get('author') and article_info['author'] != '未知作者':
            metadata.append(f"**作者:** {article_info['author']}")
        
        if article_info.get('publish_time'):
            metadata.append(f"**发布时间:** {article_info['publish_time']}")
        
        if article_info.get('url'):
            metadata.append(f"**原文链接:** [{article_info['url']}]({article_info['url']})")
        
        if metadata:
            # 在元信息和内容之间添加分隔线
            metadata.append('---')
            markdown_content = '\n\n'.join(metadata) + '\n\n' + markdown_content
        
        return markdown_content