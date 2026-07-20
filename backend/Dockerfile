FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
# Frontend build output, published here by `vite build` (frontend/vite.config.ts).
# Run `npm run build` in frontend/ before deploying so this is current.
COPY static ./static

# Cloud Run injects PORT; default matches its convention for local runs.
ENV PORT=8080
EXPOSE 8080

CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
