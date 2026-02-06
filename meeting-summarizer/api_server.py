#!/usr/bin/env python3
"""
Paraformer API Server
提供 HTTP API 接口用于语音转录
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
import uvicorn
from typing import Optional

# 导入转录函数
from transcribe_multi_model import transcribe_with_paraformer

app = FastAPI(
    title="Paraformer ASR API",
    description="阿里 Paraformer 语音识别 API 服务",
    version="1.0.0"
)

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "Paraformer ASR API",
        "version": "1.0.0",
        "model": "paraformer-zh"
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: Optional[str] = "zh"
):
    """
    转录音频文件
    
    参数:
    - file: 音频文件 (mp3, wav, m4a, mp4)
    - language: 语言代码 (默认: zh)
    
    返回:
    - utterances: 转录结果列表
    - confidence: 准确率
    - model: 使用的模型
    """
    
    # 检查文件类型
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.mp4', '.flac', '.ogg'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {file_ext}. 支持的格式: {', '.join(allowed_extensions)}"
        )
    
    # 保存上传的文件到临时目录
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # 调用 Paraformer 转录
        result = transcribe_with_paraformer(tmp_file_path)
        
        # 删除临时文件
        os.unlink(tmp_file_path)
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="转录失败"
            )
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "utterances": result['utterances'],
                "confidence": result['confidence'],
                "model": result['model'],
                "audio_duration": result.get('audio_duration', 0)
            }
        })
        
    except Exception as e:
        # 清理临时文件
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"处理错误: {str(e)}"
        )

@app.post("/transcribe/url")
async def transcribe_url(
    audio_url: str,
    language: Optional[str] = "zh"
):
    """
    从 URL 转录音频
    
    参数:
    - audio_url: 音频文件 URL
    - language: 语言代码 (默认: zh)
    
    返回:
    - utterances: 转录结果列表
    - confidence: 准确率
    - model: 使用的模型
    """
    import requests
    
    try:
        # 下载音频文件
        response = requests.get(audio_url, timeout=60)
        response.raise_for_status()
        
        # 从 URL 推断文件扩展名
        file_ext = Path(audio_url).suffix.lower()
        if not file_ext:
            file_ext = '.mp3'  # 默认
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name
        
        # 调用 Paraformer 转录
        result = transcribe_with_paraformer(tmp_file_path)
        
        # 删除临时文件
        os.unlink(tmp_file_path)
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="转录失败"
            )
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "utterances": result['utterances'],
                "confidence": result['confidence'],
                "model": result['model'],
                "audio_duration": result.get('audio_duration', 0)
            }
        })
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"下载音频失败: {str(e)}"
        )
    except Exception as e:
        # 清理临时文件
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"处理错误: {str(e)}"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
