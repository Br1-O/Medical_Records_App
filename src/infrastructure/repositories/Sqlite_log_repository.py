from typing import List
from domain.Log import Log, ILog_repository
from domain.Entity import Entity
from infrastructure.database import Sqlite_database_handler

class Sqlite_log_repository(ILog_repository):

    def __init__(self, db: Sqlite_database_handler):
        self._db: Sqlite_database_handler = db

    def _row_to_log(self, row) -> Log:
        return Log(
            timestamp=row["timestamp"],
            operation=row["operation"],
            affected_record_id=row["affected_record_id"],
            id=row["id"]
        )

    def get_logs_by_entity(self, entity: Entity) -> List[Log]:
        query = "SELECT * FROM logs WHERE operation LIKE ?"
        entity_name = type(entity).__name__
        if entity_name == "Patient":
            rows = self._db.execute_query(query, ["%Paciente%"])
        elif entity_name == "Medical_record":
            rows = self._db.execute_query(query, ["%Historial%"])
        else:
            rows = self._db.execute_query(query, ["%%"])
        return [self._row_to_log(row) for row in rows]

    def get_logs_by_action(self, action: str) -> List[Log]:
        query = "SELECT * FROM logs WHERE operation LIKE ?"
        rows = self._db.execute_query(query, [f"%{action}%"])
        return [self._row_to_log(row) for row in rows]

    def get_all_logs(self) -> List[Log]:
        query = "SELECT * FROM logs ORDER BY id DESC"
        rows = self._db.execute_query(query)
        return [self._row_to_log(row) for row in rows]

    def create_log(self, new_log: Log) -> bool:
        query = "INSERT INTO logs (timestamp, operation, affected_record_id) VALUES (?, ?, ?)"
        params = [new_log.timestamp, new_log.operation, new_log.affectedRecordId]
        return self._db.execute_command(query, params)
