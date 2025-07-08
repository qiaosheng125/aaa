#!/usr/bin/env python
"""
会话清理工具

此脚本用于清理不活跃的用户会话，应当定期运行
"""

import logging
import sys
import os
import json
from datetime import datetime, timedelta
from app import app, db
from models import UserSession, User, AuditLog, beijing_now

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('session_cleaner')

def clean_inactive_sessions(hours=24):
    """清理指定时间内未活动的会话
    
    参数:
        hours: 未活动小时数，超过此时间的会话将被清理
    """
    try:
        logger.info(f"开始清理 {hours} 小时内不活跃的会话...")
        
        # 计算截止时间
        cutoff_time = beijing_now() - timedelta(hours=hours)
        
        # 检查当前会话数量
        total_sessions = UserSession.query.count()
        logger.info(f"当前总会话数: {total_sessions}")
        
        # 获取不活跃的会话
        inactive_sessions = UserSession.query.filter(
            UserSession.last_seen < cutoff_time
        ).all()
        
        # 记录被清理的会话信息
        cleaned_sessions = []
        admin_sessions = []
        
        for session in inactive_sessions:
            user = User.query.get(session.user_id)
            if user:
                if user.is_admin:
                    # 保留管理员会话的记录，但不清理
                    admin_sessions.append({
                        'user_id': user.id,
                        'username': user.username,
                        'session_id': session.session_id
                    })
                    continue
                
                # 记录非管理员会话信息
                cleaned_sessions.append({
                    'user_id': user.id,
                    'username': user.username,
                    'session_id': session.session_id,
                    'last_seen': session.last_seen.strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # 清理该会话
                db.session.delete(session)
        
        # 提交数据库变更
        if cleaned_sessions:
            db.session.commit()
            logger.info(f"已清理 {len(cleaned_sessions)} 个不活跃会话")
            
            # 记录审计日志
            log_entry = AuditLog(
                user_id=None,  # 系统操作
                ip_address='127.0.0.1',
                action_type='clean_inactive_sessions',
                details=json.dumps({
                    'cleaned_count': len(cleaned_sessions),
                    'hours': hours,
                    'total_sessions': total_sessions,
                    'excluded_admin_sessions': len(admin_sessions)
                })
            )
            db.session.add(log_entry)
            db.session.commit()
        else:
            logger.info("没有不活跃的会话需要清理")
        
        # 显示保留的管理员会话
        if admin_sessions:
            logger.info(f"保留了 {len(admin_sessions)} 个管理员会话")
        
        return len(cleaned_sessions)
    
    except Exception as e:
        logger.error(f"清理会话时出错: {str(e)}")
        db.session.rollback()
        return 0

if __name__ == "__main__":
    with app.app_context():
        # 如果提供了参数，使用参数作为小时数
        hours = 24
        if len(sys.argv) > 1:
            try:
                hours = float(sys.argv[1])
            except ValueError:
                logger.error("小时数必须为数字")
                sys.exit(1)
        
        # 执行清理
        cleaned = clean_inactive_sessions(hours)
        logger.info(f"会话清理完成，共清理 {cleaned} 个会话")