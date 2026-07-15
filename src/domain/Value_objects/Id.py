from Value_object import Value_object;

class Id(Value_object):
    def __init__(self, value):
        if value is not None:
            if not isinstance(value, int) or value <= 0:
                raise ValueError("El ID debe ser un número entero positivo.")
        self.value = value

    def __str__(self):
        return str(self.value) if self.value is not None else ""