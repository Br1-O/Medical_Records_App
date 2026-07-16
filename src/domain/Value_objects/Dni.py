from .Value_object import Value_object

class Dni(Value_object):
    def __init__(self, value):
        if value is None or not str(value).strip():
            raise ValueError("El DNI es obligatorio.")
        dni_str = str(value).strip()
        if not dni_str.isdigit():
            raise ValueError("El DNI debe contener solo números.")
        if not (7 <= len(dni_str) <= 10):  # Entre 7 y 10 caracteres
            raise ValueError("El DNI debe tener entre 7 y 10 dígitos.")
        self.value = dni_str

    def __str__(self):
        return self.value