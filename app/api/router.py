from fastapi import APIRouter

from app.api.endpoints import stock_analysis, realtime_data, stock_export

api_router = APIRouter(prefix="/api")

# 注册各个端点路由
api_router.include_router(stock_analysis.router, prefix="/stock", tags=["股票分析"])
api_router.include_router(realtime_data.router, prefix="/realtime", tags=["实时数据"])
api_router.include_router(stock_export.router, prefix="/export", tags=["数据导出"])