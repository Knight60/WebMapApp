import tempfile

import ee

from app.config import Settings

_initialized = False


def init_ee(settings: Settings) -> None:
    """Initialize the Earth Engine session using service account credentials.

    Called once at FastAPI startup. Raises if credentials are missing or
    invalid so the app fails fast rather than serving requests against a
    broken EE session.
    """
    global _initialized
    if _initialized:
        return

    if not settings.ee_service_account_email:
        raise RuntimeError("EE_SERVICE_ACCOUNT_EMAIL is not set")

    key_path = settings.ee_private_key_path
    if settings.ee_private_key_json:
        # Cloud Run secret-as-env-var case: write the JSON to a temp file,
        # since ee.ServiceAccountCredentials expects a file path.
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        tmp.write(settings.ee_private_key_json)
        tmp.close()
        key_path = tmp.name

    if not key_path:
        raise RuntimeError(
            "Neither EE_PRIVATE_KEY_PATH nor EE_PRIVATE_KEY_JSON is set"
        )

    credentials = ee.ServiceAccountCredentials(settings.ee_service_account_email, key_path)
    ee.Initialize(credentials, project=settings.gcp_project_id or None)
    _initialized = True


def is_initialized() -> bool:
    return _initialized
