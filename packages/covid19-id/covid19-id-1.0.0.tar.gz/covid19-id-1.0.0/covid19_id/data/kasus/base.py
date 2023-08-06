import attr
from typing import List

from covid19_id.data import DataKeyDoc


@attr.dataclass(slots=True)
class BaseKasus:
    current_data: int
    missing_data: float
    list_data: List[DataKeyDoc]
