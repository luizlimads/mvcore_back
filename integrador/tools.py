from datetime import datetime, date
from django.utils import timezone
import re

DEFAULT_IMPORT_DATE = date(2015, 1, 1)

def fix_iso_datetime(dt_str: str) -> str:
    """
    Normaliza datas ISO para:
    YYYY-MM-DDTHH:MM:SS.mmmmmm
    """
    # Caso: só data (YYYY-MM-DD)
    if len(dt_str) == 10:
        return f"{dt_str}T00:00:00.000000"

    # Garante separador T
    if "T" not in dt_str:
        dt_str = dt_str.replace(" ", "T")

    # Se não tem microssegundos
    if "." not in dt_str:
        return f"{dt_str}.000000"

    # Normaliza microssegundos
    base, micro = dt_str.split(".", 1)
    micro = micro[:6].ljust(6, "0")

    return f"{base}.{micro}"

def parse_dt(dt_str: str):
    if not dt_str:
        return None

    dt_str = fix_iso_datetime(dt_str)

    dt = datetime.fromisoformat(dt_str)
    dt = dt.replace(microsecond=0)

    return timezone.make_aware(dt)

def clean_doc(doc: str) -> str:
    return re.sub(r'[^A-Za-z0-9]', '', doc)

def deep_get(dado, path, default=None):
    for key in path.split("."):
        if isinstance(dado, dict):
            dado = dado.get(key, default)
        else:
            return default
    return dado