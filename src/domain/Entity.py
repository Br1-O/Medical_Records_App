from abc import ABC

from Value_objects import Id

class Entity(ABC):
    def __init__(self, id=None, is_active=True):
        self._id = Id(id)
        self.isActive = bool(is_active)

    @property
    def id(self):
        return self._id.value