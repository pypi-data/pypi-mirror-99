import attr


@attr.dataclass(slots=True)
class TotalVaksinasi:
    jumlah_vaksinasi_1: int
    jumlah_vaksinasi_2: int
