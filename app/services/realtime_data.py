import akshare as ak
import pandas as pd
import json

# 设置pandas显示选项
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

def get_stock_realtime_data(symbol="000895"):
    """获取股票实时盘口数据并返回JSON格式"""
    # 获取股票实时盘口数据
    stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=symbol)
    
    # 将DataFrame转换为字典，然后转为JSON格式
    # 处理float64类型，确保可以被JSON序列化
    result = {
        "股票代码": symbol,
        "数据时间": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "盘口数据": json.loads(stock_bid_ask_em_df.to_json(orient="records", force_ascii=False))
    }
    
    # 返回JSON字符串
    return json.dumps(result, ensure_ascii=False, indent=2)