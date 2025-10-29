FROM python:3.11-slim as builder

WORKDIR /app

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Устанавливаем только runtime зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Делаем так, чтобы Python находил установленные пакеты
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "7999"]