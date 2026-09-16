FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/course/08_multi-ai-agent-service:/course/09_integrated-deployment-and-operations

WORKDIR /course

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared ./shared
COPY 08_multi-ai-agent-service ./08_multi-ai-agent-service
COPY 09_integrated-deployment-and-operations ./09_integrated-deployment-and-operations

RUN useradd --create-home --uid 10001 agentuser
USER agentuser

CMD ["uvicorn", "backend:app", "--app-dir", "08_multi-ai-agent-service", "--host", "0.0.0.0", "--port", "8000"]
