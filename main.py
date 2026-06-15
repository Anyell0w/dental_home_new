# main.py
import tkinter as tk
from database.connection import DatabaseConnection
from controllers.auth_controller import AuthController
from controllers.clinic_controller import ClinicController
from controllers.admin_controller import AdminController
from views.login_view import LoginView
from views.dashboard_view import DashboardView
import config

class DentalHomeApplication:
    def __init__(self):
        # 1. Inicializar la raíz oculta de Tkinter para controlar el ciclo de vida global
        self.root = tk.Tk()
        self.root.withdraw()  # Mantener oculta la ventana principal hasta que el login sea exitoso
        
        print(f"[{config.APP_NAME}] Iniciando entorno local versión {config.APP_VERSION}...") 

        try:
            # 2. Inicializar Infraestructura de Persistencia (SQLite local en 3FN)
            self.db_connection = DatabaseConnection(db_name=config.DATABASE_NAME)
        except Exception as e:
            print(f"Error crítico al conectar con la base de datos local: {e}")
            self.root.destroy()
            return

        # 3. Instanciar Capa de Controladores (Inyección de dependencias del Modelo hacia el Controlador)
        self.auth_controller = AuthController(self.db_connection)
        self.clinic_controller = ClinicController(self.db_connection, self.auth_controller)
        self.admin_controller = AdminController(self.db_connection, self.auth_controller)

        # 4. Instanciar el Contenedor Maestro de la Vista (Dashboard)
        self.dashboard_view = DashboardView(
            root=self.root,
            auth_controller=self.auth_controller,
            clinic_controller=self.clinic_controller,
            admin_controller=self.admin_controller
        )

        # 5. Lanzar la ventana modal de Login Corporativo
        self.mostrar_login()

    def mostrar_login(self):
        """Despliega la interfaz de Login y le inyecta el callback de éxito."""
        # Se le pasa self.root como padre y la función de transición como manejador
        self.login_window = LoginView(
            parent=self.root,
            auth_controller=self.auth_controller,
            on_login_success=self.transicion_a_dashboard
        )

    def transicion_a_dashboard(self, usuario_autenticado):
        """Callback que se ejecuta de forma automática al verificar credenciales válidas."""
        print(f"[Core] Autenticación validada. Redirigiendo al rol: {usuario_autenticado['rol']}...")
        
        # Hacer visible la ventana principal de la aplicación
        self.root.deiconify()
        
        # Inicializar los componentes dinámicos del Dashboard según los permisos del Rol
        self.dashboard_view.inicializar_dashboard(usuario_autenticado)

    def arrancar(self):
        """Inicia el bucle de eventos principal del sistema de escritorio."""
        self.root.mainloop()

if __name__ == "__main__":
    # Punto de entrada único del software de escritorio local 
    app = DentalHomeApplication()
    app.arrancar()
