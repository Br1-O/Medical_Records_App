import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.gui.Graphic_user_interface import Graphic_user_interface


class Log_view(ttk.Frame):
    """Vista de Auditoria: Muestra la bitacora de acciones del sistema."""
    def __init__(self, parent, gui: 'Graphic_user_interface'):
        super().__init__(parent)
        self._gui = gui
        self._setup_ui()

    def _setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(5, 15))
        ttk.Label(header, text="Bitacora de Auditoria (Logs)", style="Title.TLabel").pack(side="left")

        # Tabla de Logs
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("timestamp", "operation")
        self.tree_logs = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree_logs.heading("timestamp", text="Fecha / Hora")
        self.tree_logs.heading("operation", text="Operacion")

        self.tree_logs.column("timestamp", width=250, anchor="center")
        self.tree_logs.column("operation", width=400, anchor="w")

        self.tree_logs.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree_logs.yview)
        self.tree_logs.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        self.tree_logs.bind("<Double-1>", lambda e: self._on_log_double_click())

        # Boton para refrescar logs
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
