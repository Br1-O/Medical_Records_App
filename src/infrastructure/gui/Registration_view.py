import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, TYPE_CHECKING

from domain.Enums.View import View
from infrastructure.gui.styles import PALETTE

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


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
        ttk.Button(top_bar, text="<- Volver al Listado", style="Secondary.TButton",
                   command=lambda: self._gui.set_view(View.MAIN_WINDOW)).pack(side="left")

        # Contenedor del Formulario
        form_container = ttk.Frame(self, style="Card.TFrame")
        form_container.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(form_container, text="Ficha de Datos de Paciente", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Campos clave de entrada
        fields = [
            "DNI (*):", "Nombre (*):", "Apellido (*):", "Genero (*):",
            "Telefono (*):", "Contacto de Emergencia (*):",
            "Obra Social / Prepaga:", "Nro Obra Social:"
        ]
        field_keys = [
            "dni", "name", "last_name", "gender",
            "phone", "emergency_contact",
            "health_insurance_name", "health_insurance_number"
        ]

        for i, (label_text, field_key) in enumerate(zip(fields, field_keys)):
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

        # Selector de fecha de nacimiento (Ano-Mes-Dia)
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

        # Caja de botones inferiores de accion
        btn_container = tk.Frame(form_container, background=PALETTE["bg_white"])
        btn_container.grid(row=len(fields)+2, column=1, sticky="e", pady=(20, 0))

        ttk.Button(btn_container, text="Guardar Paciente", style="Success.TButton",
                   command=self._on_save).pack(side="right", padx=5)
        ttk.Button(btn_container, text="Cancelar", style="Secondary.TButton",
                   command=self._on_cancel).pack(side="right", padx=5)

    def _on_save(self):
        data = self.get_data()
        required_fields = ["dni", "name", "last_name", "birth_date", "gender", "phone", "emergency_contact"]
        field_names = {"dni": "DNI", "name": "Nombre", "last_name": "Apellido", "birth_date": "Fecha de nacimiento", "gender": "Genero", "phone": "Telefono", "emergency_contact": "Contacto de emergencia"}
        missing = [field_names.get(f, f) for f in required_fields if not data.get(f)]

        if missing:
            messagebox.showerror("Error de Validacion", f"Los campos obligatorios deben ser completados: {', '.join(missing)}.")
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
