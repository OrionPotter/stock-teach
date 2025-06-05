import pandas as pd
import akshare as ak
import time
import urllib3
import requests
import random
import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 尝试导入备选库
try:
    import baostock as bs
except ImportError:
    bs = None

def fetch_stock_data(symbol, start_date=None, end_date=None, adjust="qfq", retry_count=3, use_alternative=True):
    """
    使用akshare获取股票历史数据，如果失败则尝试使用备选方案
    
    参数:
    symbol (str): 股票代码，如 "600000" (上证) 或 "000001" (深证)
    start_date (str): 开始日期，格式 'YYYYMMDD'
    end_date (str): 结束日期，格式 'YYYYMMDD'
    adjust (str): 复权类型，可选值："qfq"(前复权)、"hfq"(后复权)、""(不复权)
    retry_count (int): 重试次数
    use_alternative (bool): 是否使用备选数据源
    
    返回:
    pandas.DataFrame: 包含股票数据的DataFrame
    """
    # 设置默认日期范围
    if start_date is None:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y%m%d")
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y%m%d")
    
    logging.info(f"开始获取股票 {symbol} 从 {start_date} 到 {end_date} 的数据")
    
    # 首先尝试使用akshare的stock_zh_a_hist获取数据
    df = _fetch_with_akshare_hist(symbol, start_date, end_date, adjust, retry_count)
    
    # 如果获取失败，尝试使用备选方案
    if df.empty and use_alternative:
        # 尝试使用akshare的stock_zh_a_spot_em获取当日数据
        logging.info(f"尝试使用stock_zh_a_spot_em获取股票 {symbol} 的当日数据")
        df_spot = _fetch_with_akshare_spot(symbol)
        
        if not df_spot.empty:
            return df_spot
    
    if df.empty:
        logging.warning(f"无法获取股票 {symbol} 的数据，所有尝试均失败")
    else:
        logging.info(f"成功获取股票 {symbol} 的数据，共 {len(df)} 条记录")
    
    return df

def _fetch_with_akshare_hist(symbol, start_date, end_date, adjust="qfq", retry_count=3):
    """
    使用akshare的stock_zh_a_hist获取股票历史数据
    """
    try:
        # 禁用SSL警告
        urllib3.disable_warnings()
        
        # 添加重试机制
        for attempt in range(retry_count):
            try:
                # 随机延时，避免被限流
                time.sleep(random.uniform(1, 3))
                
                # 使用akshare获取A股历史数据
                df = ak.stock_zh_a_hist(
                    symbol=symbol, 
                    period="daily", 
                    start_date=start_date, 
                    end_date=end_date, 
                    adjust=adjust
                )
                
                # 如果成功获取数据
                if not df.empty:
                    # 重命名列以匹配之前的格式
                    df.rename(columns={
                        "日期": "date",
                        "开盘": "open",
                        "收盘": "close",
                        "最高": "high",
                        "最低": "low",
                        "成交量": "volume"
                    }, inplace=True)
                    
                    # 设置日期为索引
                    df.set_index("date", inplace=True)
                    
                    return df
                else:
                    logging.warning(f"尝试 {attempt+1}/{retry_count} 获取股票数据返回空DataFrame")
                
            except Exception as e:
                logging.error(f"尝试 {attempt+1}/{retry_count} 获取股票数据失败: {e}")
                time.sleep(random.uniform(2, 5))  # 随机等待2-5秒后重试
        
        # 如果所有尝试都失败
        return pd.DataFrame()
        
    except Exception as e:
        logging.error(f"使用akshare获取股票历史数据时出错: {e}")
        return pd.DataFrame()

def _fetch_with_akshare_spot(symbol):
    """
    使用akshare的stock_zh_a_spot_em获取股票当日数据
    """
    try:
        # 获取所有A股实时行情
        df_spot_all = ak.stock_zh_a_spot_em()
        
        # 筛选指定股票
        df_spot = df_spot_all[df_spot_all['代码'] == symbol]
        
        if not df_spot.empty:
            # 提取需要的列并重命名
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            df_result = pd.DataFrame({
                'date': [today],
                'open': [df_spot['开盘'].values[0]],
                'close': [df_spot['最新价'].values[0]],
                'high': [df_spot['最高'].values[0]],
                'low': [df_spot['最低'].values[0]],
                'volume': [df_spot['成交量'].values[0]]
            })
            
            # 设置日期为索引
            df_result.set_index('date', inplace=True)
            
            return df_result
        
        return pd.DataFrame()
    
    except Exception as e:
        logging.error(f"使用akshare获取股票当日数据时出错: {e}")
        return pd.DataFrame()


# 测试函数
if __name__ == "__main__":
    # 获取上证指数数据
    data = fetch_stock_data("000001")
    print(data.head())