import re
from .Value_object import Value_object

class Phone(Value_object):
    def __init__(self, value, field_name="Teléfono", required=True):
        if required and (value is None or not str(value).strip()):
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        
        phone_str = str(value).strip() if value is not None else ""
        if phone_str:
            cleaned = re.sub(r'[\s\-\(\)\+]', '', phone_str)
            if not cleaned.isdigit():
                raise ValueError(f"El campo '{field_name}' debe contener solo números y caracteres válidos.")
            if not (8 <= len(phone_str) <= 20):  # Validado contra SRS: Máximo 20 caracteres
                raise ValueError(f"El campo '{field_name}' debe tener entre 8 y 20 caracteres.")
        self.value = phone_str

    def __str__(self):
        return self.value