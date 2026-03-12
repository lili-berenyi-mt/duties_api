FROM python:3.12-slim
WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/ ./frontend/
EXPOSE 5000
CMD ["python", "-m", "frontend.app"]
