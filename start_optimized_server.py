#!/usr/bin/env python
"""
高性能服务器启动脚本

使用优化的gunicorn配置启动Flask应用，支持20-30个客户同时访问
"""
import os
import sys
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('server_launcher')

def kill_existing_gunicorn():
    """查找并杀死已经运行的gunicorn进程"""
    try:
        logger.info("检查是否有gunicorn进程正在运行...")
        result = subprocess.run(['pgrep', '-f', 'gunicorn'], capture_output=True, text=True)
        pids = result.stdout.strip().split('\n')
        
        for pid in pids:
            if pid:
                logger.info(f"检测到正在运行的gunicorn进程 PID:{pid}，正在终止...")
                subprocess.run(['kill', '-9', pid])
                logger.info(f"已终止gunicorn进程 PID:{pid}")
        
        time.sleep(1)  # 等待进程完全终止
    except Exception as e:
        logger.error(f"尝试终止已有gunicorn进程时出错: {str(e)}")

def start_optimized_server():
    """启动使用优化配置的gunicorn服务器"""
    try:
        logger.info("准备使用优化配置启动服务器...")
        
        # 设置必要的环境变量
        os.environ['PYTHONUNBUFFERED'] = '1'
        
        # 构建启动命令
        cmd = [
            'gunicorn',
            '-c', 'gunicorn_config.py',  # 使用我们创建的配置文件
            'main:app'
        ]
        
        logger.info(f"启动命令: {' '.join(cmd)}")
        logger.info("服务器启动中...")
        
        # 使用 Popen 启动服务器，并让它在后台运行
        subprocess.Popen(cmd)
        
        logger.info("服务器已启动，使用优化配置提供服务")
        logger.info("可通过 http://0.0.0.0:5000 访问应用")
        
    except Exception as e:
        logger.error(f"启动服务器时出错: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    # 先关闭可能已经在运行的gunicorn进程
    kill_existing_gunicorn()
    
    # 启动优化后的服务器
    sys.exit(start_optimized_server())