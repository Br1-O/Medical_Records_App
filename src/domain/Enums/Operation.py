from enum import Enum

class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    RECOVERY = "RECOVERY"