from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.schemas import TrendSignalResponse
from app.services.stage_by_tech import analyze_stock, get_trend_signals

router = APIRouter()

@router.get("/stage", response_model=TrendSignalResponse)
async def get_stock_stage(
    symbol: str = Query("000895", description="股票代码"),
    start_date: str = Query("20240530", description="开始日期，格式 'YYYYMMDD'"),
    end_date: str = Query("20250605", description="结束日期，格式 'YYYYMMDD'")
):
    try:
        data = analyze_stock(symbol, start_date, end_date)
        result_list = get_trend_signals(data)  # 返回 List[dict] 或 List[TrendSignalItem]
        if not result_list:
            raise HTTPException(status_code=404, detail=f"无法获取股票 {symbol} 的数据")
        return {"signals": result_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
