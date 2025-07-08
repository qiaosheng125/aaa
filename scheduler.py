#!/usr/bin/env python
"""
定时任务调度器

使用APScheduler库管理定期执行的维护任务，如会话清理、旧文件清理等
"""

import logging
import sys
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app import app
from clean_sessions import clean_inactive_sessions
from models import File

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('task_scheduler')

def schedule_tasks():
    """
    配置并启动定时任务
    """
    try:
        logger.info("正在初始化任务调度器...")
        
        # 创建调度器
        scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        
        # 添加会话清理任务 - 每天凌晨3点执行
        scheduler.add_job(
            func=lambda: app.app_context().push() and clean_inactive_sessions(24),
            trigger=CronTrigger(hour=3, minute=0),
            id='clean_sessions',
            name='清理不活跃会话',
            replace_existing=True
        )
        
        # 添加文件清理任务 - 每周一凌晨5点执行
        scheduler.add_job(
            func=lambda: app.app_context().push() and File.cleanup_old_files(),
            trigger=CronTrigger(day_of_week='mon', hour=5, minute=0),
            id='cleanup_files',
            name='清理旧文件',
            replace_existing=True
        )
        
        # 添加数据库连接保活任务 - 每5分钟执行一次
        def keep_db_alive():
            with app.app_context():
                from sqlalchemy import text
                from app import db
                # 执行简单查询以保持数据库连接活跃
                db.session.execute(text('SELECT 1'))
                db.session.commit()
                
        scheduler.add_job(
            func=keep_db_alive,
            trigger=IntervalTrigger(minutes=5),
            id='keep_db_alive',
            name='保持数据库连接',
            replace_existing=True
        )
        
        # 启动调度器
        scheduler.start()
        logger.info("任务调度器已启动，正在运行以下任务:")
        for job in scheduler.get_jobs():
            logger.info(f"  - {job.name}: 下次运行时间 {job.next_run_time}")
        
        return scheduler
    
    except Exception as e:
        logger.error(f"初始化任务调度器时出错: {str(e)}")
        return None

if __name__ == "__main__":
    # 启动调度器
    scheduler = schedule_tasks()
    
    try:
        # 保持程序运行
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        if scheduler:
            scheduler.shutdown()
            logger.info("任务调度器已关闭")