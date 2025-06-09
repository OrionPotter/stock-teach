import pandas as pd
import numpy as np
import json
from app.services.data_fetcher import fetch_stock_data

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_kdj(df, n=9, k_period=3, d_period=3):
    low_min = df['low'].rolling(window=n, min_periods=n).min()
    high_max = df['high'].rolling(window=n, min_periods=n).max()
    rsv = (df['close'] - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(alpha=1/k_period, adjust=False).mean()
    d = k.ewm(alpha=1/d_period, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j

def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9, adjust=False).mean()
    macd_hist = dif - dea
    return dif, dea, macd_hist

def get_ma(df, window):
    return df['close'].rolling(window=window, min_periods=window).mean()

def get_trend_signals(data):
    data = data.copy()
    data['RSI6'] = calculate_rsi(data['close'], 6)
    data['RSI12'] = calculate_rsi(data['close'], 12)
    data['RSI24'] = calculate_rsi(data['close'], 24)
    data['K'], data['D'], data['J'] = calculate_kdj(data)
    data['DIF'], data['DEA'], data['MACD_HIST'] = calculate_macd(data['close'])
    data['MA5'] = get_ma(data, 5)
    data['MA10'] = get_ma(data, 10)
    data['MA20'] = get_ma(data, 20)
    data['VOL_MA5'] = data['volume'].rolling(window=5, min_periods=5).mean()
    data['VOL_MA10'] = data['volume'].rolling(window=10, min_periods=10).mean()

    # 这里reset_index会把date变成一列，列名为'date'
    recent = data.tail(5).reset_index()

    results = []
    for i in range(len(recent)):
        row = recent.loc[i]
        # MACD金叉
        if i == 0:
            macd_cross = False
        else:
            prev = recent.loc[i-1]
            macd_cross = (prev['DIF'] < prev['DEA']) and (row['DIF'] > row['DEA'])
        # KDJ金叉
        if i == 0:
            kdj_cross = False
        else:
            prev = recent.loc[i-1]
            kdj_cross = (prev['K'] < prev['D']) and (row['K'] > row['D'])
        # RSI反弹
        if i == 0:
            rsi_rebound = False
        else:
            prev = recent.loc[i-1]
            rsi_rebound = (prev['RSI6'] < 30) and (row['RSI6'] >= 30)
        # 多头排列
        ma_bullish = (row['MA5'] > row['MA10']) and (row['MA10'] > row['MA20']) and (row['close'] > row['MA20'])

        results.append({
            'date': row['date'] if isinstance(row['date'], str) else row['date'].strftime('%Y-%m-%d'),
            'close': float(row['close']),
            'volume': int(row['volume']),
            'MA5': float(row['MA5']) if not np.isnan(row['MA5']) else None,
            'MA10': float(row['MA10']) if not np.isnan(row['MA10']) else None,
            'MA20': float(row['MA20']) if not np.isnan(row['MA20']) else None,
            'VOL_MA5': float(row['VOL_MA5']) if not np.isnan(row['VOL_MA5']) else None,
            'VOL_MA10': float(row['VOL_MA10']) if not np.isnan(row['VOL_MA10']) else None,
            'DIF': float(row['DIF']) if not np.isnan(row['DIF']) else None,
            'DEA': float(row['DEA']) if not np.isnan(row['DEA']) else None,
            'MACD_HIST': float(row['MACD_HIST']) if not np.isnan(row['MACD_HIST']) else None,
            'MACD_gold_cross': bool(macd_cross),
            'K': float(row['K']) if not np.isnan(row['K']) else None,
            'D': float(row['D']) if not np.isnan(row['D']) else None,
            'J': float(row['J']) if not np.isnan(row['J']) else None,
            'KDJ_gold_cross': bool(kdj_cross),
            'RSI6': float(row['RSI6']) if not np.isnan(row['RSI6']) else None,
            'RSI12': float(row['RSI12']) if not np.isnan(row['RSI12']) else None,
            'RSI24': float(row['RSI24']) if not np.isnan(row['RSI24']) else None,
            'RSI_rebound': bool(rsi_rebound),
            'MA_bullish': bool(ma_bullish)
        })
    return results

# 使用方法：
# data = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')
# print(get_trend_signals(data))

def analyze_stock(symbol, start_date, end_date):
    """分析股票并返回结果"""
    # 获取股票数据
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    
    if stock_data.empty:
        logging.error(f"无法获取股票 {symbol} 的数据")
        return None
    
    # 检查数据长度是否足够计算技术指标
    if len(stock_data) < 20:
        logging.warning(f"警告：获取的数据长度({len(stock_data)})不足以计算某些技术指标")

    return stock_data

# 测试函数
if __name__ == "__main__":
    stock_data = analyze_stock("000895", "20240609", "20250609")
    print(get_trend_signals(stock_data))
