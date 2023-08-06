import attr
from datetime import date

from . import Kasus
from . import Sembuh
from . import Meninggal
from . import Perawatan


@attr.dataclass(slots=True)
class Data:
    last_update: date
    kasus: Kasus
    sembuh: Sembuh
    meninggal: Meninggal
    perawatan: Perawatan
