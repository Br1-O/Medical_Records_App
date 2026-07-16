import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, TYPE_CHECKING

from domain.Enums.View import View
from infrastructure.gui.styles import PALETTE

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


class Record_creation_view(ttk.Frame):
    """Vista de Entrada Clinica: Permite agregar una nueva entrada a la historia clinica."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self.text_areas = {}
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="<- Volver a Ficha", style="Secondary.TButton",
                   command=lambda: self._gui.set_view(View.PATIENT_DETAIL)).pack(side="left")

        form_container = ttk.Frame(self, style="Card.TFrame")
        form_container.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(form_container, text="Nueva Entrada de Historia Clinica", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        fields = [
            ("Motivo de Consulta (*):", "consultation_reason", 3),
            ("Diagnostico (*):", "diagnosis", 3),
            ("Evolucion / Tratamiento (*):", "treatment_evolution", 5),
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
        field_names = {"consultation_reason": "Motivo de consulta", "diagnosis": "Diagnostico", "treatment_evolution": "Tratamiento / Evolucion"}
        missing = [field_names.get(k, k) for k in ("consultation_reason", "diagnosis", "treatment_evolution") if not data.get(k)]
        if missing:
            messagebox.showerror("Error de Validacion",
                f"Los campos obligatorios deben ser completados: {', '.join(missing)}.")
            return

        if self._gui.on_medical_record_creation:
            self._gui.on_medical_record_creation()

    def get_data(self) -> Dict[str, Any]:
        return {key: ta.get("1.0", tk.END).strip() for key, ta in self.text_areas.items()}

    def clear(self):
        for ta in self.text_areas.values():
            ta.delete("1.0", tk.END)
