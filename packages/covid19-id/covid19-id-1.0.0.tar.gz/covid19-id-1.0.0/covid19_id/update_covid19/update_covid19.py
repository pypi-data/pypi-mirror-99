import attr

from . import Data
from . import Update


@attr.dataclass(slots=True)
class UpdateCovid19:
    data: Data
    update: Update
