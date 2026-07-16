import re
from .Value_object import Value_object

class Email(Value_object):
    def __init__(self, value):
        email_str = str(value).strip() if value is not None else ""
        if email_str:
            pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email_str):
                raise ValueError("El formato del email no es válido.")
            if len(email_str) > 100:  # Validado contra SRS: Máximo 100 caracteres
                raise ValueError("El email no puede exceder 100 caracteres.")
        self.value = email_str

    def __str__(self):
        return self.value