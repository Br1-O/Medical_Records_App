import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from typing import Callable, List, Dict, Any, Optional

from domain.Enums.View import View
from domain.Patient.Patient import Patient
from domain.Medical_record.Medical_record import Medical_record
from domain.Log.Log import Log

# =======================
# CONFIGURACIÓN ESTÉTICA 
# =======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WINDOW_ICON_PATH_ICO = os.path.join(BASE_DIR, "public", "images", "favicon.ico")
WINDOW_ICON_PATH_PNG = os.path.join(BASE_DIR, "public", "images", "favicon.png")

PALETTE = {
    "bg_light": "#F7F9FC",       # Fondo general
    "bg_white": "#FFFFFF",       # Fondo de tarjetas y contenedores
    "primary": "#8FAADC",        # Azul suave
    "primary_hover": "#7D9BCB",  # Azul hover
    "secondary": "#E2E8F0",      # Gris para bordes y elementos secundarios
    "text_dark": "#2D3748",      # Gris oscuro para legibilidad de textos
    "text_muted": "#718096",     # Gris medio para subtítulos o datos secundarios
    "accent_green": "#A8DADC",   # Verde para éxitos o acciones positivas
    "accent_red": "#F5B7B1"      # Rojo/Rosa para errores o destrucciones
}

FONT_FAMILY = "Segoe UI"  # Fuente 

def apply_modern_styles():
    """Configura los estilos globales de ttk."""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configuración de frames y labels
    style.configure("TFrame", background=PALETTE["bg_light"])
    style.configure("Card.TFrame", background=PALETTE["bg_white"], relief="flat", borderwidth=1)
    style.configure("TLabel", background=PALETTE["bg_light"], foreground=PALETTE["text_dark"], font=(FONT_FAMILY, 10))
    style.configure("Title.TLabel", background=PALETTE["bg_light"], foreground=PALETTE["text_dark"], font=(FONT_FAMILY, 16, "bold"))
    style.configure("Sub.TLabel", background=PALETTE["bg_light"], foreground=PALETTE["text_muted"], font=(FONT_FAMILY, 10, "italic"))
    style.configure("CardTitle.TLabel", background=PALETTE["bg_white"], foreground=PALETTE["text_dark"], font=(FONT_FAMILY, 12, "bold"))
    style.configure("CardText.TLabel", background=PALETTE["bg_white"], foreground=PALETTE["text_dark"], font=(FONT_FAMILY, 10))
    
    # Entradas de texto (Inputs)
    style.configure("TEntry", fieldbackground=PALETTE["bg_white"], bordercolor=PALETTE["secondary"], lightcolor=PALETTE["secondary"], darkcolor=PALETTE["secondary"])
    
    # Botones planos 
    style.configure("TButton", font=(FONT_FAMILY, 10, "bold"), background=PALETTE["primary"], foreground=PALETTE["text_dark"], borderwidth=0, focuscolor="none")
    style.map("TButton", background=[("active", PALETTE["primary_hover"])])
    
    style.configure("Secondary.TButton", background=PALETTE["secondary"], foreground=PALETTE["text_dark"])
    style.map("Secondary.TButton", background=[("active", "#CBD5E0")])
    
    style.configure("Danger.TButton", background=PALETTE["accent_red"], foreground=PALETTE["text_dark"])
    style.map("Danger.TButton", background=[("active", "#E69A9A")])

    style.configure("Success.TButton", background=PALETTE["accent_green"], foreground=PALETTE["text_dark"])
    style.map("Success.TButton", background=[("active", "#8FC3C5")])

    # Estilos del Notebook (Pestañas)
    style.configure("TNotebook", background=PALETTE["bg_light"], borderwidth=0)
    style.configure("TNotebook.Tab", background=PALETTE["secondary"], foreground=PALETTE["text_dark"], 
                    font=(FONT_FAMILY, 10, "bold"), padding=[20, 8], borderwidth=0)
    style.map("TNotebook.Tab", 
              background=[("selected", PALETTE["primary"]), ("active", PALETTE["primary_hover"])],
              foreground=[("selected", PALETTE["text_dark"])])

    # Tablas (Treeview)
    style.configure("Treeview", font=(FONT_FAMILY, 10), background=PALETTE["bg_white"], foreground=PALETTE["text_dark"], rowheight=28, fieldbackground=PALETTE["bg_white"])
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, "bold"), background=PALETTE["secondary"], foreground=PALETTE["text_dark"], relief="flat")
    style.map("Treeview", background=[("selected", PALETTE["primary"])], foreground=[("selected", PALETTE["text_dark"])])


