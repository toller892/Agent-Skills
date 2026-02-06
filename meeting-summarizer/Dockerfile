FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建 API 专用的 requirements
RUN echo "fastapi>=0.104.0" >> requirements_api.txt && \
    echo "uvicorn[standard]>=0.24.0" >> requirements_api.txt && \
    echo "python-multipart>=0.0.6" >> requirements_api.txt && \
    echo "funasr>=1.0.0" >> requirements_api.txt && \
    echo "modelscope>=1.9.0" >> requirements_api.txt && \
    echo "torch>=2.0.0" >> requirements_api.txt && \
    echo "torchaudio>=2.0.0" >> requirements_api.txt && \
    echo "requests>=2.31.0" >> requirements_api.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements_api.txt

# 复制应用代码
COPY transcribe_multi_model.py .
COPY api_server.py .

# 预下载模型（可选，加快首次启动）
# RUN python -c "from funasr import AutoModel; AutoModel(model='paraformer-zh', vad_model='fsmn-vad', punc_model='ct-punc', spk_model='cam++', device='cpu')"

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 启动服务
CMD ["python", "api_server.py"]
