from typing import List, Optional
from domain.Patient import Patient, IPatient_repository
from infrastructure.database import Sqlite_database_handler

class Sqlite_patient_repository(IPatient_repository):

    def __init__(self, db: Sqlite_database_handler):
        self._db: Sqlite_database_handler = db

    def _row_to_patient(self, row) -> Patient:
        return Patient(
            name=row["name"],
            last_name=row["last_name"],
            dni=row["dni"],
            birth_date=row["birth_date"] or "",
            gender=row["gender"] or "Otro",
            phone=row["phone"] or "",
            emergency_contact=row["emergency_contact"] or "",
            address=row["address"] or "",
            secondary_phone=row["secondary_phone"] or "",
            email=row["email"] or "",
            city=row["city"] or "Mar del Plata",
            country=row["country"] or "Argentina",
            has_health_insurance=bool(row["has_health_insurance"]),
            health_insurance_name=row["health_insurance_name"] or "",
            health_insurance_number=row["health_insurance_number"] or "",
            medical_observations=row["medical_observations"] or "",
            is_active=bool(row["is_active"]),
            id=row["id"]
        )

    def get_patient_by_last_name(self, last_name: str) -> List[Patient]:
        query = "SELECT * FROM patients WHERE last_name LIKE ? AND is_active = 1"
        rows = self._db.execute_query(query, [f"%{last_name}%"])
        return [self._row_to_patient(row) for row in rows]

    def get_patient_by_dni(self, dni: str) -> Optional[Patient]:
        query = "SELECT * FROM patients WHERE dni = ?"
        rows = self._db.execute_query(query, [dni])
        if rows:
            return self._row_to_patient(rows[0])
        return None

    def get_all_active_patients(self) -> List[Patient]:
        query = "SELECT * FROM patients WHERE is_active = 1"
        rows = self._db.execute_query(query)
        return [self._row_to_patient(row) for row in rows]

    def get_all_inactive_patients(self) -> List[Patient]:
        query = "SELECT * FROM patients WHERE is_active = 0"
        rows = self._db.execute_query(query)
        return [self._row_to_patient(row) for row in rows]

    def create_patient(self, new_patient: Patient) -> bool:
        query = """
            INSERT INTO patients (dni, name, last_name, birth_date, gender, phone,
                emergency_contact, address, secondary_phone, email, city, country,
                has_health_insurance, health_insurance_name, health_insurance_number,
                medical_observations, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        params = [
            new_patient.dni,
            new_patient.name,
            new_patient.last_name,
            new_patient.birth_date,
            new_patient.gender,
            new_patient.phone,
            new_patient.emergency_contact,
            new_patient.address,
            new_patient.secondary_phone,
            new_patient.email,
            new_patient.city,
            new_patient.country,
            1 if new_patient.has_health_insurance else 0,
            new_patient.health_insurance_name,
            new_patient.health_insurance_number,
            new_patient.medical_observations
        ]
        return self._db.execute_command(query, params)

    def update_patient(self, updated_patient: Patient) -> bool:
        query = """
            UPDATE patients SET name = ?, last_name = ?, dni = ?, birth_date = ?, gender = ?,
                phone = ?, emergency_contact = ?, address = ?, secondary_phone = ?,
                email = ?, city = ?, country = ?, has_health_insurance = ?,
                health_insurance_name = ?, health_insurance_number = ?,
                medical_observations = ?, is_active = ?
            WHERE id = ?
        """
        params = [
            updated_patient.name,
            updated_patient.last_name,
            updated_patient.dni,
            updated_patient.birth_date,
            updated_patient.gender,
            updated_patient.phone,
            updated_patient.emergency_contact,
            updated_patient.address,
            updated_patient.secondary_phone,
            updated_patient.email,
            updated_patient.city,
            updated_patient.country,
            1 if updated_patient.has_health_insurance else 0,
            updated_patient.health_insurance_name,
            updated_patient.health_insurance_number,
            updated_patient.medical_observations,
            1 if updated_patient.isActive else 0,
            updated_patient.id
        ]
        return self._db.execute_command(query, params)

    def delete_patient_by_dni(self, dni: str) -> bool:
        query = "UPDATE patients SET is_active = 0 WHERE dni = ?"
        return self._db.execute_command(query, [dni])