# =====================================================================
# MODULARIZACIÓN DE VISTAS (SUB-COMPONENTES)
# =====================================================================

class General_view(ttk.Frame):
    """Vista General: Contiene la tabla principal de pacientes y la barra de búsqueda."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(5, 15))
        ttk.Label(header, text="Búsqueda de Pacientes", style="Title.TLabel").pack(side="left")
        
        # Formulario de Búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=(0, 15))
        
        self.search_type = ttk.Combobox(search_frame, values=["Apellido", "Nombre", "DNI", "Obra Social"], state="readonly", width=14)
        self.search_type.set("Apellido")
        self.search_type.pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.status_filter = ttk.Combobox(search_frame, values=["Activo", "Inactivo"], state="readonly", width=12)
        self.status_filter.set("Activo")
        self.status_filter.pack(side="left", padx=(0, 10))

        search_btn = ttk.Button(search_frame, text="Buscar", command=self._on_search)
        search_btn.pack(side="left", padx=(0, 5))

        clear_btn = ttk.Button(search_frame, text="Limpiar", command=self._on_clear_search)
        clear_btn.pack(side="left", padx=(0, 5))

        # Tabla de Pacientes
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("dni", "last_name", "name")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("last_name", text="Apellido")
        self.tree.heading("name", text="Nombre")
        
        self.tree.column("dni", width=120, anchor="center")
        self.tree.column("last_name", width=200, anchor="w")
        self.tree.column("name", width=200, anchor="w")
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        # Doble click para ir al Detalle
        self.tree.bind("<Double-1>", lambda event: self._on_double_click())

        # Barra de acciones inferior
        actions_frame = ttk.Frame(self)
        actions_frame.pack(fill="x", pady=(15, 5))
        
        ttk.Button(actions_frame, text="Nuevo Paciente", style="Success.TButton", 
           command=self._on_new_patient).pack(side="right", padx=5)
        ttk.Button(actions_frame, text="Ver Ficha Detallada", 
           command=self._on_view_detail_clicked).pack(side="right", padx=5)

    def _on_search(self):
        if self._gui.on_patient_search:
            self._gui.on_patient_search()

    def _on_clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search_type.set("Apellido")
        self.status_filter.set("Activo")
        if self._gui.on_patient_search:
            self._gui.on_patient_search()

    def _on_new_patient(self):
        self._gui.set_editing_mode(False)
        self._gui._editing_patient_dni = ""
        self._gui.clear_fields(View.PATIENT_REGISTRATION)
        self._gui.set_view(View.PATIENT_REGISTRATION)

    def _on_double_click(self):
        selected = self.tree.selection()
        if selected:
            if self._gui.on_patient_detail_view:
                self._gui.on_patient_detail_view()
            self._gui.set_view(View.PATIENT_DETAIL)

    def _on_view_detail_clicked(self):
        """Valida que haya un paciente seleccionado antes de abrir el detalle."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Por favor, seleccione un paciente de la lista para ver su ficha detallada.")
            return
        
        if self._gui.on_patient_detail_view:
            self._gui.on_patient_detail_view()
        self._gui.set_view(View.PATIENT_DETAIL)


