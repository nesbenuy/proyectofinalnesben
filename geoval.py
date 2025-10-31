import re

# Acepta decimal (ej. -34.903) o DMS (ej. 34°54'11.2"S)
_DEC_OR_DMS = re.compile(
    r'^\s*([+-]?\d+(?:\.\d+)?)\s*$'
    r'|^\s*([0-9]{1,3})[°\s]\s*([0-9]{1,2})[\'’]\s*([0-9]{1,2}(?:\.\d+)?)[\"”]?\s*([NSEW])\s*$',
    re.IGNORECASE
)

def _parse_common(txt):
    if txt is None:
        return None
    s = str(txt).strip()
    m = _DEC_OR_DMS.match(s)
    if not m:
        return None
    if m.group(1) is not None:  # decimal
        try:
            return float(m.group(1)), None
        except ValueError:
            return None
    # DMS
    deg = float(m.group(2)); minu = float(m.group(3)); sec = float(m.group(4)); hemi = m.group(5).upper()
    val = deg + minu/60.0 + sec/3600.0
    return val, hemi

def parse_lat(txt):
    r = _parse_common(txt)
    if r is None:
        return None
    val, hemi = r
    if hemi in ("S",):
        val = -val
    if hemi in ("N",):
        val = +val
    return round(val, 6) if -90.0 <= val <= 90.0 else None

def parse_lon(txt):
    r = _parse_common(txt)
    if r is None:
        return None
    val, hemi = r
    if hemi in ("W",):
        val = -val
    if hemi in ("E",):
        val = +val
    return round(val, 6) if -180.0 <= val <= 180.0 else None