import attr
from datetime import date
from typing import List

from . import Provinsi


@attr.dataclass(slots=True)
class DataProvinsi:
    last_date: date
    current_data: int
    missing_data: int
    tanpa_provinsi: int
    list_data: List[Provinsi]
