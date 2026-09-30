# ---------- Etapa 1: compilar el frontend ----------
FROM node:22-alpine AS frontend

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build


# ---------- Etapa 2: servidor Python ----------
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # La base de datos vive en el volumen persistente montado en /data.
    BALANCEADOR_DB=/data/jugadores.db \
    BALANCEADOR_FRONTEND_DIST=/app/frontend/dist

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install ".[produccion]"

COPY --from=frontend /frontend/dist ./frontend/dist

# Railway define PORT; en local se usa 8000.
CMD uvicorn balanceador_equipos.backend.produccion:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --proxy-headers \
    --forwarded-allow-ips "*"
