from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Medical_record.Medical_record import MedicalRecord

class IMedical_record_repository(ABC):

    @abstractmethod
    def get_all_active_medical_records_by_last_name(self, last_name: str) -> List[MedicalRecord]:
        """Devuelve historias clínicas activas buscando por apellido del paciente."""
        pass

    @abstractmethod
    def get_all_active_medical_records_by_dni(self, dni: str) -> List[MedicalRecord]:
        """Devuelve historias clínicas activas buscando por DNI del paciente."""
        pass

    @abstractmethod
    def get_all_inactive_medical_records_by_last_name(self, last_name: str) -> List[MedicalRecord]:
        """Devuelve historias clínicas inactivas buscando por apellido del paciente."""
        pass

    @abstractmethod
    def get_all_inactive_medical_records_by_dni(self, dni: str) -> List[MedicalRecord]:
        """Devuelve historias clínicas inactivas buscando por DNI del paciente."""
        pass

    @abstractmethod
    def get_medical_record_by_id(self, id: int) -> Optional[MedicalRecord]:
        """Devuelve una consulta/ficha médica específica por su ID."""
        pass

    @abstractmethod
    def create_medical_record(self, new_medical_record: MedicalRecord) -> bool:
        """Registra una nueva evolución o consulta en la historia clínica."""
        pass

    @abstractmethod
    def delete_medical_record_by_id(self, id: int) -> bool:
        """Realiza la baja lógica (anulación) de una ficha médica por ID."""
        pass