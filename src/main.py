import sys
import os

from infrastructure.database import Sqlite_database_handler
from infrastructure.repositories import Sqlite_patient_repository, Sqlite_medical_record_repository, Sqlite_log_repository

from application.services import Patient_service, Medical_record_service, Log_service

from infrastructure.gui import Graphic_user_interface, Graphic_user_interface_handler

class App_launcher:
    def __init__(self):
        # directorio donde vive "main.py" (que es "src/")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Une ese directorio directamente con base de datos
        db_path = os.path.join(base_dir, "saca_muela.db")
        self._db_handler = Sqlite_database_handler(db_path)

        patient_repo = Sqlite_patient_repository(self._db_handler)
        medical_record_repo = Sqlite_medical_record_repository(self._db_handler)
        log_repo = Sqlite_log_repository(self._db_handler)

        self._patient_service = Patient_service(patient_repo)
        self._medical_record_service = Medical_record_service(medical_record_repo)
        self._log_service = Log_service(log_repo)

        self._gui = Graphic_user_interface()
        self._gui_handler = Graphic_user_interface_handler(
            self._gui, 
            self._patient_service, 
            self._medical_record_service, 
            self._log_service
        )

    def run(self) -> None:
        try:
            self._db_handler.connect()
            self._gui_handler.bind_methods_to_graphic_user_interface()
            self._gui_handler._on_patient_search_handler()
            print("[INFO] Sistema de Gestión Clínico iniciado con éxito.")
            self._gui.root.mainloop()
        except Exception as e:
            print(f"[FATAL ERROR] Error crítico durante el lanzamiento: {e}", file=sys.stderr)
            self.shutdown()

    def shutdown(self) -> None:
        print("[INFO] Apagando el sistema...")
        try:
            self._db_handler.close()
        except Exception as e:
            print(f"[WARN] Error al cerrar base de datos: {e}")
        sys.exit(0)

if __name__ == "__main__":
    app = App_launcher()
    app.run()