"""
数据库迁移脚本：添加文件查看计数字段

这个脚本将为File模型添加view_count字段，用于跟踪文件被查看的次数。
"""

from app import app, db
import models
from sqlalchemy import Column, Integer, text
import sys

def run_migration():
    """
    运行数据库迁移，添加文件查看计数字段
    """
    # 将应用上下文推送到应用栈中
    with app.app_context():
        try:
            # 检查字段是否已经存在
            inspector = db.inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('files')]
            
            if 'view_count' not in columns:
                print("正在添加view_count字段...")
                # 使用执行原始SQL来添加字段
                sql = text('ALTER TABLE files ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0')
                db.session.execute(sql)
                db.session.commit()
                print("view_count字段添加成功")
            else:
                print("view_count字段已存在，无需添加")
            
            return True
            
        except Exception as e:
            print(f"添加view_count字段失败: {str(e)}")
            return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)