from fastapi import APIRouter, HTTPException, Query
import json

from app.services.realtime_data import get_stock_realtime_data

router = APIRouter()

@router.get("/data")
async def get_realtime_data(symbol: str = Query("000895", description="股票代码")):
    """获取股票实时盘口数据"""
    try:
        result_json = get_stock_realtime_data(symbol)
        result = json.loads(result_json)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))