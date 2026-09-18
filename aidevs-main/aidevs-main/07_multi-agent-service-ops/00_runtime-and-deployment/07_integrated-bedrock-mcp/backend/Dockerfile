FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY mcp_probe.py .
COPY skills ./skills
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
