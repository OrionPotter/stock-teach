from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
import os
from typing import Optional

from app.services.stock_exporter import export_stock_data
from app.models.schemas import StockExportResponse

router = APIRouter()

@router.get("/csv", response_model=StockExportResponse)
async def export_stock_to_csv(
    symbol: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None, description="开始日期，格式 'YYYYMMDD'"),
    end_date: Optional[str] = Query(None, description="结束日期，格式 'YYYYMMDD'")
):
    """导出股票数据为CSV文件"""
    try:
        output_file = export_stock_data(symbol, start_date, end_date)
        if not output_file:
            return StockExportResponse(
                success=False,
                message=f"无法获取股票 {symbol} 的数据"
            )
        
        return StockExportResponse(
            success=True,
            message=f"股票数据已成功导出",
            file_path=output_file
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{symbol}")
async def download_stock_csv(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """下载股票数据CSV文件"""
    try:
        output_file = export_stock_data(symbol, start_date, end_date)
        if not output_file or not os.path.exists(output_file):
            raise HTTPException(status_code=404, detail=f"无法生成股票 {symbol} 的数据文件")
        
        # 设置下载完成后删除文件（可选）
        if background_tasks:
            background_tasks.add_task(lambda: os.unlink(output_file) if os.path.exists(output_file) else None)
        
        return FileResponse(
            path=output_file,
            filename=os.path.basename(output_file),
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))