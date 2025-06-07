import pandas as pd
import argparse
import os
from datetime import datetime

from app.core.logging import logging

# 导入自定义模块
from app.services.data_fetcher import fetch_stock_data


def calculate_daily_change(data):
    """
    计算每日涨跌幅
    """
    # 计算涨跌幅 = (当日收盘价 - 前一日收盘价) / 前一日收盘价 * 100%
    data['涨跌幅'] = data['close'].pct_change() * 100
    # 第一天的涨跌幅设为0
    data['涨跌幅'].iloc[0] = 0
    return data

def format_stock_data(data):
    """
    格式化股票数据，添加涨跌幅
    """
    # 复制数据，避免修改原始数据
    formatted_data = data.copy()
    
    # 计算涨跌幅
    formatted_data = calculate_daily_change(formatted_data)
    
    # 重命名列
    formatted_data.rename(columns={
        'open': '开盘价',
        'close': '收盘价',
        'high': '最高价',
        'low': '最低价',
        'volume': '成交量'
    }, inplace=True)
    
    # 重置索引，将日期变为列
    formatted_data.reset_index(inplace=True)
    formatted_data.rename(columns={'date': '日期'}, inplace=True)
    
    # 四舍五入到两位小数
    for col in ['开盘价', '收盘价', '最高价', '最低价', '涨跌幅']:
        formatted_data[col] = formatted_data[col].round(2)
    
    return formatted_data

def export_stock_data(symbol, start_date=None, end_date=None, output_dir='./output'):
    """
    导出股票数据为CSV文件
    
    参数:
    symbol (str): 股票代码
    start_date (str): 开始日期，格式 'YYYYMMDD'
    end_date (str): 结束日期，格式 'YYYYMMDD'
    output_dir (str): 输出目录
    """
    # 获取股票数据
    logging.info(f"获取股票 {symbol} 从 {start_date} 到 {end_date} 的数据")
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    
    if stock_data.empty:
        logging.error(f"无法获取股票 {symbol} 的数据")
        return False
    
    # 格式化数据
    formatted_data = format_stock_data(stock_data)
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成输出文件名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{symbol}_{current_time}.csv")
    
    # 导出为CSV
    formatted_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    logging.info(f"股票数据已导出到 {output_file}")
    
    return output_file

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='导出股票数据为CSV文件')
    parser.add_argument('symbol', help='股票代码')
    parser.add_argument('--start_date', help='开始日期 (YYYYMMDD)', default=None)
    parser.add_argument('--end_date', help='结束日期 (YYYYMMDD)', default=None)
    parser.add_argument('--output_dir', help='输出目录', default='./output')
    
    args = parser.parse_args()
    
    # 导出数据
    output_file = export_stock_data(
        args.symbol, 
        args.start_date, 
        args.end_date, 
        args.output_dir
    )
    
    if output_file:
        print(f"股票数据已成功导出到: {output_file}")
    else:
        print("导出失败")

if __name__ == "__main__":
    main()