class Value_object:
    """Clase base para todos los Value Objects para proveer igualdad estructural."""
    def __eq__(self, other):
        if not isinstance(other, Value_object):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))