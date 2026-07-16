import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.database.Sqlite_database_handler import SQLiteDatabaseHandler


class AppLauncher:
    @staticmethod
    def main():
        db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "saca_muela.db",
        )
        db_handler = SQLiteDatabaseHandler(db_path)
        db_handler.connect()


if __name__ == "__main__":
    AppLauncher.main()
