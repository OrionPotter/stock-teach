from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.schemas import StockAnalysisResponse
from app.services.stock_analyzer import analyze_stock

router = APIRouter()

@router.get("/analysis", response_model=StockAnalysisResponse)
async def get_stock_analysis(
    symbol: str = Query("000895", description="股票代码"),
    start_date: str = Query("20240530", description="开始日期，格式 'YYYYMMDD'"),
    end_date: str = Query("20250605", description="结束日期，格式 'YYYYMMDD'")
):
    """获取股票技术分析结果，包括各种技术指标和信号"""
    try:
        result = analyze_stock(symbol, start_date, end_date)
        if result is None:
            raise HTTPException(status_code=404, detail=f"无法获取股票 {symbol} 的数据")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))