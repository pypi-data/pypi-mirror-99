import attr

from . import MeninggalKondisiPenyerta
from . import MeninggalJenisKelamin
from . import MeninggalKelompokUmur
from . import MeninggalGejala


@attr.dataclass(slots=True)
class Meninggal:
    kondisi_penyerta: MeninggalKondisiPenyerta
    jenis_kelamin: MeninggalJenisKelamin
    kelompok_umur: MeninggalKelompokUmur
    gejala: MeninggalGejala
