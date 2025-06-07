from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# 请求模型
class StockAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="股票代码，如 '000895'")
    start_date: str = Field(..., description="开始日期，格式 'YYYYMMDD'")
    end_date: str = Field(..., description="结束日期，格式 'YYYYMMDD'")

class RealtimeDataRequest(BaseModel):
    symbol: str = Field(..., description="股票代码，如 '000895'")

class StockExportRequest(BaseModel):
    symbol: str = Field(..., description="股票代码，如 '000895'")
    start_date: Optional[str] = Field(None, description="开始日期，格式 'YYYYMMDD'")
    end_date: Optional[str] = Field(None, description="结束日期，格式 'YYYYMMDD'")

# 响应模型
class StockInfo(BaseModel):
    代码: str
    名称: str
    当前价格: float
    日期: str

class IndicatorStats(BaseModel):
    买入: int
    卖出: int
    中立: int

class IndicatorItem(BaseModel):
    名称: str
    值: float
    信号: str

class OscillatorIndicators(BaseModel):
    指标列表: List[IndicatorItem]
    统计: IndicatorStats

class MovingAverages(BaseModel):
    指标列表: List[IndicatorItem]
    统计: IndicatorStats

class StockAnalysisResponse(BaseModel):
    股票信息: StockInfo
    震荡指标: OscillatorIndicators
    移动平均线: MovingAverages
    总体统计: IndicatorStats

class RealtimeDataResponse(BaseModel):
    股票代码: str
    数据时间: str
    盘口数据: List[Dict[str, Any]]

class StockExportResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None