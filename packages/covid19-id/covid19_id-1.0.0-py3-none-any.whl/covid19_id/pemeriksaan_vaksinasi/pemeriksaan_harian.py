import attr

from covid19_id.utils import ValueInt


@attr.dataclass(slots=True)
class PemeriksaanHarian:
    key_as_string: str
    key: int
    doc_count: int
    jumlah_spesimen_pcr_tcm: ValueInt
    jumlah_spesimen_antigen: ValueInt
    jumlah_orang_antigen: ValueInt
    jumlah_orang_pcr_tcm: ValueInt
    jumlah_spesimen_pcr_tcm_kum: ValueInt
    jumlah_spesimen_antigen_kum: ValueInt
    jumlah_orang_pcr_tcm_kum: ValueInt
    jumlah_orang_antigen_kum: ValueInt
