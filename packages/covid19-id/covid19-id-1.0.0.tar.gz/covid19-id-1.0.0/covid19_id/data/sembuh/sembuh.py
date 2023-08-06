import attr

from . import SembuhKondisiPenyerta
from . import SembuhJenisKelamin
from . import SembuhKelompokUmur
from . import SembuhGejala


@attr.dataclass(slots=True)
class Sembuh:
    kondisi_penyerta: SembuhKondisiPenyerta
    jenis_kelamin: SembuhJenisKelamin
    kelompok_umur: SembuhKelompokUmur
    gejala: SembuhGejala
