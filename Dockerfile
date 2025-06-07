# 使用 Python 瘦版映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝相依套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製其他檔案進容器
COPY . .

# 啟動服務
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
