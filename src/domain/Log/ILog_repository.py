from abc import ABC, abstractmethod
from typing import List
from domain.Log import Log
from domain.Entity import Entity

class ILog_repository(ABC):

    @abstractmethod
    def get_logs_by_entity(self, entity: Entity) -> List[Log]:
        """Devuelve la bitácora de auditoría asociada a una entidad específica."""
        pass

    @abstractmethod
    def get_logs_by_action(self, action: str) -> List[Log]:
        """Devuelve los logs filtrados por un tipo de acción/operación."""
        pass

    @abstractmethod
    def get_all_logs(self) -> List[Log]:
        """Devuelve el historial completo de auditoría del sistema."""
        pass

    @abstractmethod
    def create_log(self, new_log: Log) -> bool:
        """Registra un nuevo evento de auditoría en la base de datos."""
        pass