class Detail_view(ttk.Frame):
    """Vista Detalle: Muestra la información del Paciente y su Historial de Consultas."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="← Volver al Listado", style="Secondary.TButton", 
                   command=lambda: self._gui.set_view(View.MAIN_WINDOW)).pack(side="left")

        # Tarjeta de Datos del Paciente (Card)
        self.card = ttk.Frame(self, style="Card.TFrame")
        self.card.pack(fill="x", ipady=15, ipadx=15, pady=(0, 15))
        
        self.lbl_fullname = ttk.Label(self.card, text="Cargando Paciente...", style="CardTitle.TLabel")
        self.lbl_fullname.pack(anchor="w", pady=(0, 5))
        
        info_grid = ttk.Frame(self.card, style="Card.TFrame")
        info_grid.pack(fill="x", pady=(0, 5))

        self.lbl_dni = ttk.Label(info_grid, text="DNI: -", style="CardText.TLabel")
        self.lbl_dni.grid(row=0, column=0, sticky="w", padx=(0, 30), pady=1)
        self.lbl_birth_date = ttk.Label(info_grid, text="Nacimiento: -", style="CardText.TLabel")
        self.lbl_birth_date.grid(row=0, column=1, sticky="w", padx=(0, 30), pady=1)
        self.lbl_gender = ttk.Label(info_grid, text="Género: -", style="CardText.TLabel")
        self.lbl_gender.grid(row=0, column=2, sticky="w", pady=1)

        self.lbl_phone = ttk.Label(info_grid, text="Teléfono: -", style="CardText.TLabel")
        self.lbl_phone.grid(row=1, column=0, sticky="w", padx=(0, 30), pady=1)
        self.lbl_emergency = ttk.Label(info_grid, text="Contacto Emergencia: -", style="CardText.TLabel")
        self.lbl_emergency.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=1)

        self.lbl_insurance = ttk.Label(info_grid, text="Obra Social: -", style="CardText.TLabel")
        self.lbl_insurance.grid(row=2, column=0, sticky="w", padx=(0, 30), pady=1)
        self.lbl_insurance_num = ttk.Label(info_grid, text="Nro Obra Social: -", style="CardText.TLabel")
        self.lbl_insurance_num.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=1)
        self.lbl_status = ttk.Label(info_grid, text="Estado: -", style="CardText.TLabel")
        self.lbl_status.grid(row=2, column=2, sticky="w", pady=1)

        # Botones de Acción -  tk.Frame para el fondo
        btn_box = tk.Frame(self.card, background=PALETTE["bg_white"])
        btn_box.pack(anchor="e", pady=(10, 0))
        
        # El botón editar datos redirige al formulario con la información cargada
        ttk.Button(btn_box, text="Editar Datos", 
                   command=self._on_edit_patient).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Dar de Baja", style="Danger.TButton", 
                   command=self._on_delete_patient).pack(side="left", padx=5)

        # Sección de Historia Clínica
        ttk.Label(self, text="Historia Clínica", style="CardTitle.TLabel").pack(anchor="w", pady=(10, 5))

        # Barra de búsqueda de evoluciones
        record_search_frame = ttk.Frame(self)
        record_search_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(record_search_frame, text="Buscar entrada:").pack(side="left", padx=(0, 5))
        self.record_search_entry = ttk.Entry(record_search_frame, width=25)
        self.record_search_entry.pack(side="left", padx=(0, 5))
        self.record_search_type = ttk.Combobox(record_search_frame, values=["Fecha", "Diagnóstico", "Tratamiento"], state="readonly", width=14)
        self.record_search_type.set("Diagnóstico")
        self.record_search_type.pack(side="left", padx=(0, 5))
        ttk.Button(record_search_frame, text="Buscar", command=self._on_search_record).pack(side="left")
        ttk.Button(record_search_frame, text="Limpiar", command=self._on_clear_search_record).pack(side="left", padx=(5, 0))
        
        self.history_frame = ttk.Frame(self)
        self.history_frame.pack(fill="both", expand=True)

        columns = ("date", "motivo", "diagnostico")
        self.tree_history = ttk.Treeview(self.history_frame, columns=columns, show="headings")
        self.tree_history.heading("date", text="Fecha")
        self.tree_history.heading("motivo", text="Motivo de Consulta")
        self.tree_history.heading("diagnostico", text="Diagnóstico")
        
        self.tree_history.column("date", width=150, anchor="center")
        self.tree_history.column("motivo", width=300, anchor="w")
        self.tree_history.column("diagnostico", width=300, anchor="w")
        
        self.tree_history.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.tree_history.yview)
        self.tree_history.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        self.tree_history.bind("<Double-1>", lambda e: self._on_view_record())

        # Acciones de Historia Clínica
        history_actions = ttk.Frame(self)
        history_actions.pack(fill="x", pady=(15, 5))
        
        ttk.Button(history_actions, text="Ver Detalle",
                   command=self._on_view_record).pack(side="left", padx=(0, 5))
        ttk.Button(history_actions, text="Anular Entrada", style="Danger.TButton", 
                   command=self._on_delete_record).pack(side="left")
        ttk.Button(history_actions, text="+ Agregar Entrada", style="Success.TButton", 
                   command=lambda: self._gui.set_view(View.MEDICAL_RECORD_DETAIL)).pack(side="right")

    def _on_edit_patient(self):
        if self._gui.on_edit_patient:
            self._gui.on_edit_patient()
        self._gui.set_view(View.PATIENT_REGISTRATION)

    def _on_delete_patient(self):
        if messagebox.askyesno("Atención", "¿Está seguro de que desea dar de baja a este paciente?"):
            if self._gui.on_patient_delete:
                self._gui.on_patient_delete()

    def _on_delete_record(self):
        selected = self.tree_history.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, seleccione una entrada de la lista.")
            return
        if messagebox.askyesno("Atención", "¿Desea anular de forma permanente esta entrada médica?"):
            if self._gui.on_medical_record_delete:
                self._gui.on_medical_record_delete()

    def _on_view_record(self):
        selected = self.tree_history.selection()
        if not selected:
            return
        if self._gui.on_medical_record_detail_view:
            self._gui.on_medical_record_detail_view()
        self._gui.set_view(View.MEDICAL_RECORD_READ)

    def _on_search_record(self):
        if self._gui.on_medical_record_search:
            self._gui.on_medical_record_search()

    def _on_clear_search_record(self):
        self.record_search_entry.delete(0, tk.END)
        self.record_search_type.set("Diagnóstico")
        if self._gui.on_medical_record_search:
            self._gui.on_medical_record_search()


class Registration_view(ttk.Frame):
    """Vista de Registro: Formulario para dar de alta o editar un Paciente."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self.inputs = {}
        self._editing = False
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="← Volver al Listado", style="Secondary.TButton", 
                   command=lambda: self._gui.set_view(View.MAIN_WINDOW)).pack(side="left")

        # Contenedor del Formulario
        form_container = ttk.Frame(self, style="Card.TFrame")
        form_container.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(form_container, text="Ficha de Datos de Paciente", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Campos clave de entrada
        fields = [
            ("DNI (*):", "dni"),
            ("Nombre (*):", "name"),
            ("Apellido (*):", "last_name"),
            ("Género (*):", "gender"),
            ("Teléfono (*):", "phone"),
            ("Contacto de Emergencia (*):", "emergency_contact"),
            ("Obra Social / Prepaga:", "health_insurance_name"),
            ("Nro Obra Social:", "health_insurance_number")
        ]

        for i, (label_text, field_key) in enumerate(fields):
            row = i + 1
            ttk.Label(form_container, text=label_text, style="CardText.TLabel").grid(row=row, column=0, sticky="e", padx=(0, 15), pady=8)
            
            if field_key == "gender":
                combo = ttk.Combobox(form_container, values=["Masculino", "Femenino", "Otro"], state="readonly", width=37)
                combo.grid(row=row, column=1, sticky="w", pady=8)
                self.inputs[field_key] = combo
            else:
                entry = ttk.Entry(form_container, width=40)
                entry.grid(row=row, column=1, sticky="w", pady=8)
                self.inputs[field_key] = entry

        # Selector de fecha de nacimiento (Año-Mes-Día)
        birth_row = len(fields) + 1
        ttk.Label(form_container, text="Fecha de Nacimiento (*):", style="CardText.TLabel").grid(row=birth_row, column=0, sticky="e", padx=(0, 15), pady=8)
        date_frame = ttk.Frame(form_container, style="Card.TFrame")
        date_frame.grid(row=birth_row, column=1, sticky="w", pady=8)

        years = [str(y) for y in range(2026, 1899, -1)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]

        self.date_year = ttk.Combobox(date_frame, values=years, state="readonly", width=8)
        self.date_year.set("YYYY")
        self.date_year.pack(side="left", padx=(0, 4))
        ttk.Label(date_frame, text="/").pack(side="left")
        self.date_month = ttk.Combobox(date_frame, values=months, state="readonly", width=5)
        self.date_month.set("MM")
        self.date_month.pack(side="left", padx=(4, 4))
        ttk.Label(date_frame, text="/").pack(side="left")
        self.date_day = ttk.Combobox(date_frame, values=days, state="readonly", width=5)
        self.date_day.set("DD")
        self.date_day.pack(side="left", padx=(4, 0))

        # Caja de botones inferiores de acción
        btn_container = tk.Frame(form_container, background=PALETTE["bg_white"])
        btn_container.grid(row=len(fields)+2, column=1, sticky="e", pady=(20, 0))

        ttk.Button(btn_container, text="Guardar Paciente", style="Success.TButton", 
                   command=self._on_save).pack(side="right", padx=5)
        ttk.Button(btn_container, text="Cancelar", style="Secondary.TButton", 
                   command=self._on_cancel).pack(side="right", padx=5)

    def _on_save(self):
        data = self.get_data()
        required_fields = ["dni", "name", "last_name", "birth_date", "gender", "phone", "emergency_contact"]
        field_names = {"dni": "DNI", "name": "Nombre", "last_name": "Apellido", "birth_date": "Fecha de nacimiento", "gender": "Género", "phone": "Teléfono", "emergency_contact": "Contacto de emergencia"}
        missing = [field_names.get(f, f) for f in required_fields if not data.get(f)]

        if missing:
            messagebox.showerror("Error de Validación", f"Los campos obligatorios deben ser completados: {', '.join(missing)}.")
            return

        if self._gui._editing_patient_dni and self._gui.on_patient_update:
            self._gui.on_patient_update()
        elif self._gui.on_patient_creation:
            self._gui.on_patient_creation()

    def set_editing_mode(self, editing: bool) -> None:
        self._editing = editing

    def _on_cancel(self):
        self._editing = False
        self._gui._editing_patient_dni = ""
        self.clear()
        self._gui.set_view(View.MAIN_WINDOW)

    def get_data(self) -> Dict[str, Any]:
        """Obtiene un diccionario con los datos cargados en pantalla."""
        data = {key: entry.get().strip() for key, entry in self.inputs.items()}
        y = self.date_year.get().strip()
        m = self.date_month.get().strip()
        d = self.date_day.get().strip()
        if y and m and d and y != "YYYY" and m != "MM" and d != "DD":
            data["birth_date"] = f"{y}-{m}-{d}"
        else:
            data["birth_date"] = ""
        return data

    def clear(self):
        """Limpia todos los campos de texto de la ficha."""
        for key, widget in self.inputs.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        self.date_year.set("YYYY")
        self.date_month.set("MM")
        self.date_day.set("DD")


class Record_creation_view(ttk.Frame):
    """Vista de Entrada Clínica: Permite agregar una nueva entrada a la historia clínica."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self.text_areas = {}
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="← Volver a Ficha", style="Secondary.TButton", 
                   command=lambda: self._gui.set_view(View.PATIENT_DETAIL)).pack(side="left")

        form_container = ttk.Frame(self, style="Card.TFrame")
        form_container.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(form_container, text="Nueva Entrada de Historia Clínica", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        fields = [
            ("Motivo de Consulta (*):", "consultation_reason", 3),
            ("Diagnóstico (*):", "diagnosis", 3),
            ("Evolución / Tratamiento (*):", "treatment_evolution", 5),
            ("Observaciones:", "observations", 2),
        ]

        for label_text, field_key, height in fields:
            ttk.Label(form_container, text=label_text, style="CardText.TLabel").pack(anchor="w", pady=(8, 2))
            text_area = tk.Text(form_container, wrap="word", height=height, bg=PALETTE["bg_white"],
                                fg=PALETTE["text_dark"], highlightbackground=PALETTE["secondary"],
                                relief="flat", borderwidth=1)
            text_area.pack(fill="x", pady=(0, 4))
            self.text_areas[field_key] = text_area

        btn_container = tk.Frame(form_container, background=PALETTE["bg_white"])
        btn_container.pack(anchor="e", pady=(10, 0))

        ttk.Button(btn_container, text="Guardar Entrada", style="Success.TButton", 
                   command=self._on_save).pack(side="right", padx=5)
        ttk.Button(btn_container, text="Cancelar", style="Secondary.TButton", 
                   command=lambda: self._gui.set_view(View.PATIENT_DETAIL)).pack(side="right", padx=5)

    def _on_save(self):
        data = self.get_data()
        field_names = {"consultation_reason": "Motivo de consulta", "diagnosis": "Diagnóstico", "treatment_evolution": "Tratamiento / Evolución"}
        missing = [field_names.get(k, k) for k in ("consultation_reason", "diagnosis", "treatment_evolution") if not data.get(k)]
        if missing:
            messagebox.showerror("Error de Validación",
                f"Los campos obligatorios deben ser completados: {', '.join(missing)}.")
            return

        if self._gui.on_medical_record_creation:
            self._gui.on_medical_record_creation()

    def get_data(self) -> Dict[str, Any]:
        return {key: ta.get("1.0", tk.END).strip() for key, ta in self.text_areas.items()}

    def clear(self):
        for ta in self.text_areas.values():
            ta.delete("1.0", tk.END)


class Medical_record_read_view(ttk.Frame):
    """Vista de solo lectura: muestra todos los campos de una entrada de historia clínica."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="← Volver a Ficha", style="Secondary.TButton",
                   command=lambda: self._gui.set_view(View.PATIENT_DETAIL)).pack(side="left")

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(card, text="Detalle de Entrada Clínica", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))

        self.lbl_date = ttk.Label(card, text="Fecha: -", style="CardText.TLabel")
        self.lbl_date.pack(anchor="w", pady=2)

        self.fields = {}
        for label_text, key in [("Motivo de Consulta:", "consultation_reason"),
                                ("Diagnóstico:", "diagnosis"),
                                ("Evolución / Tratamiento:", "treatment_evolution"),
                                ("Observaciones:", "observations")]:
            ttk.Label(card, text=label_text, style="CardTitle.TLabel").pack(anchor="w", pady=(12, 2))
            ta = tk.Text(card, wrap="word", bg=PALETTE["bg_white"], fg=PALETTE["text_dark"],
                         highlightbackground=PALETTE["secondary"], relief="flat", borderwidth=1,
                         state="disabled", height=4)
            ta.pack(fill="x", pady=(0, 4))
            self.fields[key] = ta

    def set_data(self, date, consultation_reason, diagnosis, treatment_evolution, observations):
        self.lbl_date.configure(text=f"Fecha: {date}")
        for key, val in [("consultation_reason", consultation_reason),
                         ("diagnosis", diagnosis),
                         ("treatment_evolution", treatment_evolution),
                         ("observations", observations)]:
            ta = self.fields[key]
            ta.configure(state="normal")
            ta.delete("1.0", tk.END)
            ta.insert("1.0", val or "")
            ta.configure(state="disabled")


