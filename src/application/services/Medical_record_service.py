from typing import List, Optional
from domain.Medical_record.Medical_record import Medical_record
from domain.Medical_record.IMedical_record_repository import IMedical_record_repository

class Medical_record_service:

    def __init__(self, medical_record_repository: IMedical_record_repository):
        self._medical_record_repository = medical_record_repository

    def get_all_active_medical_records_by_last_name_use_case(self, last_name: str) -> List[Medical_record]:
        return self._medical_record_repository.get_all_active_medical_records_by_last_name(last_name)

    def get_all_active_medical_records_by_dni_use_case(self, dni: str) -> List[Medical_record]:
        return self._medical_record_repository.get_all_active_medical_records_by_dni(dni)

    def get_all_inactive_medical_records_by_last_name_use_case(self, last_name: str) -> List[Medical_record]:
        return self._medical_record_repository.get_all_inactive_medical_records_by_last_name(last_name)

    def get_all_inactive_medical_records_by_dni_use_case(self, dni: str) -> List[Medical_record]:
        return self._medical_record_repository.get_all_inactive_medical_records_by_dni(dni)

    def get_medical_record_by_id_use_case(self, id: int) -> Optional[Medical_record]:
        return self._medical_record_repository.get_medical_record_by_id(id)

    def create_medical_record_use_case(self, new_medical_record: Medical_record) -> bool:
        return self._medical_record_repository.create_medical_record(new_medical_record)

    def delete_medical_record_by_id_use_case(self, id: int) -> bool:
        return self._medical_record_repository.delete_medical_record_by_id(id)