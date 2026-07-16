from typing import List, Optional
from domain.Medical_record import Medical_record, IMedical_record_repository
from infrastructure.database import Sqlite_database_handler

class Sqlite_medical_record_repository(IMedical_record_repository):

    def __init__(self, db: Sqlite_database_handler):
        self._db: Sqlite_database_handler = db

    def _row_to_medical_record(self, row) -> Medical_record:
        return Medical_record(
            patient_id=row["patient_id"],
            date=row["date"],
            consultation_reason=row["consultation_reason"] or "",
            diagnosis=row["diagnosis"] or "",
            treatment_evolution=row["treatment_evolution"] or "",
            observations=row["observations"] or "",
            is_active=bool(row["is_active"]),
            id=row["id"]
        )

    def get_all_active_medical_records_by_last_name(self, last_name: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.last_name LIKE ? AND mr.is_active = 1
        """
        rows = self._db.execute_query(query, [f"%{last_name}%"])
        return [self._row_to_medical_record(row) for row in rows]

    def get_all_active_medical_records_by_dni(self, dni: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.dni = ? AND mr.is_active = 1
        """
        rows = self._db.execute_query(query, [dni])
        return [self._row_to_medical_record(row) for row in rows]

    def get_all_inactive_medical_records_by_last_name(self, last_name: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.last_name LIKE ? AND mr.is_active = 0
        """
        rows = self._db.execute_query(query, [f"%{last_name}%"])
        return [self._row_to_medical_record(row) for row in rows]

    def get_all_inactive_medical_records_by_dni(self, dni: str) -> List[Medical_record]:
        query = """
            SELECT mr.* FROM medical_records mr 
            INNER JOIN patients p ON mr.patient_id = p.id 
            WHERE p.dni = ? AND mr.is_active = 0
        """
        rows = self._db.execute_query(query, [dni])
        return [self._row_to_medical_record(row) for row in rows]

    def get_medical_record_by_id(self, id: int) -> Optional[Medical_record]:
        query = "SELECT * FROM medical_records WHERE id = ?"
        rows = self._db.execute_query(query, [id])
        if rows:
            return self._row_to_medical_record(rows[0])
        return None

    def create_medical_record(self, new_medical_record: Medical_record) -> bool:
        query = """
            INSERT INTO medical_records (patient_id, date, consultation_reason,
                diagnosis, treatment_evolution, observations, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        params = [
            new_medical_record.patient_id,
            new_medical_record.date,
            new_medical_record.consultation_reason,
            new_medical_record.diagnosis,
            new_medical_record.treatment_evolution,
            new_medical_record.observations
        ]
        return self._db.execute_command(query, params)

    def delete_medical_record_by_id(self, id: int) -> bool:
        query = "UPDATE medical_records SET is_active = 0 WHERE id = ?"
        return self._db.execute_command(query, [id])
