from pydantic import BaseModel


class CompositeResponse(BaseModel):
    year: int
    month: int
    mode: str
    tile_url_template: str | None
    has_data: bool
    data_quality: str
    image_count: int
