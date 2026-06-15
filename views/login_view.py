# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Toplevel):
    def __init__(self, parent, auth_controller, on_login_success):
        super().__init__(parent)
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        
        # Configuración de ventana profesional fija
        self.title("Dental Home - Acceso")
        self.geometry("380x520")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        
        # Centrar la ventana de login en la pantalla del usuario
        self.util_centrar_ventana()
        
        # Ocultar la ventana raíz temporalmente mientras dura el login
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar_login)
        
        # Paleta de Colores Corporativa
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_TEXT = "#201F1E"
        self.COLOR_SUBTEXT = "#605E5C"
        self.COLOR_BLUE_MATTE = "#106EBE"
        self.COLOR_BLUE_HOVER = "#005A9E"
        
        self._construir_interfaz()

    def util_centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _construir_interfaz(self):
        # 1. Contenedor del Logo de la Aplicación (Espacio dedicado para Identidad Corporativa)
        self.logo_canvas = tk.Canvas(self, width=100, height=100, bg=self.COLOR_WHITE, bd=0, highlightthickness=0)
        self.logo_canvas.pack(pady=(40, 10))
        
        # Dibujo vectorial de un isotipo de salud/dental abstracto minimalista
        self.logo_canvas.create_rectangle(35, 20, 65, 80, fill="#E1DFDD", outline="")
        self.logo_canvas.create_rectangle(20, 35, 80, 65, fill=self.COLOR_BLUE_MATTE, outline="")
        self.logo_canvas.create_oval(40, 40, 60, 60, fill=self.COLOR_WHITE, outline="")

        # 2. Etiquetas de Bienvenida
        lbl_titulo = tk.Label(self, text="Dental Home", font=("Segoe UI", 20, "bold"), bg=self.COLOR_WHITE, fg=self.COLOR_TEXT)
        lbl_titulo.pack()
        
        lbl_subtitulo = tk.Label(self, text="Inicie sesión para acceder al área local", font=("Segoe UI", 10), bg=self.COLOR_WHITE, fg=self.COLOR_SUBTEXT)
        lbl_subtitulo.pack(pady=(5, 30))

        # 3. Formulario de Credenciales de Entrada
        form_frame = tk.Frame(self, bg=self.COLOR_WHITE, padx=35)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Nombre de usuario", font=("Segoe UI", 9, "bold"), bg=self.COLOR_WHITE, fg=self.COLOR_TEXT).pack(anchor="w")
        self.ent_usuario = ttk.Entry(form_frame, font=("Segoe UI", 11))
        self.ent_usuario.pack(fill="x", pady=(5, 20))
        self.ent_usuario.focus_set()

        tk.Label(form_frame, text="Contraseña", font=("Segoe UI", 9, "bold"), bg=self.COLOR_WHITE, fg=self.COLOR_TEXT).pack(anchor="w")
        self.ent_contrasena = ttk.Entry(form_frame, show="*", font=("Segoe UI", 11))
        self.ent_contrasena.pack(fill="x", pady=(5, 30))
        
        # Enlazar la tecla Enter para procesar el formulario de forma directa
        self.ent_contrasena.bind("<Return>", lambda event: self._procesar_login())

        # 4. Botón de Acción Principal (Estilo Microsoft Flat Blue)
        self.btn_ingresar = tk.Button(
            self, text="Iniciar Sesión", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_BLUE_MATTE, fg=self.COLOR_WHITE, activebackground=self.COLOR_BLUE_HOVER,
            activeforeground=self.COLOR_WHITE, bd=0, cursor="hand2", pady=8
        )
        self.btn_ingresar.pack(fill="x", padx=35)
        self.btn_ingresar.configure(command=self._procesar_login)

    def _procesar_login(self):
        usuario = self.ent_usuario.get()
        contrasena = self.ent_contrasena.get()
        
        # Delegar la validación y autenticación a la capa de control lógico
        exito, resultado = self.auth_controller.iniciar_sesion(usuario, contrasena)
        
        if exito:
            self.destroy() # Liberar la vista de login de la memoria
            self.on_login_success(resultado) # Notificar la sesión activa al Dashboard
        else:
            messagebox.showerror("Error de Acceso", resultado)

    def _al_cerrar_login(self):
        # Detener la ejecución del hilo principal de la aplicación si se cierra el Login
        self.master.destroy()
