import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from domain.Enums.View import View
from infrastructure.gui.styles import PALETTE

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


class Detail_view(ttk.Frame):
    """Vista Detalle: Muestra la informacion del Paciente y su Historial de Consultas."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 10))
        ttk.Button(top_bar, text="<- Volver al Listado", style="Secondary.TButton",
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
        self.lbl_gender = ttk.Label(info_grid, text="Genero: -", style="CardText.TLabel")
        self.lbl_gender.grid(row=0, column=2, sticky="w", pady=1)

        self.lbl_phone = ttk.Label(info_grid, text="Telefono: -", style="CardText.TLabel")
        self.lbl_phone.grid(row=1, column=0, sticky="w", padx=(0, 30), pady=1)
        self.lbl_emergency = ttk.Label(info_grid, text="Contacto Emergencia: -", style="CardText.TLabel")
        self.lbl_emergency.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=1)

        self.lbl_insurance = ttk.Label(info_grid, text="Obra Social: -", style="CardText.TLabel")
        self.lbl_insurance.grid(row=2, column=0, sticky="w", padx=(0, 30), pady=1)
        self.lbl_insurance_num = ttk.Label(info_grid, text="Nro Obra Social: -", style="CardText.TLabel")
        self.lbl_insurance_num.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=1)
        self.lbl_status = ttk.Label(info_grid, text="Estado: -", style="CardText.TLabel")
        self.lbl_status.grid(row=2, column=2, sticky="w", pady=1)

        # Botones de Accion -  tk.Frame para el fondo
        btn_box = tk.Frame(self.card, background=PALETTE["bg_white"])
        btn_box.pack(anchor="e", pady=(10, 0))

        # El boton editar datos redirige al formulario con la informacion cargada
        ttk.Button(btn_box, text="Editar Datos",
                   command=self._on_edit_patient).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Dar de Baja", style="Danger.TButton",
                   command=self._on_delete_patient).pack(side="left", padx=5)
        self.btn_reactivate = ttk.Button(btn_box, text="Reactivar", style="Success.TButton",
                   command=self._on_reactivate_patient)
        self.btn_reactivate.pack(side="left", padx=5)
        self.btn_reactivate.pack_forget()

        # Seccion de Historia Clinica
        ttk.Label(self, text="Historia Clinica", style="CardTitle.TLabel").pack(anchor="w", pady=(10, 5))

        # Barra de busqueda de evoluciones
        record_search_frame = ttk.Frame(self)
        record_search_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(record_search_frame, text="Buscar entrada:").pack(side="left", padx=(0, 5))
        self.record_search_entry = ttk.Entry(record_search_frame, width=25)
        self.record_search_entry.pack(side="left", padx=(0, 5))
        self.record_search_type = ttk.Combobox(record_search_frame, values=["Fecha", "Diagnostico", "Tratamiento"], state="readonly", width=14)
        self.record_search_type.set("Diagnostico")
        self.record_search_type.pack(side="left", padx=(0, 5))
        ttk.Button(record_search_frame, text="Buscar", command=self._on_search_record).pack(side="left")
        ttk.Button(record_search_frame, text="Limpiar", command=self._on_clear_search_record).pack(side="left", padx=(5, 0))

        self.history_frame = ttk.Frame(self)
        self.history_frame.pack(fill="both", expand=True)

        columns = ("date", "motivo", "diagnostico")
        self.tree_history = ttk.Treeview(self.history_frame, columns=columns, show="headings")
        self.tree_history.heading("date", text="Fecha")
        self.tree_history.heading("motivo", text="Motivo de Consulta")
        self.tree_history.heading("diagnostico", text="Diagnostico")

        self.tree_history.column("date", width=150, anchor="center")
        self.tree_history.column("motivo", width=300, anchor="w")
        self.tree_history.column("diagnostico", width=300, anchor="w")

        self.tree_history.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.tree_history.yview)
        self.tree_history.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        self.tree_history.bind("<Double-1>", lambda e: self._on_view_record())

        # Acciones de Historia Clinica
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

    def set_active_status(self, is_active: bool) -> None:
        if is_active:
            self.btn_reactivate.pack_forget()
        else:
            self.btn_reactivate.pack(side="left", padx=5)

    def _on_delete_patient(self):
        if messagebox.askyesno("Atencion", "Esta seguro de que desea dar de baja a este paciente?"):
            if self._gui.on_patient_delete:
                self._gui.on_patient_delete()

    def _on_reactivate_patient(self):
        if messagebox.askyesno("Atencion", "Desea reactivar este paciente?"):
            if self._gui.on_patient_reactivate:
                self._gui.on_patient_reactivate()

    def _on_delete_record(self):
        selected = self.tree_history.selection()
        if not selected:
            messagebox.showwarning("Atencion", "Por favor, seleccione una entrada de la lista.")
            return
        if messagebox.askyesno("Atencion", "Desea anular de forma permanente esta entrada medica?"):
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
        self.record_search_type.set("Diagnostico")
        if self._gui.on_medical_record_search:
            self._gui.on_medical_record_search()
