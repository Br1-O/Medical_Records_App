from .Value_object import Value_object

class Gender(Value_object):
    def __init__(self, value):
        if value is None or not str(value).strip():
            raise ValueError("El género es obligatorio.")
        
        val_str = str(value).strip()
        allowed = ["Masculino", "Femenino", "Otro"]
        if val_str not in allowed:
            raise ValueError(f"El género debe ser uno de los siguientes: {', '.join(allowed)}.")
        self.value = val_str

    def __str__(self):
        return self.value