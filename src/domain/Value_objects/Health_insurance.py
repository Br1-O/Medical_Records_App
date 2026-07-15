from Value_objects import Value_object
from Text_with_range import Text_with_range

class Health_insurance(Value_object):
    """Engloba la lógica condicional de la obra social y su número de afiliado."""
    def __init__(self, has_insurance, name, affiliate_number):
        self.has_insurance = bool(has_insurance)
        
        if self.has_insurance:
            # Obligatorios si posee_obra_social = 1
            self.name = Text_with_range(name, "Obra social", 2, 50, required=True).value
            self.affiliate_number = Text_with_range(affiliate_number, "Número de afiliado", 1, 30, required=True).value
        else:
            self.name = ""
            self.affiliate_number = ""

    def __str__(self):
        if self.has_insurance:
            return f"{self.name} (Nº: {self.affiliate_number})"
        return "Sin obra social"