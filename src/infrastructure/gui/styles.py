from tkinter import ttk

# =======================
# CONFIGURACION ESTETICA
# =======================
PALETTE = {
    "bg_light": "#F7F9FC",       # Fondo general
    "bg_white": "#FFFFFF",       # Fondo de tarjetas y contenedores
    "primary": "#8FAADC",        # Azul suave
    "primary_hover": "#7D9BCB",  # Azul hover
    "secondary": "#E2E8F0",      # Gris para bordes y elementos secundarios
    "text_dark": "#2D3748",      # Gris oscuro para legibilidad de textos
    "text_muted": "#718096",     # Gris medio para subtitulos o datos secundarios
    "accent_green": "#A8DADC",   # Verde para exitos o acciones positivas
    "accent_red": "#F5B7B1"      # Rojo/Rosa para errores o destrucciones
}

FONT_FAMILY = "Segoe UI"  # Fuente

def apply_modern_styles():
    """Configura los estilos globales de ttk."""
    style = ttk.Style()
    style.theme_use("clam")

    # Configuracion de frames y labels
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

    # Estilos del Notebook (Pestanas)
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
