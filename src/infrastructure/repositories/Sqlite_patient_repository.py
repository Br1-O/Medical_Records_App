from typing import List, Optional
from domain.Patient.Patient import Patient
from domain.Patient.IPatient_repository import IPatient_repository
from infrastructure.database.Sqlite_database_handler import Sqlite_database_handler

class Sqlite_patient_repository(IPatient_repository):

    def __init__(self, db: Sqlite_database_handler):
        self._db: Sqlite_database_handler = db

    def get_patient_by_last_name(self, last_name: str) -> List[Patient]:
        query = "SELECT * FROM patients WHERE last_name = ? AND active = 1"
        rows = self._db.execute_query(query, [last_name])
        # Aquí mapearías las filas a objetos del dominio Patient utilizando sus Value Objects
        # Ejemplo conceptual de retorno: [Patient.reconstruct(row) for row in rows]
        return []

    def get_patient_by_dni(self, dni: str) -> Optional[Patient]:
        query = "SELECT * FROM patients WHERE dni = ? AND active = 1"
        rows = self._db.execute_query(query, [dni])
        if rows:
            # return Patient.reconstruct(rows[0])
            pass
        return None

    def get_all_active_patients(self) -> List[Patient]:
        query = "SELECT * FROM patients WHERE active = 1"
        rows = self._db.execute_query(query)
        return []

    def get_all_inactive_patients(self) -> List[Patient]:
        query = "SELECT * FROM patients WHERE active = 0"
        rows = self._db.execute_query(query)
        return []

    def create_patient(self, new_patient: Patient) -> bool:
        query = "INSERT INTO patients (dni, name, last_name, active) VALUES (?, ?, ?, 1)"
        # Extraes los valores primitivos desde los Value Objects del dominio
        params = [new_patient.dni.value, new_patient.name.value, new_patient.last_name.value]
        return self._db.execute_command(query, params)

    def update_patient(self, updated_patient: Patient) -> bool:
        query = "UPDATE patients SET name = ?, last_name = ? WHERE dni = ?"
        params = [updated_patient.name.value, updated_patient.last_name.value, updated_patient.dni.value]
        return self._db.execute_command(query, params)

    def delete_patient_by_dni(self, dni: str) -> bool:
        # Baja lógica
        query = "UPDATE patients SET active = 0 WHERE dni = ?"
        return self._db.execute_command(query, [dni])