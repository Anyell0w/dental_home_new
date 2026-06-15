# views/dashboard_view.py
import tkinter as tk
from tkinter import ttk
from .components.pacientes_tab import PacientesTab
from .components.citas_tab import CitasTab
from .components.historias_tab import HistoriasTab
from .components.admin_tab import AdminTab

class DashboardView:
    def __init__(self, root, auth_controller, clinic_controller, admin_controller):
        self.root = root
        self.auth_controller = auth_controller
        self.clinic_controller = clinic_controller
        self.admin_controller = admin_controller
        
        self.usuario_sesion = None
        
        # Configurar paleta cromática global corporativa de controles ttk
        self._configurar_estilos_globales()

    def _configurar_estilos_globales(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Propiedades base de los contenedores
        style.configure("Corporate.TFrame", background="#FFFFFF")
        
        # Pestañas de Navegación Superiores (Estilo Microsoft Fluent Tabs)
        style.configure("TNotebook", background="#F3F4F6", borderwidth=0, highlightthickness=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), background="#E1DFDD", foreground="#201F1E", padding=(20, 8), borderwidth=0)
        style.map("TNotebook.Tab",
            background=[("selected", "#FFFFFF"), ("active", "#EF6F5")],
            foreground=[("selected", "#106EBE")]
        )
        
        # Cajas de Texto de entrada de Datos (Entry)
        style.configure("TEntry", fieldbackground="#FFFFFF", borderwidth=1, relief="solid")

    def inicializar_dashboard(self, usuario_autenticado):
        """Monta la estructura visual principal adaptada según el perfil verificado."""
        self.usuario_sesion = usuario_autenticado
        
        # Maximizar la ventana principal de manera elegante
        self.root.title("Dental Home — Consola de Gestión Centralizada")
        self.root.state('zoomed')
        self.root.configure(bg="#F3F4F6")
        
        # 1. Barra Superior Corporativa de Identificación (Top Bar)
        top_bar = tk.Frame(self.root, bg="#106EBE", height=50)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)
        
        lbl_app = tk.Label(top_bar, text="DENTAL HOME", font=("Segoe UI", 12, "bold"), fg="#FFFFFF", bg="#106EBE", padx=20)
        lbl_app.pack(side="left")
        
        # Mostrar metadatos de la sesión activa
        info_usuario = f"Usuario: {self.usuario_sesion['nombreUsuario']}  |  Rol: {self.usuario_sesion['rol']}"
        lbl_user = tk.Label(top_bar, text=info_usuario, font=("Segoe UI", 10, "bold"), fg="#FFFFFF", bg="#106EBE", padx=20)
        lbl_user.pack(side="right")

        # 2. Contenedor de Navegación Dinámica por Pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._inyectar_modulos_por_permisos()

    def _inyectar_modulos_por_permisos(self):
        """Estrategia de segregación de interfaces basada estrictamente en los Roles del sistema."""
        rol = self.usuario_sesion["rol"]
        
        # Modulos compartidos para los perfiles operativos altos y de secretaría
        if rol in ["Administrador", "Secretaria"]:
            self.tab_pacientes = PacientesTab(self.notebook, self.clinic_controller)
            self.notebook.add(self.tab_pacientes, text="   Pacientes   ")
            
            self.tab_citas = CitasTab(self.notebook, self.clinic_controller)
            self.notebook.add(self.tab_citas, text="   Agenda de Citas   ")
            
        # Módulo clínico restringido exclusivo para Odontólogos y Administradores
        if rol in ["Administrador", "Doctor"]:
            self.tab_historias = HistoriasTab(self.notebook, self.clinic_controller)
            self.notebook.add(self.tab_historias, text="   Historias Clínicas   ")
            
        # Módulo de infraestructura y copias de seguridad exclusivo del Administrador
        if rol == "Administrador":
            self.tab_admin = AdminTab(self.notebook, self.admin_controller)
            self.notebook.add(self.tab_admin, text="   Administración de Sistema   ")
