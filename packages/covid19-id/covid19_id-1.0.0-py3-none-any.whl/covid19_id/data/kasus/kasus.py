import attr

from . import KasusKondisiPenyerta
from . import KasusJenisKelamin
from . import KasusKelompokUmur
from . import KasusGejala


@attr.dataclass(slots=True)
class Kasus:
    kondisi_penyerta: KasusKondisiPenyerta
    jenis_kelamin: KasusJenisKelamin
    kelompok_umur: KasusKelompokUmur
    gejala: KasusGejala
