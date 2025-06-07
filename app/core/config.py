import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    # API配置
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "股票技术分析API"
    
    # 数据目录
    OUTPUT_DIR: str = "./output"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置对象
settings = Settings()

# 确保输出目录存在
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)