import attr


@attr.dataclass(slots=True)
class Data:
    id: int
    jumlah_odp: int
    jumlah_pdp: int
    total_spesimen: int
    total_spesimen_negatif: int
