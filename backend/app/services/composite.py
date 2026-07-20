import datetime as dt
from calendar import monthrange
from dataclasses import dataclass

import ee

from app.config import Settings
from app.services.cache import TTLCache
from app.services.cloud_mask import get_s2_sr_cloud_collection, mask_clouds

TRUE_COLOR = "true_color"
FALSE_COLOR = "false_color"

VIS_PARAMS = {
    TRUE_COLOR: {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000, "gamma": 1.1},
    FALSE_COLOR: {"bands": ["B8", "B4", "B3"], "min": 0, "max": 4000, "gamma": 1.1},
}

# Widen the window by this many days beyond the calendar month if the strict
# month yields too few source images (monsoon months can be nearly cloud-free-less).
SPARSE_IMAGE_THRESHOLD = 3
FALLBACK_WINDOW_DAYS = 10

_cache = TTLCache()


@dataclass
class CompositeResult:
    tile_url_template: str | None
    has_data: bool
    data_quality: str  # "ok" | "sparse" | "none"
    image_count: int


def _thailand_geometry() -> ee.Geometry:
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0")
    return countries.filter(ee.Filter.eq("ADM0_NAME", "Thailand")).geometry()


def current_month_bound(settings: Settings) -> dt.date:
    if settings.current_date_override:
        return dt.date.fromisoformat(settings.current_date_override)
    return dt.date.today()


def _month_date_range(year: int, month: int, settings: Settings) -> tuple[str, str]:
    start = dt.date(year, month, 1)
    last_day = monthrange(year, month)[1]
    natural_end = dt.date(year, month, last_day) + dt.timedelta(days=1)
    today = current_month_bound(settings)
    end = min(natural_end, today + dt.timedelta(days=1))
    return start.isoformat(), end.isoformat()


def _widen_range(start: str, end: str) -> tuple[str, str]:
    start_d = dt.date.fromisoformat(start) - dt.timedelta(days=FALLBACK_WINDOW_DAYS)
    end_d = dt.date.fromisoformat(end) + dt.timedelta(days=FALLBACK_WINDOW_DAYS)
    return start_d.isoformat(), end_d.isoformat()


def build_monthly_composite(year: int, month: int, mode: str, settings: Settings) -> CompositeResult:
    cache_key = (year, month, mode)
    is_current_month = (year, month) == (
        current_month_bound(settings).year,
        current_month_bound(settings).month,
    )
    ttl = 900 if is_current_month else 3000  # 15 min vs 50 min

    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    aoi = _thailand_geometry()
    start, end = _month_date_range(year, month, settings)

    collection = get_s2_sr_cloud_collection(aoi, start, end)
    image_count = collection.size().getInfo()
    data_quality = "ok"

    if image_count < SPARSE_IMAGE_THRESHOLD:
        start, end = _widen_range(start, end)
        collection = get_s2_sr_cloud_collection(aoi, start, end)
        image_count = collection.size().getInfo()
        data_quality = "sparse"

    if image_count == 0:
        result = CompositeResult(tile_url_template=None, has_data=False, data_quality="none", image_count=0)
        _cache.set(cache_key, result, ttl)
        return result

    composite = collection.map(mask_clouds).median().clip(aoi)
    vis = VIS_PARAMS[mode]
    map_id = ee.Image(composite).getMapId(vis)

    result = CompositeResult(
        tile_url_template=map_id["tile_fetcher"].url_format,
        has_data=True,
        data_quality=data_quality,
        image_count=image_count,
    )
    _cache.set(cache_key, result, ttl)
    return result
