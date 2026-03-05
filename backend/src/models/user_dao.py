#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户数据访问层 - 使用纯Python实现
"""

import json
from .user import User

class UserDAO:
    """用户数据访问对象"""
    
    def __init__(self, db_connection):
        """初始化"""
        self.db = db_connection
    
    def create_user(self, username, email, password, full_name='', phone='', avatar='', 
                    is_active=True, is_superuser=False, permissions=None, settings=None):
        """创建新用户"""
        # 检查用户名和邮箱是否已存在
        if self.get_user_by_username(username):
            raise ValueError("用户名已存在")
        
        if self.get_user_by_email(email):
            raise ValueError("邮箱已存在")
        
        # 创建用户对象并设置密码
        user = User(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            avatar=avatar,
            is_active=is_active,
            is_superuser=is_superuser,
            permissions=permissions,
            settings=settings
        )
        
        # 插入数据库
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, phone, avatar, 
                                 is_active, is_superuser, permissions, settings)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user.username, user.email, user.password_hash, user.full_name, user.phone,
                user.avatar, user.is_active, user.is_superuser, user.permissions, user.settings
            ))
            self.db.commit()
            
            # 获取新创建的用户ID
            user.id = cursor.lastrowid
            return user
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"创建用户失败: {e}")
        finally:
            cursor.close()
    
    def get_user_by_id(self, user_id):
        """根据ID获取用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            return User.from_db_row(row) if row else None
        finally:
            cursor.close()
    
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            return User.from_db_row(row) if row else None
        finally:
            cursor.close()
    
    def get_user_by_email(self, email):
        """根据邮箱获取用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
            return User.from_db_row(row) if row else None
        finally:
            cursor.close()
    
    def get_all_users(self, skip=0, limit=100):
        """获取所有用户（分页）"""
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s", (limit, skip))
            rows = cursor.fetchall()
            return [User.from_db_row(row) for row in rows]
        finally:
            cursor.close()
    
    def get_user_count(self):
        """获取用户总数"""
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
    
    def search_users(self, keyword, skip=0, limit=100):
        """搜索用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT * FROM users 
                WHERE username LIKE %s OR email LIKE %s OR full_name LIKE %s
                ORDER BY id LIMIT %s OFFSET %s
            """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', limit, skip))
            rows = cursor.fetchall()
            return [User.from_db_row(row) for row in rows]
        finally:
            cursor.close()
    
    def update_user(self, user_id, update_data):
        """更新用户信息"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        cursor = self.db.cursor()
        try:
            # 构建更新语句
            set_clause = []
            params = []
            
            for key, value in update_data.items():
                if key in ['full_name', 'phone', 'avatar', 'is_active', 'is_superuser']:
                    set_clause.append(f"{key} = %s")
                    params.append(value)
                elif key == 'permissions':
                    set_clause.append("permissions = %s")
                    params.append(json.dumps(value))
                elif key == 'settings':
                    set_clause.append("settings = %s")
                    params.append(json.dumps(value))
            
            if not set_clause:
                return user
            
            params.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(set_clause)} WHERE id = %s", params)
            self.db.commit()
            
            # 返回更新后的用户
            return self.get_user_by_id(user_id)
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"更新用户失败: {e}")
        finally:
            cursor.close()
    
    def delete_user(self, user_id):
        """删除用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()
    
    def change_password(self, user_id, new_password):
        """修改密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        cursor = self.db.cursor()
        try:
            user.set_password(new_password)
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", 
                          (user.password_hash, user_id))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()
    
    def authenticate_user(self, username, password):
        """用户认证"""
        user = self.get_user_by_username(username)
        if not user:
            # 尝试使用邮箱登录
            user = self.get_user_by_email(username)
        
        if user and user.check_password(password) and user.is_active:
            # 更新最后登录时间
            cursor = self.db.cursor()
            try:
                cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user.id,))
                self.db.commit()
            finally:
                cursor.close()
            return user
        
        return None
    
    def activate_user(self, user_id):
        """激活用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE users SET is_active = TRUE WHERE id = %s", (user_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()
    
    def deactivate_user(self, user_id):
        """禁用用户"""
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()
    
    def update_permissions(self, user_id, permissions):
        """更新用户权限"""
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE users SET permissions = %s WHERE id = %s", 
                          (json.dumps(permissions), user_id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()
    
    def update_settings(self, user_id, settings):
        """更新用户设置"""
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE users SET settings = %s WHERE id = %s", 
                          (json.dumps(settings), user_id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            return False
        finally:
            cursor.close()