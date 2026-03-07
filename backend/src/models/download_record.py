#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载记录模型类
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class DownloadRecord:
    """下载记录模型类"""
    
    def __init__(self, 
                 id=None, 
                 user_id=None,
                 url='', 
                 title='', 
                 author='', 
                 download_status='pending',
                 markdown_file='',
                 media_count=0,
                 file_size=0,
                 download_time=None,
                 created_at=None,
                 updated_at=None):
        """初始化下载记录"""
        self.id = id
        self.user_id = user_id
        self.url = url
        self.title = title
        self.author = author
        self.download_status = download_status  # pending, downloading, completed, failed
        self.markdown_file = markdown_file
        self.media_count = media_count
        self.file_size = file_size
        self.download_time = download_time
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db_row(cls, row):
        """从数据库行创建下载记录对象"""
        if not row:
            return None
            
        return cls(
            id=row[0],
            user_id=row[1],
            url=row[2],
            title=row[3],
            author=row[4],
            download_status=row[5],
            markdown_file=row[6],
            media_count=row[7],
            file_size=row[8],
            download_time=row[9],
            created_at=row[10],
            updated_at=row[11]
        )
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'download_status': self.download_status,
            'markdown_file': self.markdown_file,
            'media_count': self.media_count,
            'file_size': self.file_size,
            'download_time': self.download_time.isoformat() if self.download_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """字符串表示"""
        return f"<DownloadRecord(title='{self.title}', status='{self.download_status}')>"