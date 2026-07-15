import sqlite3


class SQLiteDatabaseHandler:
    def __init__(self, db_path):
        self.dbPath = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.dbPath)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE,
                birth_date TEXT NOT NULL,
                gender TEXT NOT NULL,
                address TEXT DEFAULT '',
                phone TEXT NOT NULL,
                secondary_phone TEXT DEFAULT '',
                email TEXT DEFAULT '',
                city TEXT DEFAULT 'Mar del Plata',
                country TEXT DEFAULT 'Argentina',
                emergency_contact TEXT NOT NULL,
                has_health_insurance INTEGER DEFAULT 0,
                health_insurance_name TEXT DEFAULT '',
                health_insurance_number TEXT DEFAULT '',
                medical_observations TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                consultation_reason TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                treatment_evolution TEXT NOT NULL,
                observations TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                operation TEXT NOT NULL,
                affected_record_id INTEGER NOT NULL,
                is_active INTEGER DEFAULT 1
            )
        """)

        self.connection.commit()

    def executeNonQuery(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False

    def executeQuery(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
