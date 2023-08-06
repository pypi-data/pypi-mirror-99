import attr

from . import PerawatanKondisiPenyerta
from . import PerawatanJenisKelamin
from . import PerawatanKelompokUmur
from . import PerawatanGejala


@attr.dataclass(slots=True)
class Perawatan:
    kondisi_penyerta: PerawatanKondisiPenyerta
    jenis_kelamin: PerawatanJenisKelamin
    kelompok_umur: PerawatanKelompokUmur
    gejala: PerawatanGejala
