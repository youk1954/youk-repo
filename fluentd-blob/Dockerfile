FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY upload_to_blob.py /app/upload_to_blob.py

# 로그가 바로 나오도록
ENV PYTHONUNBUFFERED=1

# 기본 실행: 업로더 시작
CMD ["python", "/app/upload_to_blob.py"]
