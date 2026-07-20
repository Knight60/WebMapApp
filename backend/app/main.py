import mimetypes
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, CORS_ORIGINS

# Not in Python's default table; without this .geojson is served as octet-stream.
mimetypes.add_type("application/geo+json", ".geojson")

app = FastAPI(title=APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def api_root():
    return {"name": APP_NAME, "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Built frontend, published here by `vite build` (see frontend/vite.config.ts).
# Mounted last so it only handles paths the API routes above didn't claim.
WEB_ROOT = Path(__file__).resolve().parent.parent / "static"

if WEB_ROOT.is_dir():
    app.mount("/", StaticFiles(directory=WEB_ROOT, html=True), name="web")
