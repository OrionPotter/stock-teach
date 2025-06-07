import logging
import sys
from pathlib import Path

def setup_logging():
    """配置日志"""
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log", encoding="utf-8"),
        ],
    )
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    