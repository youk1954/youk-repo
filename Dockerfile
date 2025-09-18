FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# 로그 디렉토리 생성(공유 마운트 경로)
RUN mkdir -p /logs && chmod 777 /logs

EXPOSE 8080
CMD ["python", "app.py"]
