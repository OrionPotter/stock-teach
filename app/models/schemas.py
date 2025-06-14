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

class TrendSignalItem(BaseModel):
    date: str = Field(..., description="交易日期，格式如 2025-06-03")
    close: float = Field(..., description="收盘价")
    volume: int = Field(..., description="成交量")
    MA5: Optional[float] = Field(None, description="5日均线")
    MA10: Optional[float] = Field(None, description="10日均线")
    MA20: Optional[float] = Field(None, description="20日均线")
    VOL_MA5: Optional[float] = Field(None, description="5日均量")
    VOL_MA10: Optional[float] = Field(None, description="10日均量")
    DIF: Optional[float] = Field(None, description="MACD DIF线")
    DEA: Optional[float] = Field(None, description="MACD DEA线")
    MACD_HIST: Optional[float] = Field(None, description="MACD柱状图")
    MACD_gold_cross: bool = Field(..., description="MACD金叉")
    K: Optional[float] = Field(None, description="KDJ K值")
    D: Optional[float] = Field(None, description="KDJ D值")
    J: Optional[float] = Field(None, description="KDJ J值")
    KDJ_gold_cross: bool = Field(..., description="KDJ金叉")
    RSI6: Optional[float] = Field(None, description="RSI6")
    RSI12: Optional[float] = Field(None, description="RSI12")
    RSI24: Optional[float] = Field(None, description="RSI24")
    RSI_rebound: bool = Field(..., description="RSI反弹")
    MA_bullish: bool = Field(..., description="均线多头排列")

class TrendSignalResponse(BaseModel):
    signals: List[TrendSignalItem] = Field(..., description="最近5天的技术指标趋势列表")