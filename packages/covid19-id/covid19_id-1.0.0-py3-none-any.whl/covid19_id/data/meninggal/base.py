import attr
from typing import List

from covid19_id.data import DataKeyDoc


@attr.dataclass(slots=True)
class BaseMeninggal:
    list_data: List[DataKeyDoc]
