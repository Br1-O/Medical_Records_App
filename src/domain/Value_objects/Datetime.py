from datetime import datetime
import re
from .Value_object import Value_object

class Datetime(Value_object):
    """Para Logs y marcas de tiempo del sistema."""
    def __init__(self, value):
        if value is None or not str(value).strip():
            raise ValueError("La fecha y hora es obligatoria.")
        
        dt_val = str(value).strip()
        dt_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        if not re.match(dt_pattern, dt_val):
            raise ValueError("El formato de fecha y hora debe ser YYYY-MM-DD HH:MM:SS.")
        
        try:
            datetime.strptime(dt_val, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("La marca temporal provista no es válida.")
            
        self.value = dt_val

    def __str__(self):
        return self.value