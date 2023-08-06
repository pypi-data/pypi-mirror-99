import attr
from enum import Enum


class JenisKelaminKey(Enum):
    LAKI_LAKI = "LAKI-LAKI"
    PEREMPUAN = "PEREMPUAN"


@attr.dataclass(slots=True)
class JenisKelamin:
    key: JenisKelaminKey
    doc_count: int
