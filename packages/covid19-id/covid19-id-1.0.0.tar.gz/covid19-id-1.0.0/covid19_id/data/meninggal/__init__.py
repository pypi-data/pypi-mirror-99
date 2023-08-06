from .base import BaseMeninggal
from .kondisi_penyerta import MeninggalKondisiPenyerta
from .jenis_kelamin import MeninggalJenisKelamin
from .kelompok_umur import MeninggalKelompokUmur
from .gejala import MeninggalGejala
from .meninggal import Meninggal


__all__ = [
    "BaseMeninggal",
    "Meninggal",
    "MeninggalGejala",
    "MeninggalJenisKelamin",
    "MeninggalKelompokUmur",
    "MeninggalKondisiPenyerta",
]
