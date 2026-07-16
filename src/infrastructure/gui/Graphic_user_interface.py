import tkinter as tk
from tkinter import ttk
import os
from typing import Callable, List, Dict, Any, Optional

from domain.Enums.View import View
from domain.Patient.Patient import Patient
from domain.Medical_record.Medical_record import Medical_record
from domain.Log.Log import Log

from infrastructure.gui.styles import PALETTE, apply_modern_styles
from infrastructure.gui.General_view import General_view
from infrastructure.gui.Detail_view import Detail_view
from infrastructure.gui.Registration_view import Registration_view
from infrastructure.gui.Record_creation_view import Record_creation_view
from infrastructure.gui.Medical_record_read_view import Medical_record_read_view
from infrastructure.gui.Log_view import Log_view

# =======================
# CONFIGURACION BASE
# =======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WINDOW_ICON_PATH_ICO = os.path.join(BASE_DIR, "public", "images", "favicon.ico")
WINDOW_ICON_PATH_PNG = os.path.join(BASE_DIR, "public", "images", "favicon.png")


# ==================================
# GRAPHIC USER INTERFACE MAIN CLASS
# ==================================

class Graphic_user_interface:

    def __init__(self):
        # --- Configuracion Base de la Ventana Tkinter ---
        self.root = tk.Tk()
        self.root.title("Sistema de Gestion de Historias Clinicas - Saca Muela")
        self.root.geometry("950x850")
        self.root.configure(bg=PALETTE["bg_light"])

        # Carga del icono (.ico en Windows, .png en Linux/macOS)
        try:
            if os.name == "nt":
                self.root.iconbitmap(WINDOW_ICON_PATH_ICO)
            else:
                self._icon_ref = tk.PhotoImage(file=WINDOW_ICON_PATH_PNG)
                self.root.iconphoto(True, self._icon_ref)
        except Exception:
            pass

        apply_modern_styles()

        # --- Creacion del Notebook (Pestanas del Sistema) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. Pestana de Pacientes
        self.tab_patients = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_patients, text=" Pacientes ")

        # 2. Pestana de Auditoria
        self.tab_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_logs, text=" Auditoria de Sistema ")

        # Inicializacion de las Vistas Modularizadas en sus respectivas pestanas
        self.views: Dict[View, ttk.Frame] = {}
        self.views[View.MAIN_WINDOW] = General_view(self.tab_patients, self)
        self.views[View.PATIENT_DETAIL] = Detail_view(self.tab_patients, self)

        # En la pestana de Logs, coloca la vista de Auditoria
        self.views[View.LOGS_WINDOW] = Log_view(self.tab_logs, self)

        # Agrega las vistas dinamicas:
        self.views[View.PATIENT_REGISTRATION] = Registration_view(self.tab_patients, self)
        self.views[View.MEDICAL_RECORD_DETAIL] = Record_creation_view(self.tab_patients, self)
        self.views[View.MEDICAL_RECORD_READ] = Medical_record_read_view(self.tab_patients, self)

        # Evento de cambio de pestana para recargar datos automaticamente
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # Forzar vista inicial dentro de la pestana Pacientes
        self.set_view(View.MAIN_WINDOW)

        # --- Callbacks mapeados con el Handler ---
        self._current_patient_dni: str = ""
        self._editing_patient_dni: str = ""

        self.on_patient_search: Optional[Callable[[], None]] = None
        self.on_patient_creation: Optional[Callable[[], None]] = None
        self.on_patient_update: Optional[Callable[[], None]] = None
        self.on_patient_delete: Optional[Callable[[], None]] = None

        self.on_medical_record_search: Optional[Callable[[], None]] = None
        self.on_medical_record_creation: Optional[Callable[[], None]] = None
        self.on_medical_record_delete: Optional[Callable[[], None]] = None

        self.on_log_search: Optional[Callable[[], None]] = None
        self.on_log_double_click: Optional[Callable[[], None]] = None
        self.on_patient_detail_view: Optional[Callable[[], None]] = None
        self.on_edit_patient: Optional[Callable[[], None]] = None
        self.on_patient_reactivate: Optional[Callable[[], None]] = None
        self.on_medical_record_detail_view: Optional[Callable[[], None]] = None

    def set_view(self, view_name: View) -> None:
        """Oculta y posiciona las vistas de la pestana activa o cambia de pestana."""
        if view_name in [View.MAIN_WINDOW, View.PATIENT_DETAIL, View.PATIENT_REGISTRATION, View.MEDICAL_RECORD_DETAIL, View.MEDICAL_RECORD_READ, View.ALL_PATIENTS]:
            self.notebook.select(0)

            # Ocultamos todas las vistas hijas de esta pestana antes de mostrar la activa
            for v_name, v_frame in self.views.items():
                if v_name != View.LOGS_WINDOW:
                    v_frame.pack_forget()

            # Si es ALL_PATIENTS, mostramos la MAIN_WINDOW (el listado)
            actual_view_name = View.MAIN_WINDOW if view_name == View.ALL_PATIENTS else view_name
            target_view = self.views.get(actual_view_name)
            if target_view:
                target_view.pack(fill="both", expand=True, padx=10, pady=10)

        elif view_name == View.LOGS_WINDOW:
            self.notebook.select(1)
            self.views[View.LOGS_WINDOW].pack(fill="both", expand=True, padx=10, pady=10)

    def _on_tab_changed(self, event):
        """Dispara las busquedas y cargas necesarias segun la pestana activa."""
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:  # Pestana de Logs activa
            self.views[View.LOGS_WINDOW].pack(fill="both", expand=True, padx=10, pady=10)
            if self.on_log_search:
                self.on_log_search()

    def clear_fields(self, view_name: View) -> None:
        if view_name == View.MAIN_WINDOW:
            self.views[View.MAIN_WINDOW].search_entry.delete(0, tk.END)
        elif view_name == View.PATIENT_REGISTRATION:
            self.views[View.PATIENT_REGISTRATION].clear()
        elif view_name == View.MEDICAL_RECORD_DETAIL:
            self.views[View.MEDICAL_RECORD_DETAIL].clear()

    # --- Metodos de lectura de datos para el Handler ---
    def get_selected_patient_id(self) -> int:
        view: General_view = self.views[View.MAIN_WINDOW]
        selected_item = view.tree.selection()
        if not selected_item:
            return 0
        return int(view.tree.item(selected_item[0], "tags")[0])

    def get_selected_patient_dni(self) -> str:
        view: General_view = self.views[View.MAIN_WINDOW]
        selected_item = view.tree.selection()
        if not selected_item:
            return ""
        return str(view.tree.item(selected_item[0], "values")[0])

    def set_editing_mode(self, editing: bool) -> None:
        view: Registration_view = self.views[View.PATIENT_REGISTRATION]
        view.set_editing_mode(editing)

    def get_search_text_from_patient_search_form(self) -> Dict[str, Any]:
        view: General_view = self.views[View.MAIN_WINDOW]
        return {"query": view.search_entry.get().strip()}

    def get_patient_status_filter(self) -> bool:
        view: General_view = self.views[View.MAIN_WINDOW]
        return view.status_filter.get() == "Activo"

    def get_patient_search_type(self) -> str:
        view: General_view = self.views[View.MAIN_WINDOW]
        return view.search_type.get()

    def get_search_record_query(self) -> str:
        view: Detail_view = self.views[View.PATIENT_DETAIL]
        return view.record_search_entry.get().strip()

    def get_search_record_type(self) -> str:
        view: Detail_view = self.views[View.PATIENT_DETAIL]
        return view.record_search_type.get()

    def get_selected_log_data(self) -> tuple:
        view: Log_view = self.views[View.LOGS_WINDOW]
        selected_item = view.tree_logs.selection()
        if not selected_item:
            return ("", 0)
        tags = view.tree_logs.item(selected_item[0], "tags")
        operation = tags[0] if len(tags) > 0 else ""
        affected_id = int(tags[1]) if len(tags) > 1 and tags[1].isdigit() else 0
        return (operation, affected_id)

    def get_selected_medical_record_id(self) -> int:
        view: Detail_view = self.views[View.PATIENT_DETAIL]
        selected_item = view.tree_history.selection()
        if not selected_item:
            return 0
        return int(view.tree_history.item(selected_item[0], "tags")[0])

    # --- Metodos completados para extraer la informacion ingresada por el usuario ---
    def get_data_from_patient_creation_form(self) -> Dict[str, Any]:
        view: Registration_view = self.views[View.PATIENT_REGISTRATION]
        return view.get_data()

    def get_data_from_patient_update_form(self) -> Dict[str, Any]:
        view: Registration_view = self.views[View.PATIENT_REGISTRATION]
        return view.get_data()

    def get_data_from_medical_record_creation_form(self) -> Dict[str, Any]:
        view: Record_creation_view = self.views[View.MEDICAL_RECORD_DETAIL]
        return view.get_data()

    def get_search_text_from_medical_record_form(self) -> Dict[str, Any]: return {}
    def get_data_from_medical_record_update_form(self) -> Dict[str, Any]: return {}
    def get_search_text_from_log_form(self) -> Dict[str, Any]: return {}

    # --- Metodos para renderizar datos ---
    def set_all_patients_data_for_display(self, patients: List[Patient]) -> None:
        view: General_view = self.views[View.MAIN_WINDOW]
        for item in view.tree.get_children():
            view.tree.delete(item)
        if not patients:
            view.tree.insert("", "end", values=("No se encontraron registros", "", ""))
            return
        for p in patients:
            view.tree.insert("", "end", values=(p.dni, p.last_name, p.name), tags=(str(p.id),))

    def set_patient_data_for_update_form(self, patient: Patient) -> None:
        """Carga los datos del paciente seleccionado en el formulario de registro para poder editarlo."""
        view: Registration_view = self.views[View.PATIENT_REGISTRATION]
        view.clear()

        # Mapea los datos que expone Patient
        mapping = {
            "dni": patient.dni,
            "name": patient.name,
            "last_name": patient.last_name,
            "gender": patient.gender or "",
            "phone": patient.phone or "",
            "emergency_contact": patient.emergency_contact or "",
            "health_insurance_name": patient.health_insurance_name or "",
            "health_insurance_number": patient.health_insurance_number or ""
        }

        for key, val in mapping.items():
            if key in view.inputs:
                widget = view.inputs[key]
                text_val = str(val) if val is not None else ""
                if isinstance(widget, ttk.Combobox):
                    widget.set(text_val)
                else:
                    widget.insert(0, text_val)

        # Setea los comboboxes de fecha por separado
        if patient.birth_date and len(patient.birth_date) == 10:
            parts = patient.birth_date.split("-")
            view.date_year.set(parts[0])
            view.date_month.set(parts[1])
            view.date_day.set(parts[2])

    def set_all_medical_records_data_for_display(self, medical_records: List[Medical_record]) -> None:
        view: Detail_view = self.views[View.PATIENT_DETAIL]
        for item in view.tree_history.get_children():
            view.tree_history.delete(item)
        if not medical_records:
            view.tree_history.insert("", "end", values=("No se encontraron registros", "", ""))
            return
        for record in medical_records:
            date_only = record.date.split(" ")[0] if record.date else ""
            view.tree_history.insert("", "end", values=(date_only, record.consultation_reason, record.diagnosis), tags=(str(record.id),))

    def set_medical_record_data_for_display(self, record: 'Medical_record') -> None:
        view: Medical_record_read_view = self.views[View.MEDICAL_RECORD_READ]
        view.set_data(
            date=record.date,
            consultation_reason=record.consultation_reason,
            diagnosis=record.diagnosis,
            treatment_evolution=record.treatment_evolution,
            observations=record.observations
        )

    def set_all_logs_data_for_display(self, logs: List[Log]) -> None:
        view: Log_view = self.views[View.LOGS_WINDOW]
        for item in view.tree_logs.get_children():
            view.tree_logs.delete(item)
        if not logs:
            view.tree_logs.insert("", "end", values=("No se encontraron registros", ""))
            return
        for log in logs:
            view.tree_logs.insert("", "end", values=(log.timestamp, log.operation), tags=(log.operation, str(log.affectedRecordId)))
