import pandas as pd
import numpy as np
import akshare as ak

from core.logging import logging

from app.services.data_fetcher import fetch_stock_data
from app.services.tech_indicators import calculate_moving_averages, calculate_oscillator_indicators

def count_signals(df):
    """计算买入、卖出和中立的数量"""
    buy_count = len(df[df['信号'] == '买入'])
    sell_count = len(df[df['信号'] == '卖出'])
    neutral_count = len(df[df['信号'] == '中立'])
    return buy_count, sell_count, neutral_count

def get_stock_info(symbol, stock_data):
    """获取股票基本信息"""
    try:
        # 获取股票名称
        stock_info_df = ak.stock_info_a_code_name()
        stock_name = stock_info_df[stock_info_df['code'] == symbol]['name'].values[0]
    except Exception as e:
        logging.warning(f"获取股票名称失败: {e}")
        stock_name = "未知"
    
    # 获取最新价格和日期
    latest_price = stock_data['close'].iloc[-1]
    latest_date = stock_data.index[-1]
    
    # 股票信息
    return {
        "代码": symbol,
        "名称": stock_name,
        "当前价格": float(latest_price),
        "日期": str(latest_date)
    }

def calculate_indicators(stock_data):
    """计算各类技术指标"""
    # 计算技术指标
    oscillator_df = calculate_oscillator_indicators(stock_data)
    ma_df = calculate_moving_averages(stock_data)
    
    # 计算震荡指标的信号数量
    oscillator_buy, oscillator_sell, oscillator_neutral = count_signals(oscillator_df)
    oscillator_counts = (oscillator_buy, oscillator_sell, oscillator_neutral)
    
    # 计算移动平均线的信号数量
    ma_buy, ma_sell, ma_neutral = count_signals(ma_df)
    ma_counts = (ma_buy, ma_sell, ma_neutral)
    
    # 计算总体信号
    total_buy = oscillator_buy + ma_buy
    total_sell = oscillator_sell + ma_sell
    total_neutral = oscillator_neutral + ma_neutral
    total_counts = (total_buy, total_sell, total_neutral)
    
    return oscillator_df, ma_df, oscillator_counts, ma_counts, total_counts

def create_result_json(oscillator_df, ma_df, oscillator_counts, ma_counts, total_counts, stock_info):
    """创建结果JSON"""
    # 转换DataFrame为字典
    oscillator_indicators = oscillator_df.to_dict('records')
    ma_indicators = ma_df.to_dict('records')
    
    # 创建结果字典
    result = {
        "股票信息": {
            "代码": stock_info["代码"],
            "名称": stock_info["名称"],
            "当前价格": stock_info["当前价格"],
            "日期": stock_info["日期"]
        },
        "震荡指标": {
            "指标列表": oscillator_indicators,
            "统计": {
                "买入": oscillator_counts[0],
                "卖出": oscillator_counts[1],
                "中立": oscillator_counts[2]
            }
        },
        "移动平均线": {
            "指标列表": ma_indicators,
            "统计": {
                "买入": ma_counts[0],
                "卖出": ma_counts[1],
                "中立": ma_counts[2]
            }
        },
        "总体统计": {
            "买入": total_counts[0],
            "卖出": total_counts[1],
            "中立": total_counts[2]
        }
    }
    
    return result

def analyze_stock(symbol, start_date, end_date):
    """分析股票并返回结果"""
    # 获取股票数据
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    
    if stock_data.empty:
        logging.error(f"无法获取股票 {symbol} 的数据")
        return None
    
    # 检查数据长度是否足够计算技术指标
    if len(stock_data) < 20:
        logging.warning(f"警告：获取的数据长度({len(stock_data)})不足以计算某些技术指标(如CCI需要至少20个数据点)")
    
    # 获取股票基本信息
    stock_info = get_stock_info(symbol, stock_data)
    
    # 计算各类指标
    oscillator_df, ma_df, oscillator_counts, ma_counts, total_counts = calculate_indicators(stock_data)
    
    # 创建结果JSON
    result = create_result_json(oscillator_df, ma_df, oscillator_counts, ma_counts, total_counts, stock_info)
    
    return result