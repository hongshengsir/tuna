#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载记录数据访问对象
"""

import os
from datetime import datetime
from typing import List, Optional
from ..config.database import get_db
from .download_record import DownloadRecord

class DownloadRecordDAO:
    """下载记录数据访问对象"""
    
    def __init__(self, db_connection=None):
        """初始化"""
        self.table_name = 'download_records'
        self.db_connection = db_connection
    
    def create_table(self):
        """创建下载记录表"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    url VARCHAR(500) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(100),
                    download_status VARCHAR(20) DEFAULT 'pending',
                    markdown_file VARCHAR(500),
                    media_count INT DEFAULT 0,
                    file_size BIGINT DEFAULT 0,
                    download_time TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_user_id (user_id),
                    INDEX idx_url (url),
                    INDEX idx_status (download_status),
                    INDEX idx_created_at (created_at)
                )
            """)
            
            conn.commit()
            print(f"✅ 下载记录表 {self.table_name} 创建成功")
            
        except Exception as e:
            print(f"❌ 创建下载记录表失败: {e}")
            conn.rollback()
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()

    def create_download_record(self, user_id: int, url: str, title: str, author: str = '', 
                              download_status: str = 'pending', markdown_file: str = '', 
                              media_count: int = 0, file_size: int = 0) -> Optional[int]:
        """创建下载记录（便捷方法）"""
        from .download_record import DownloadRecord
        
        record = DownloadRecord(
            user_id=user_id,
            url=url,
            title=title,
            author=author,
            download_status=download_status,
            markdown_file=markdown_file,
            media_count=media_count,
            file_size=file_size
        )
        
        return self.create_record(record)
    
    def create_record(self, record: DownloadRecord) -> Optional[int]:
        """创建下载记录"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                INSERT INTO {self.table_name} 
                (user_id, url, title, author, download_status, markdown_file, 
                 media_count, file_size, download_time, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record.user_id, record.url, record.title, record.author,
                record.download_status, record.markdown_file, record.media_count,
                record.file_size, record.download_time, datetime.utcnow(), datetime.utcnow()
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            
            return record_id
            
        except Exception as e:
            print(f"❌ 创建下载记录失败: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_record_by_id(self, record_id: int) -> Optional[DownloadRecord]:
        """根据ID获取下载记录"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} WHERE id = %s
            """, (record_id,))
            
            row = cursor.fetchone()
            return DownloadRecord.from_db_row(row) if row else None
            
        except Exception as e:
            print(f"❌ 获取下载记录失败: {e}")
            return None
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_records_by_user(self, user_id: int, limit: int = 50) -> List[DownloadRecord]:
        """根据用户ID获取下载记录列表"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            return [DownloadRecord.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"❌ 获取用户下载记录失败: {e}")
            return []
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_all_records(self, skip: int = 0, limit: int = 20) -> List[DownloadRecord]:
        """获取所有下载记录（分页）"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """, (limit, skip))
            
            rows = cursor.fetchall()
            return [DownloadRecord.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"❌ 获取所有下载记录失败: {e}")
            return []
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_records_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[DownloadRecord]:
        """根据用户ID获取下载记录（分页）"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """, (user_id, limit, skip))
            
            rows = cursor.fetchall()
            return [DownloadRecord.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"❌ 获取用户下载记录失败: {e}")
            return []
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_records_by_status(self, status: str, skip: int = 0, limit: int = 20) -> List[DownloadRecord]:
        """根据状态获取下载记录（分页）"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} 
                WHERE download_status = %s 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """, (status, limit, skip))
            
            rows = cursor.fetchall()
            return [DownloadRecord.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"❌ 获取状态下载记录失败: {e}")
            return []
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_total_record_count(self) -> int:
        """获取总记录数"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT COUNT(*) FROM {self.table_name}
            """)
            
            row = cursor.fetchone()
            return row[0] if row else 0
            
        except Exception as e:
            print(f"❌ 获取总记录数失败: {e}")
            return 0
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_record_count_by_user_id(self, user_id: int) -> int:
        """获取用户记录数"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT COUNT(*) FROM {self.table_name} WHERE user_id = %s
            """, (user_id,))
            
            row = cursor.fetchone()
            return row[0] if row else 0
            
        except Exception as e:
            print(f"❌ 获取用户记录数失败: {e}")
            return 0
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_record_count_by_status(self, status: str) -> int:
        """获取状态记录数"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT COUNT(*) FROM {self.table_name} WHERE download_status = %s
            """, (status,))
            
            row = cursor.fetchone()
            return row[0] if row else 0
            
        except Exception as e:
            print(f"❌ 获取状态记录数失败: {e}")
            return 0
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def update_record_status(self, record_id: int, status: str, 
                           markdown_file: str = None, media_count: int = None,
                           file_size: int = None) -> bool:
        """更新下载记录状态"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            # 构建更新语句
            update_fields = ["download_status = %s"]
            params = [status]
            
            if markdown_file:
                update_fields.append("markdown_file = %s")
                params.append(markdown_file)
            
            if media_count is not None:
                update_fields.append("media_count = %s")
                params.append(media_count)
            
            if file_size is not None:
                update_fields.append("file_size = %s")
                params.append(file_size)
            
            # 如果是完成状态，设置下载时间
            if status == 'completed':
                update_fields.append("download_time = %s")
                params.append(datetime.utcnow())
            
            params.append(record_id)
            
            cursor.execute(f"""
                UPDATE {self.table_name} 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """, params)
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 更新下载记录状态失败: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def delete_record(self, record_id: int) -> bool:
        """删除下载记录"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                DELETE FROM {self.table_name} WHERE id = %s
            """, (record_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ 删除下载记录失败: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_statistics(self, user_id: int = None) -> dict:
        """获取下载统计信息"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            where_clause = "WHERE user_id = %s" if user_id else ""
            params = [user_id] if user_id else []
            
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN download_status = 'completed' THEN 1 END) as completed,
                    COUNT(CASE WHEN download_status = 'failed' THEN 1 END) as failed,
                    COUNT(CASE WHEN download_status = 'downloading' THEN 1 END) as downloading,
                    SUM(media_count) as total_media,
                    SUM(file_size) as total_size
                FROM {self.table_name} 
                {where_clause}
            """, params)
            
            row = cursor.fetchone()
            
            return {
                'total': row[0] if row else 0,
                'completed': row[1] if row else 0,
                'failed': row[2] if row else 0,
                'downloading': row[3] if row else 0,
                'total_media': row[4] if row else 0,
                'total_size': row[5] if row else 0
            }
            
        except Exception as e:
            print(f"❌ 获取统计信息失败: {e}")
            return {}
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_user_stats(self, user_id: int) -> dict:
        """获取用户下载统计信息"""
        return self.get_statistics(user_id)
    
    def get_overall_stats(self) -> dict:
        """获取整体下载统计信息"""
        return self.get_statistics()
    
    def get_recent_records(self, limit: int = 10) -> List[DownloadRecord]:
        """获取最近的下载记录"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT * FROM {self.table_name} 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            
            rows = cursor.fetchall()
            return [DownloadRecord.from_db_row(row) for row in rows]
            
        except Exception as e:
            print(f"❌ 获取最近下载记录失败: {e}")
            return []
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()
    
    def get_daily_stats(self, days: int = 7) -> dict:
        """获取每日下载统计"""
        conn = self.db_connection or get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as total,
                    COUNT(CASE WHEN download_status = 'completed' THEN 1 END) as completed,
                    COUNT(CASE WHEN download_status = 'failed' THEN 1 END) as failed
                FROM {self.table_name} 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            """, (days,))
            
            rows = cursor.fetchall()
            
            stats = {}
            for row in rows:
                date_str = row[0].strftime('%Y-%m-%d')
                stats[date_str] = {
                    'total': row[1],
                    'completed': row[2],
                    'failed': row[3]
                }
            
            return stats
            
        except Exception as e:
            print(f"❌ 获取每日统计失败: {e}")
            return {}
        finally:
            cursor.close()
            if not self.db_connection:
                conn.close()