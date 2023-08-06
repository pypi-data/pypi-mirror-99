import attr

from covid19_id.utils import ValueInt


@attr.dataclass(slots=True)
class VaksinasiHarian:
    key_as_string: str
    key: int
    doc_count: int
    jumlah_vaksinasi_2: ValueInt
    jumlah_vaksinasi_1: ValueInt
    jumlah_jumlah_vaksinasi_1_kum: ValueInt
    jumlah_jumlah_vaksinasi_2_kum: ValueInt
