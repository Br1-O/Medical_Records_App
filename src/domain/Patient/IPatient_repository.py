from abc import ABC, abstractmethod
from typing import List, Optional
from Patient import Patient

class IPatient_repository(ABC):
    
    @abstractmethod
    def get_patient_by_last_name(self, last_name: str) -> List[Patient]:
        """Devuelve una lista de pacientes que coincidan con el apellido."""
        pass

    @abstractmethod
    def get_patient_by_dni(self, dni: str) -> Optional[Patient]:
        """Devuelve un paciente por su DNI o None si no existe."""
        pass

    @abstractmethod
    def get_all_active_patients(self) -> List[Patient]:
        """Devuelve todos los pacientes activos."""
        pass

    @abstractmethod
    def get_all_inactive_patients(self) -> List[Patient]:
        """Devuelve todos los pacientes inactivos."""
        pass

    @abstractmethod
    def create_patient(self, new_patient: Patient) -> bool:
        """Persiste un nuevo paciente. Devuelve True si fue exitoso."""
        pass

    @abstractmethod
    def update_patient(self, updated_patient: Patient) -> bool:
        """Actualiza los datos de un paciente existente. Devuelve True si fue exitoso."""
        pass

    @abstractmethod
    def delete_patient_by_dni(self, dni: str) -> bool:
        """Realiza la baja lógica (desactiva) de un paciente usando su DNI."""
        pass