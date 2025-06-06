import json
from flask import Flask, request, jsonify
from main import main
import logging
from real_time import get_stock_realtime_data  # 导入实时盘口数据函数

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/stock-analysis', methods=['GET'])
def stock_analysis():
    """
    股票分析API
    参数:
    - symbol: 股票代码，如 "000895"
    - start_date: 开始日期，格式 "YYYYMMDD"
    - end_date: 结束日期，格式 "YYYYMMDD"
    """
    try:
        # 获取请求参数
        symbol = request.args.get('symbol', '000895')
        start_date = request.args.get('start_date', '20240530')
        end_date = request.args.get('end_date', '20250605')
        
        # 调用main函数
        logging.info(f"分析股票: {symbol}, 从 {start_date} 到 {end_date}")
        result = main(symbol, start_date, end_date)
        
        if result is None:
            return jsonify({"error": f"无法获取股票 {symbol} 的数据"}), 404
        
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"处理请求时出错: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/realtime-data', methods=['GET'])
def realtime_data():
    """
    实时盘口数据API
    参数:
    - symbol: 股票代码，如 "000895"
    """
    try:
        # 获取请求参数
        symbol = request.args.get('symbol', '000895')
        
        # 调用实时数据函数
        logging.info(f"获取股票 {symbol} 的实时盘口数据")
        result_json = get_stock_realtime_data(symbol)
        result = json.loads(result_json)  # 将JSON字符串转换为字典
        
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"获取实时数据时出错: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查API
    """
    return jsonify({"status": "ok"})

@app.route('/', methods=['GET'])
def home():
    """
    主页，提供API使用说明
    """
    return """
    <html>
        <head>
            <title>股票技术分析API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                h2 { color: #444; }
                pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
                .endpoint { margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <h1>股票技术分析API</h1>
            <p>使用此API可以获取股票的技术分析指标和信号。</p>
            
            <div class="endpoint">
                <h2>股票分析</h2>
                <p><strong>端点:</strong> /stock-analysis</p>
                <p><strong>方法:</strong> GET</p>
                <p><strong>参数:</strong></p>
                <ul>
                    <li>symbol: 股票代码，如 "000895"</li>
                    <li>start_date: 开始日期，格式 "YYYYMMDD"</li>
                    <li>end_date: 结束日期，格式 "YYYYMMDD"</li>
                </ul>
                <p><strong>示例:</strong></p>
                <pre>/stock-analysis?symbol=000895&start_date=20240101&end_date=20240630</pre>
            </div>
            
            <div class="endpoint">
                <h2>实时盘口数据</h2>
                <p><strong>端点:</strong> /realtime-data</p>
                <p><strong>方法:</strong> GET</p>
                <p><strong>参数:</strong></p>
                <ul>
                    <li>symbol: 股票代码，如 "000895"</li>
                </ul>
                <p><strong>示例:</strong></p>
                <pre>/realtime-data?symbol=000895</pre>
            </div>
            
            <div class="endpoint">
                <h2>健康检查</h2>
                <p><strong>端点:</strong> /health</p>
                <p><strong>方法:</strong> GET</p>
                <p><strong>示例:</strong></p>
                <pre>/health</pre>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)