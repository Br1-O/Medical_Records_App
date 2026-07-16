from datetime import datetime
import re
from .Value_object import Value_object

class Date(Value_object):
    def __init__(self, value, field_name="Fecha", allow_future=False):
        if value is None or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        
        date_val = str(value).strip()
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date_val):
            raise ValueError(f"El campo '{field_name}' debe tener formato YYYY-MM-DD.")
        
        try:
            dt = datetime.strptime(date_val, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"La fecha en '{field_name}' no corresponde a un día de calendario válido.")
        
        if dt.year < 1900 or dt.year > 2100:
            raise ValueError(f"El año en '{field_name}' debe estar entre 1900 y 2100.")
        
        if not allow_future and dt.date() > datetime.now().date():
            raise ValueError(f"La fecha en '{field_name}' no puede ser mayor a la fecha actual.")
            
        self.value = date_val

    def __str__(self):
        return self.value