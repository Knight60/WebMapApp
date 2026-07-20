from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import Settings, get_settings
from app.models.schemas import CompositeResponse
from app.services.composite import FALSE_COLOR, TRUE_COLOR, build_monthly_composite, current_month_bound

router = APIRouter(prefix="/api/imagery", tags=["imagery"])

VALID_MODES = {TRUE_COLOR, FALSE_COLOR}


@router.get("/composite", response_model=CompositeResponse)
def get_composite(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    mode: str = Query(...),
    settings: Settings = Depends(get_settings),
) -> CompositeResponse:
    if mode not in VALID_MODES:
        raise HTTPException(422, f"mode must be one of {sorted(VALID_MODES)}")

    if year != settings.target_year:
        raise HTTPException(422, f"year must be {settings.target_year}")

    today = current_month_bound(settings)
    if month > today.month:
        raise HTTPException(422, f"month must be between 1 and {today.month} (current month)")

    result = build_monthly_composite(year, month, mode, settings)
    return CompositeResponse(
        year=year,
        month=month,
        mode=mode,
        tile_url_template=result.tile_url_template,
        has_data=result.has_data,
        data_quality=result.data_quality,
        image_count=result.image_count,
    )
