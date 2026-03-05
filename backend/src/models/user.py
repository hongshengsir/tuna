#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户模型类 - 使用纯Python实现
"""

import bcrypt
import json
from datetime import datetime

class User:
    """用户模型类"""
    
    def __init__(self, id=None, username='', email='', password='', password_hash='', 
                 full_name='', phone='', avatar='', is_active=True, is_superuser=False, 
                 last_login=None, permissions=None, settings=None, 
                 created_at=None, updated_at=None):
        """初始化用户"""
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.avatar = avatar
        self.is_active = bool(is_active)
        self.is_superuser = bool(is_superuser)
        self.last_login = last_login
        
        # 密码处理
        if password:
            self.set_password(password)
        else:
            self.password_hash = password_hash
        
        # JSON字段处理
        self.permissions = json.dumps(permissions or {})
        self.settings = json.dumps(settings or {})
        
        # 时间戳
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_db_row(cls, row):
        """从数据库行创建用户对象"""
        if not row:
            return None
            
        return cls(
            id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            full_name=row[4],
            phone=row[5],
            avatar=row[6],
            is_active=bool(row[7]),
            is_superuser=bool(row[8]),
            last_login=row[9],
            permissions=json.loads(row[10]) if row[10] else {},
            settings=json.loads(row[11]) if row[11] else {},
            created_at=row[12],
            updated_at=row[13]
        )
    
    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except:
            return False
    
    def to_dict(self, include_sensitive=False):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'permissions': json.loads(self.permissions) if self.permissions else {},
            'settings': json.loads(self.settings) if self.settings else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
    
    def has_permission(self, permission):
        """检查用户是否有指定权限"""
        permissions = json.loads(self.permissions) if self.permissions else {}
        return permissions.get(permission, False) or self.is_superuser
    
    def add_permission(self, permission):
        """添加权限"""
        permissions = json.loads(self.permissions) if self.permissions else {}
        permissions[permission] = True
        self.permissions = json.dumps(permissions)
    
    def remove_permission(self, permission):
        """移除权限"""
        permissions = json.loads(self.permissions) if self.permissions else {}
        if permission in permissions:
            del permissions[permission]
            self.permissions = json.dumps(permissions)
    
    def update_setting(self, key, value):
        """更新用户设置"""
        settings = json.loads(self.settings) if self.settings else {}
        settings[key] = value
        self.settings = json.dumps(settings)
    
    def __repr__(self):
        """字符串表示"""
        return f"<User(username='{self.username}', email='{self.email}')>"