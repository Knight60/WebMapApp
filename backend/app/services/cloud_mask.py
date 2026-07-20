import ee

CLOUD_FILTER = 60  # max scene-level cloud % to include in the collection at all
CLD_PRB_THRESH = 40  # s2cloudless probability threshold above which a pixel is masked


def get_s2_sr_cloud_collection(aoi: ee.Geometry, start: str, end: str) -> ee.ImageCollection:
    """Sentinel-2 SR collection joined with s2cloudless cloud probability."""
    s2_sr = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start, end)
        .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", CLOUD_FILTER))
    )
    s2_cloudless = (
        ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
        .filterBounds(aoi)
        .filterDate(start, end)
    )
    join = ee.Join.saveFirst("s2cloudless").apply(
        primary=s2_sr,
        secondary=s2_cloudless,
        condition=ee.Filter.equals(leftField="system:index", rightField="system:index"),
    )
    return ee.ImageCollection(join)


def mask_clouds(image: ee.Image) -> ee.Image:
    cloud_prob = ee.Image(image.get("s2cloudless")).select("probability")
    is_cloud = cloud_prob.gte(CLD_PRB_THRESH).rename("clouds")
    return image.updateMask(is_cloud.Not())
