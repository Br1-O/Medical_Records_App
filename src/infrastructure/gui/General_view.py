import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from domain.Enums.View import View
from infrastructure.gui.styles import PALETTE

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


class General_view(ttk.Frame):
    """Vista General: Contiene la tabla principal de pacientes y la barra de busqueda."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(5, 15))
        ttk.Label(header, text="Busqueda de Pacientes", style="Title.TLabel").pack(side="left")

        # Formulario de Busqueda
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
            messagebox.showwarning("Atencion", "Por favor, seleccione un paciente de la lista para ver su ficha detallada.")
            return

        if self._gui.on_patient_detail_view:
            self._gui.on_patient_detail_view()
        self._gui.set_view(View.PATIENT_DETAIL)
