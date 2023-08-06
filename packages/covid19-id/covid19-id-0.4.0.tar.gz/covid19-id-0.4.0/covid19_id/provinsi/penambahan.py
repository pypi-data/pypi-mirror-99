import attr


@attr.dataclass(slots=True)
class Penambahan:
    positif: int
    sembuh: int
    meninggal: int
