# config.py
import os

# ===========================================================================
# CONFIGURACIÓN GENERAL DEL SISTEMA
# ===========================================================================
APP_NAME = "Dental Home" 
APP_VERSION = "2.0" 

# Rutas del Entorno Local (Operación local pura sin internet) 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_NAME = "dental_home.db"
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)

# ===========================================================================
# PALETA DE COLORES CORPORATIVA (Estilo Microsoft UI)
# ===========================================================================
# Colores dominantes y fondos limpios
COLOR_BG_MAIN = "#FFFFFF"         # Fondo blanco puro para tarjetas y formularios
COLOR_BG_WINDOW = "#F3F4F6"       # Gris claro para el lienzo de fondo de las ventanas

# Celestes mate y azules de acento (Microsoft Corporate Blue)
COLOR_PRIMARY = "#106EBE"         # Azul celeste mate para elementos principales y botones
COLOR_PRIMARY_HOVER = "#005A9E"   # Azul más oscuro para estados interactivos (Hover)
COLOR_ACCENT_LIGHT = "#EF6F5"     # Celeste mate ultra claro para selecciones secundarias

# Tipografía y contenidos
COLOR_TEXT_MAIN = "#201F1E"       # Gris carbón oscuro para legibilidad óptima
COLOR_TEXT_MUTED = "#605E5C"      # Gris medio para subtítulos y descripciones
COLOR_BORDER = "#E1DFDD"          # Gris suave para líneas de separación y bordes

# ===========================================================================
# CONFIGURACIÓN DE TIPOGRAFÍAS (Segoe UI - Estándar Windows/Microsoft)
# ===========================================================================
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 9, "bold")
FONT_INPUT = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")
