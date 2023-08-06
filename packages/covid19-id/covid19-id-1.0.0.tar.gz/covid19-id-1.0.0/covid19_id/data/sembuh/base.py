import attr
from typing import List

from covid19_id.data import DataKeyDoc


@attr.dataclass(slots=True)
class BaseSembuh:
    list_data: List[DataKeyDoc]
