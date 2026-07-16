import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from domain.Enums.View import View
from infrastructure.gui.styles import PALETTE

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


class Medical_record_read_view(ttk.Frame):
    """Vista de solo lectura: muestra todos los campos de una entrada de historia clinica."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="<- Volver a Ficha", style="Secondary.TButton",
                   command=lambda: self._gui.set_view(View.PATIENT_DETAIL)).pack(side="left")

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=10, pady=10, ipady=15, ipadx=15)

        ttk.Label(card, text="Detalle de Entrada Clinica", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))

        self.lbl_date = ttk.Label(card, text="Fecha: -", style="CardText.TLabel")
        self.lbl_date.pack(anchor="w", pady=2)

        self.fields = {}
        for label_text, key in [("Motivo de Consulta:", "consultation_reason"),
                                ("Diagnostico:", "diagnosis"),
                                ("Evolucion / Tratamiento:", "treatment_evolution"),
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
