FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HF_HOME=/app/vector_db/huggingface

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/vector_db /app/vector_db/huggingface

EXPOSE 8000

CMD ["sh", "-c", "uvicorn chat.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
