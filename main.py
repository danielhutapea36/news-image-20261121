#!/usr/bin/env python3
"""Pindahkan gambar berita (entry.png) ke folder keluaran make.fun.

Tugas skrip ini sempit dan disengaja: ambil berkas entry.png yang ada
di samping skrip, pastikan berkas itu benar-benar sebuah PNG, salin
isinya byte demi byte ke folder keluaran, lalu periksa ulang salinan
tersebut sebelum melaporkan keberhasilan.

Tidak ada unduhan, tidak ada angka acak, tidak ada jam atau tanggal,
dan tidak ada pustaka di luar pustaka bawaan Python.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path


TANDA_PNG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
NAMA_GAMBAR = "entry.png"
FOLDER_KELUARAN_BAWAAN = "/output"


def cari_gambar() -> Path:
    """Kembalikan alamat entry.png yang duduk di samping skrip ini."""
    return Path(__file__).resolve().parent / NAMA_GAMBAR


def folder_keluaran() -> Path:
    """Kembalikan folder keluaran dari lingkungan, atau /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FOLDER_KELUARAN_BAWAAN))


def muat_dan_periksa(alamat: Path) -> bytes:
    """Baca berkas gambar dan pastikan delapan byte awalnya tanda PNG."""
    isi = alamat.read_bytes()
    if isi[: len(TANDA_PNG)] != TANDA_PNG:
        raise ValueError(
            f"isi {alamat.name} bukan PNG: delapan byte awalnya tidak cocok"
        )
    return isi


def tulis_salinan(isi: bytes, tujuan: Path) -> Path:
    """Tulis isi persis apa adanya ke dalam folder tujuan."""
    tujuan.mkdir(parents=True, exist_ok=True)
    salinan = tujuan / NAMA_GAMBAR
    salinan.write_bytes(isi)
    return salinan


def periksa_salinan(isi_asli: bytes, salinan: Path) -> None:
    """Baca kembali salinan dan pastikan isinya sama persis dengan sumber."""
    ulang = salinan.read_bytes()
    if ulang[: len(TANDA_PNG)] != TANDA_PNG:
        raise ValueError(f"salinan di {salinan} rusak: tanda PNG-nya hilang")
    if len(ulang) != len(isi_asli):
        raise ValueError(
            f"salinan di {salinan} ukurannya {len(ulang)} byte, "
            f"padahal sumbernya {len(isi_asli)} byte"
        )
    if ulang != isi_asli:
        raise ValueError(f"salinan di {salinan} isinya berbeda dari sumber")


def sidik_jari(isi: bytes) -> str:
    """Kembalikan sidik sha256 dari isi berkas sebagai teks heksadesimal."""
    return hashlib.sha256(isi).hexdigest()


def jalankan() -> int:
    """Jalankan alur salin dan laporkan hasilnya; 0 bila berhasil."""
    try:
        sumber = cari_gambar()
        if not sumber.is_file():
            print(
                "Gagal menyalin gambar: entry.png tidak ditemukan di "
                f"{sumber.parent} — pastikan berkas gambarnya ada di "
                "samping main.py.",
                file=sys.stderr,
            )
            return 1
        isi = muat_dan_periksa(sumber)
        salinan = tulis_salinan(isi, folder_keluaran())
        periksa_salinan(isi, salinan)
    except (OSError, ValueError) as galat:
        print(f"Gagal menyalin gambar: {galat}", file=sys.stderr)
        return 1
    print(f"Tersalin {len(isi)} byte ke {salinan} (sha256 {sidik_jari(isi)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(jalankan())
