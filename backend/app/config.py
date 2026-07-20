import os

# Comma-separated list of origins allowed to call this API.
# Defaults to the Vite dev server.
CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

APP_NAME = os.getenv("APP_NAME", "WebMapApp API")
