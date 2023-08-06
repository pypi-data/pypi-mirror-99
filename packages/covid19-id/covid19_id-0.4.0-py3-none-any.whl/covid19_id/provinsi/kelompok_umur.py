import attr

from covid19_id.utils import ValueInt


@attr.dataclass(slots=True)
class KelompokUmur:
    key: str
    doc_count: int
    usia: ValueInt
