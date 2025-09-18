FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /logs && chmod 777 /logs
EXPOSE 8080
CMD ["python", "app.py"]
