from app import app, db
from models import File
from sqlalchemy.sql import text

def add_view_enabled_field():
    """向files表添加view_enabled字段，表示文件是否允许查看"""
    with app.app_context():
        print("正在为文件表添加view_enabled字段...")
        
        try:
            # 根据数据库类型执行不同的SQL
            if db.engine.name == 'postgresql':
                # PostgreSQL语法
                db.session.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS view_enabled BOOLEAN DEFAULT TRUE"))
            else:
                # SQLite语法
                # 首先检查列是否存在
                columns = db.session.execute(text("PRAGMA table_info(files)")).fetchall()
                column_names = [column[1] for column in columns]
                if 'view_enabled' not in column_names:
                    db.session.execute(text("ALTER TABLE files ADD COLUMN view_enabled BOOLEAN DEFAULT 1"))
            
            db.session.commit()
            
            # 更新已有记录，设置默认值为True(1)
            db.session.execute(text("UPDATE files SET view_enabled = TRUE WHERE view_enabled IS NULL"))
            db.session.commit()
            
            print("文件表view_enabled字段添加成功")
        except Exception as e:
            print(f"添加view_enabled字段时出错: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    add_view_enabled_field()
    print("迁移完成") 