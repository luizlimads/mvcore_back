from datetime import datetime
from django.utils import timezone

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
