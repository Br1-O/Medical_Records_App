from Value_object import Value_object


class Text_with_range(Value_object):
    """Value object genérico para textos con límites de caracteres."""
    def __init__(self, value, field_name, min_len, max_len, required=True):
        if required and (value is None or not str(value).strip()):
            raise ValueError(f"El campo '{field_name}' es obligatorio.")[cite: 1]
        
        val_str = str(value).strip() if value is not None else ""
        if val_str:
            if len(val_str) < min_len or len(val_str) > max_len:
                raise ValueError(
                    f"El campo '{field_name}' debe tener entre {min_len} y {max_len} caracteres."[cite: 1]
                )
        self.value = val_str

    def __str__(self):
        return self.value