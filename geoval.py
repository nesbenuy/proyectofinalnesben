"""
geoval.py 
------------------------------------------------
Interpreta coordenadas decimales y DMS (grados, minutos, segundos)
con o sin hemisferio. Si la longitud no especifica hemisferio, asume Oeste (valor negativo).
"""

import re
from typing import Optional, Tuple

_HEMI_LAT = {"N": 1, "S": -1}
_HEMI_LON = {"E": 1, "W": -1, "O": -1}

RE_DECIMAL = re.compile(
    r"""^\s*
        (?P<hemi>[NnSsEeWwOo])?     # hemisferio opcional al inicio
        \s*
        (?P<val>[+-]?\d+(?:\.\d+)?)
        \s*
        (?P<hemi2>[NnSsEeWwOo])?    # hemisferio opcional al final
        \s*$""", re.VERBOSE
)

RE_DMS = re.compile(
    r"""^\s*
        (?P<hemi>[NnSsEeWwOo])?
        \s*
        (?P<deg>\d{1,3})
        (?:\s*°|\s+)?
        \s*
        (?P<min>\d{1,2})?
        (?:\s*['’m]|\s+)?
        \s*
        (?P<sec>\d{1,2}(?:\.\d+)?)?
        (?:\s*["”s]|\s+)?
        \s*
        (?P<hemi2>[NnSsEeWwOo])?
        \s*$""", re.VERBOSE
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
        minutes = float(m.group("min")) if m.group("min") else 0.0
        seconds = float(m.group("sec")) if m.group("sec") else 0.0
    except (TypeError, ValueError):
        return None

    value = deg + minutes / 60.0 + seconds / 3600.0
    value = _apply_sign(value, hemi, is_lat)
    return round(value, 6) if _in_range(value, is_lat) else None


def parse_lat(text: str) -> Optional[float]:
    if not text:
        return None
    text = text.strip().replace(",", ".")
    return _parse_decimal(text, is_lat=True) or _parse_dms(text, is_lat=True)


def parse_lon(text: str) -> Optional[float]:
    if not text:
        return None
    text = text.strip().replace(",", ".")
    result = _parse_decimal(text, is_lat=False) or _parse_dms(text, is_lat=False)
    # Convención local: si no se especifica hemisferio y el valor es positivo, asumimos Oeste (negativo)
    if result is not None and result > 0 and not any(h in text.upper() for h in "EWONSO"):
        result = -abs(result)
    return result


def parse_lat_lon(lat_text: str, lon_text: str) -> Tuple[Optional[float], Optional[float]]:
    return parse_lat(lat_text), parse_lon(lon_text)