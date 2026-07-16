from domain.Entity import Entity
from domain.Value_objects import Datetime, Id;

class Log(Entity):
    def __init__(self, 
                 timestamp, 
                 operation, 
                 affected_record_id,
                 is_active=True, 
                 id=None):
        super().__init__(id=id, is_active=is_active)
        
        self._timestamp = Datetime(timestamp)
        
        # Operaciones limitadas a las definidas por el SRS
        allowed_operations = [
            "Alta Paciente", 
            "Modificación Paciente", 
            "Baja Paciente", 
            "Alta Historial", 
            "Anulación"
        ]
        if operation not in allowed_operations:
            raise ValueError(f"Operación '{operation}' inválida. Operaciones válidas: {allowed_operations}")
            
        self._operation = operation
        self._affectedRecordId = Id(affected_record_id)
        if self._affectedRecordId.value is None:
            raise ValueError("El id del registro afectado en auditoría es obligatorio.")

    @property
    def timestamp(self): return self._timestamp.value
    
    @property
    def operation(self): return self._operation
    
    @property
    def affectedRecordId(self): return self._affectedRecordId.value