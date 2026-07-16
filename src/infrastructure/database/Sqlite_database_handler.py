import sqlite3
from typing import List, Any, Optional

class Sqlite_database_handler:
    
    def __init__(self, path: str):
        self._path: str = path
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establece la conexión con la base de datos SQLite."""
        if not self._connection:
            self._connection = sqlite3.connect(self._path)
            # Para habilitar que devuelva diccionarios o soporte transacciones complejas si fuese necesario
            self._connection.row_factory = sqlite3.Row

    def execute_command(self, query: str, params: List[Any] = []) -> bool:
        """Ejecuta comandos de escritura (INSERT, UPDATE, DELETE). Devuelve True si tuvo éxito."""
        if not self._connection:
            self.connect()
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            return True
        except sqlite3.Error as e:
            print(self._connection) # Log temporal
            print(f"Error de base de datos ejecutando comando: {e}")
            return False

    def execute_query(self, query: str, params: List[Any] = []) -> List[sqlite3.Row]:
        """Ejecuta consultas de lectura (SELECT) y retorna las filas obtenidas."""
        if not self._connection:
            self.connect()
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error de base de datos ejecutando consulta: {e}")
            return []

    def close(self) -> None:
        """Cierra la conexión activa de la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None
