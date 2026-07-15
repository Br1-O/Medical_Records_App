import re
from Value_objects import Value_object
from Text_with_range import Text_with_range


class Name(Value_object):
    def __init__(self, value, field_name="Nombre"):
        # Regla: Entre 2 y 50 caracteres. Solo letras y espacios/apóstrofes
        text_vo = Text_with_range(value, field_name, 2, 50, required=True)
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ'\s]+$", text_vo.value):
            raise ValueError(f"El campo '{field_name}' solo debe contener letras.")
        self.value = text_vo.value

    def __str__(self):
        return self.value