from typing import List
from domain.Log.Log import Log
from domain.Log.ILog_repository import ILog_repository
from domain.Entity import Entity

class Log_service:

    def __init__(self, log_repository: ILog_repository):
        self._log_repository = log_repository

    def get_logs_by_entity_use_case(self, entity: Entity) -> List[Log]:
        return self._log_repository.get_logs_by_entity(entity)

    def get_logs_by_action_use_case(self, action: str) -> List[Log]:
        return self._log_repository.get_logs_by_action(action)

    def get_all_logs_use_case(self) -> List[Log]:
        return self._log_repository.get_all_logs()

    def create_log_use_case(self, new_log: Log) -> bool:
        return self._log_repository.create_log(new_log)