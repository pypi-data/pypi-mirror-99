import attr
from datetime import datetime
from typing import List, Optional

from . import Penambahan
from . import Harian
from . import Total


@attr.dataclass(slots=True)
class Update:
    penambahan: Penambahan
    harian: List[Harian]
    total: Total

    def __attrs_post_init__(self) -> None:
        self._today: Optional[datetime] = None

    @property
    def today(self) -> Optional[Harian]:
        if self._today:
            return self._today
        now = datetime.date()
        for harian in self.harian:
            if harian.datetime.date() == now:
                self._today = harian
                break
        return self._today
