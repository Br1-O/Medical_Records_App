from typing import List, Optional
from domain.Patient.Patient import Patient
from domain.Patient.IPatient_repository import IPatient_repository

class Patient_service:
    
    def __init__(self, patient_repository: IPatient_repository):
        self._patient_repository = patient_repository

    def get_patient_by_last_name_use_case(self, last_name: str) -> List[Patient]:
        return self._patient_repository.get_patient_by_last_name(last_name)

    def get_patient_by_dni_use_case(self, dni: str) -> Optional[Patient]:
        return self._patient_repository.get_patient_by_dni(dni)

    def get_all_active_patients_use_case(self) -> List[Patient]:
        return self._patient_repository.get_all_active_patients()

    def get_all_inactive_patients_use_case(self) -> List[Patient]:
        return self._patient_repository.get_all_inactive_patients()

    def create_patient_use_case(self, new_patient: Patient) -> bool:
        return self._patient_repository.create_patient(new_patient)

    def update_patient_use_case(self, updated_patient: Patient) -> bool:
        return self._patient_repository.update_patient(updated_patient)

    def delete_patient_by_dni_use_case(self, dni: str) -> bool:
        return self._patient_repository.delete_patient_by_dni(dni)