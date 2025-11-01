"""
geoval.py
----------
Utilidades de geocodificación y validación de coordenadas.
Acepta formatos decimales y DMS (grados, minutos, segundos) con o sin símbolos,
con hemisferios como sufijo o prefijo y separadores decimales punto o coma.

Funciones públicas:
- parse_lat(texto) -> float|None
- parse_lon(texto) -> float|None

Convenciones:
- Redondeo a 6 decimales.
- Devuelve None si no puede interpretar o si sale de rango.
"""

from __future__ import annotations
import re
from typing import Optional, Tuple

_DEC_SEP = re.compile(r",""")
def _norm(s: str) -> str:
    """Normaliza espacios y separador decimal coma->punto."""
    if s is None:
        return ""
    s = s.strip()
    s = _DEC_SEP.sub(".", s)
    # eliminar espacios intermedios para patrones tipo 34 ° 30 ' S
    s = re.sub(r"\s+", " ", s)
    return s

_HEMI_LAT = {"N": 1, "S": -1}
_HEMI_LON = {"E": 1, "W": -1, "O": -1}  # 'O' por Oeste

# Patrones generales
RE_DECIMAL = re.compile(
    r"""^\s*
        (?P<hemi>[NnSsEeWwOo])?     # hemisferio opcional como prefijo
        \s*
        (?P<val>[+-]?\d+(?:\.\d+)?)
        \s*
        (?P<hemi2>[NnSsEeWwOo])?    # hemisferio opcional como sufijo
        \s*$
    """,
    re.VERBOSE,
)

RE_DMS = re.compile(
    r"""^\s*
        (?P<hemi>[NnSsEeWwOo])?           # prefijo hemisferio
        \s*
        (?P<deg>\d{1,3})                   # grados
        (?:\s*°|\s+)?
        \s*
        (?P<min>\d{1,2})?                  # minutos opcionales
        (?:\s*['’m]|\s+)?
        \s*
        (?P<sec>\d{1,2}(?:\.\d+)?)?        # segundos opcionales
        (?:\s*["”s]|\s+)?
        \s*
        (?P<hemi2>[NnSsEeWwOo])?           # sufijo hemisferio
        \s*$
    """,
    re.VERBOSE,
)


def _pick_hemi(h1: Optional[str], h2: Optional[str]) -> Optional[str]:
    h = (h1 or h2 or "").upper()
    return h or None


def _apply_sign(value: float, hemi: Optional[str], is_lat: bool) -> float:
    if not hemi:
        return value
    if is_lat and hemi in _HEMI_LAT:
        return value * _HEMI_LAT[hemi]
    if not is_lat and hemi in _HEMI_LON:
        return value * _HEMI_LON[hemi]
    return value


def _in_range(val: float, is_lat: bool) -> bool:
    return (-90.0 <= val <= 90.0) if is_lat else (-180.0 <= val <= 180.0)


def _parse_decimal(text: str, is_lat: bool) -> Optional[float]:
    m = RE_DECIMAL.match(text)
    if not m:
        return None
    hemi = _pick_hemi(m.group("hemi"), m.group("hemi2"))
    try:
        value = float(m.group("val"))
    except (TypeError, ValueError):
        return None
    # Si hay hemisferio, domina el signo
    value = abs(value)
    value = _apply_sign(value, hemi, is_lat)
    return round(value, 6) if _in_range(value, is_lat) else None


def _parse_dms(text: str, is_lat: bool) -> Optional[float]:
    m = RE_DMS.match(text)
    if not m:
        return None
    hemi = _pick_hemi(m.group("hemi"), m.group("hemi2"))
    try:
        deg = float(m.group("deg"))
        minutes = float(m.group("min")) if m.group("min") is not None else 0.0
        seconds = float(m.group("sec")) if m.group("sec") is not None else 0.0
    except (TypeError, ValueError):
        return None

    value = deg + minutes / 60.0 + seconds / 3600.0
    value = _apply_sign(value, hemi, is_lat)

    # Si no hay hemisferio y los grados llevaban signo textual (no contemplado en DMS),
    # se asume positivo. El control de rango lo valida igualmente.
    return round(value, 6) if _in_range(value, is_lat) else None


def parse_lat(text: str) -> Optional[float]:
    """
    Convierte una latitud en decimal.
    Acepta:  -34.5   34,5   34°30'S   S34°30'   34 30 0 S
    Devuelve None si no puede interpretarse o sale del rango [-90, 90].
    """
    s = _norm(text)
    return _parse_decimal(s, is_lat=True) or _parse_dms(s, is_lat=True)


def parse_lon(text: str) -> Optional[float]:
    """
    Convierte una longitud en decimal.
    Acepta:  -56.166667   56,166667W   56°10'W   O56°10'
    Devuelve None si no puede interpretarse o sale del rango [-180, 180].
    """
    s = _norm(text)
    return _parse_decimal(s, is_lat=False) or _parse_dms(s, is_lat=False)


# Helper opcional: parseo conjunto
def parse_lat_lon(lat_text: str, lon_text: str) -> Tuple[Optional[float], Optional[float]]:
    """Devuelve una tupla (lat, lon) parseadas o (None, None) si falla ambas."""
    return parse_lat(lat_text), parse_lon(lon_text)
