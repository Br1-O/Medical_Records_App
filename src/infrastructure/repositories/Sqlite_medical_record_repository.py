from typing import List, Optional
from domain.Medical_record.Medical_record import Medical_record
from domain.Medical_record.IMedical_record_repository import IMedical_record_repository
from infrastructure.database.Sqlite_database_handler import Sqlite_database_handler

class Sqlite_medical_record_repository(IMedical_record_repository):

    def __init__(self, db: Sqlite_database_handler):
        self._db: Sqlite_database_handler = db

    def get_all_active_medical_records_by_last_name(self, last_name: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.last_name = ? AND mr.active = 1
        """
        rows = self._db.execute_query(query, [last_name])
        return []

    def get_all_active_medical_records_by_dni(self, dni: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.dni = ? AND mr.active = 1
        """
        rows = self._db.execute_query(query, [dni])
        return []

    def get_all_inactive_medical_records_by_last_name(self, last_name: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.last_name = ? AND mr.active = 0
        """
        rows = self._db.execute_query(query, [last_name])
        return []

    def get_all_inactive_medical_records_by_dni(self, dni: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.dni = ? AND mr.active = 0
        """
        rows = self._db.execute_query(query, [dni])
        return []

    def get_medical_record_by_id(self, id: int) -> Optional[Medical_record]:
        query = "SELECT * FROM medical_records WHERE id = ?"
        rows = self._db.execute_query(query, [id])
        if rows:
            # return Medical_record.reconstruct(rows[0])
            pass
        return None

    def create_medical_record(self, new_medical_record: Medical_record) -> bool:
        query = "INSERT INTO medical_records (patient_id, data, active) VALUES (?, ?, 1)"
        params = [new_medical_record.patient_id.value, new_medical_record.data.value]
        return self._db.execute_command(query, params)

    def delete_medical_record_by_id(self, id: int) -> bool:
        # Baja lógica
        query = "UPDATE medical_records SET active = 0 WHERE id = ?"
        return self._db.execute_command(query, [id])