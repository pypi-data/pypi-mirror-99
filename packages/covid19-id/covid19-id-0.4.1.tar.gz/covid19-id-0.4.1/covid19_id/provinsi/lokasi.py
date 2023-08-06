import attr


@attr.dataclass(slots=True)
class Lokasi:
    lon: float
    lat: float