class Log_view(ttk.Frame):
    """Vista de Auditoría: Muestra la bitácora de acciones del sistema."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(5, 15))
        ttk.Label(header, text="Bitácora de Auditoría (Logs)", style="Title.TLabel").pack(side="left")

        # Tabla de Logs
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("timestamp", "operation")
        self.tree_logs = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree_logs.heading("timestamp", text="Fecha / Hora")
        self.tree_logs.heading("operation", text="Operación")
        
        self.tree_logs.column("timestamp", width=250, anchor="center")
        self.tree_logs.column("operation", width=400, anchor="w")
        
        self.tree_logs.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree_logs.yview)
        self.tree_logs.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        self.tree_logs.bind("<Double-1>", lambda e: self._on_log_double_click())

        # Botón para refrescar logs
        actions_frame = ttk.Frame(self)
        actions_frame.pack(fill="x", pady=(15, 5))
        ttk.Button(actions_frame, text="Actualizar Registros", command=self._on_refresh).pack(side="right")

    def _on_refresh(self):
        if self._gui.on_log_search:
            self._gui.on_log_search()

    def _on_log_double_click(self):
        selected = self.tree_logs.selection()
        if not selected:
            return
        if self._gui.on_log_double_click:
            self._gui.on_log_double_click()


# ==================================
# GRAPHIC USER INTERFACE MAIN CLASS 
# ==================================

class Graphic_user_interface:

    def __init__(self):
        # --- Configuración Base de la Ventana Tkinter ---
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Historias Clinicas - Saca Muela")
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

        # --- Creación del Notebook (Pestañas del Sistema) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. Pestaña de Pacientes 
        self.tab_patients = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_patients, text=" Pacientes ")

        # 2. Pestaña de Auditoría
        self.tab_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_logs, text=" Auditoría de Sistema ")

        # Inicialización de las Vistas Modularizadas en sus respectivas pestañas
        self.views: Dict[View, ttk.Frame] = {}
        self.views[View.MAIN_WINDOW] = General_view(self.tab_patients, self)
        self.views[View.PATIENT_DETAIL] = Detail_view(self.tab_patients, self)
        
        # En la pestaña de Logs, coloca la vista de Auditoría
        self.views[View.LOGS_WINDOW] = Log_view(self.tab_logs, self)

        # Agrega las vistas dinámicas:
        self.views[View.PATIENT_REGISTRATION] = Registration_view(self.tab_patients, self)
        self.views[View.MEDICAL_RECORD_DETAIL] = Record_creation_view(self.tab_patients, self)
        self.views[View.MEDICAL_RECORD_READ] = Medical_record_read_view(self.tab_patients, self)

        # Evento de cambio de pestaña para recargar datos automáticamente
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # Forzar vista inicial dentro de la pestaña Pacientes
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
        self.on_medical_record_detail_view: Optional[Callable[[], None]] = None

    def set_view(self, view_name: View) -> None:
        """Oculta y posiciona las vistas de la pestaña activa o cambia de pestaña."""
        if view_name in [View.MAIN_WINDOW, View.PATIENT_DETAIL, View.PATIENT_REGISTRATION, View.MEDICAL_RECORD_DETAIL, View.MEDICAL_RECORD_READ, View.ALL_PATIENTS]:
            self.notebook.select(0)
            
            # Ocultamos todas las vistas hijas de esta pestaña antes de mostrar la activa
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
        """Dispara las búsquedas y cargas necesarias según la pestaña activa."""
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:  # Pestaña de Logs activa
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

    # --- Métodos de lectura de datos para el Handler ---
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

    # --- Métodos completados para extraer la información ingresada por el usuario ---
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

    # --- Métodos para renderizar datos ---
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