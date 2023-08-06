import attr


@attr.dataclass(slots=True)
class Total:
    jumlah_positif: int
    jumlah_dirawat: int
    jumlah_sembuh: int
    jumlah_meninggal: int
