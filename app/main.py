from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.logging import setup_logging

# 配置日志
setup_logging()

# 创建FastAPI应用
app = FastAPI(
    title="股票技术分析API",
    description="提供股票技术分析、实时盘口数据和数据导出功能的API",
    version="0.1.0",
    # 确保启用 OpenAPI 和 Swagger UI
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    # 添加联系信息和许可证信息
    contact={
        "name": "技术支持",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router)

# 主页路由
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>股票技术分析API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                h2 { color: #444; }
                pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
                .endpoint { margin-bottom: 20px; }
                .swagger-button { 
                    display: inline-block; 
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 10px 20px; 
                    text-align: center; 
                    text-decoration: none; 
                    font-size: 16px; 
                    margin: 10px 0; 
                    border-radius: 5px; 
                }
            </style>
        </head>
        <body>
            <h1>股票技术分析API</h1>
            <p>使用此API可以获取股票的技术分析指标和信号。</p>
            <p>
                <a href="/docs" class="swagger-button">Swagger UI 交互式文档</a>
                <a href="/redoc" style="margin-left: 10px;">ReDoc 文档</a>
            </p>
            
            <div class="endpoint">
                <h2>主要功能</h2>
                <ul>
                    <li>股票技术分析 - 计算各种技术指标和信号</li>
                    <li>实时盘口数据 - 获取股票实时交易数据</li>
                    <li>数据导出 - 导出股票历史数据为CSV格式</li>
                </ul>
            </div>
        </body>
    </html>
    """

# 健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)