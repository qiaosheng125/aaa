# gunicorn_config.py
"""
Gunicorn多进程配置文件，用于优化多用户并发场景下的性能

默认的gunicorn配置只有一个worker，无法充分利用多核CPU资源
这个配置文件添加了更多worker和连接选项，大幅提升并发处理能力
"""

import multiprocessing

# 设置worker数量，通常设置为 (2*CPU核心数 + 1)
# 对于这个环境，我们设置为4个worker
workers = 4

# 使用线程模式，每个worker可以处理多个线程，提高并发能力
worker_class = 'gthread'
threads = 2

# 允许每个worker处理的最大并发连接数
worker_connections = 1000  

# 请求超时时间（秒）
timeout = 120

# 保持连接时间（秒）
keepalive = 5

# 其他性能调优选项
max_requests = 10000  # 处理多少请求后自动重启worker (防止内存泄漏)
max_requests_jitter = 1000  # 添加随机抖动，避免所有worker同时重启

# 允许重用端口
reuse_port = True

# 是否在开发模式下自动重加载代码
reload = True

# 绑定地址
bind = "0.0.0.0:5000"

# 进程名称前缀
proc_name = "zucaixu_app"

# 日志级别
loglevel = "info"

# 预加载应用，可减少worker启动时间
preload_app = True

# 优化缓冲区设置
forwarded_allow_ips = '*'
proxy_allow_ips = '*'

# 优化worker启动速度
worker_tmp_dir = '/tmp'

# 在主进程启动后执行函数
def post_fork(server, worker):
    """在worker fork之后执行
    只在worker进程中运行
    """
    pass

def when_ready(server):
    """
    在所有worker都准备好之后执行
    只在主进程中运行一次
    """
    try:
        # 导入调度器
        from scheduler import schedule_tasks
        import logging
        
        logging.info("Gunicorn ready, starting background tasks scheduler...")
        # 启动任务调度器
        scheduler = schedule_tasks()
        if scheduler:
            logging.info("Background tasks scheduler started successfully")
        else:
            logging.error("Failed to start background tasks scheduler")
    except Exception as e:
        logging.error(f"Error starting scheduler: {str(e)}")

# 配置日志格式
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}