# views/components/admin_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class AdminTab(ttk.Frame):
    def __init__(self, parent, admin_controller):
        super().__init__(parent)
        self.controller = admin_controller
        self.configure(style="Corporate.TFrame")
        
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_LIGHT_GRAY = "#F3F4F6"
        self.COLOR_MATTE_BLUE = "#106EBE"
        
        self._setup_admin_ui()

    def _setup_admin_ui(self):
        # Módulo Izquierdo: Gestión y Alta de Usuarios del Sistema
        user_frame = tk.LabelFrame(
            self, text=" Alta de Personal Administrativo / Médico ", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_WHITE, fg="#201F1E", bd=1, relief="solid", padx=20, pady=15
        )
        user_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(user_frame, text="Nombre de Usuario:", bg=self.COLOR_WHITE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        self.ent_username = ttk.Entry(user_frame, font=("Segoe UI", 10))
        self.ent_username.pack(fill="x", pady=(0, 8))

        tk.Label(user_frame, text="Contraseña Inicial:", bg=self.COLOR_WHITE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        self.ent_password = ttk.Entry(user_frame, show="*", font=("Segoe UI", 10))
        self.ent_password.pack(fill="x", pady=(0, 8))

        tk.Label(user_frame, text="Rol del Sistema:", bg=self.COLOR_WHITE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        self.cmb_rol = ttk.Combobox(user_frame, values=["Administrador", "Doctor", "Secretaria"], state="readonly", font=("Segoe UI", 10))
        self.cmb_rol.pack(fill="x", pady=(0, 8))

        tk.Label(user_frame, text="Dato Extendido (Nro Colegiatura / Turno):", bg=self.COLOR_WHITE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        self.ent_extendido = ttk.Entry(user_frame, font=("Segoe UI", 10))
        self.ent_extendido.pack(fill="x", pady=(0, 15))

        self.btn_crear_user = tk.Button(
            user_frame, text="Dar de Alta Usuario", font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_MATTE_BLUE, fg=self.COLOR_WHITE, bd=0, pady=6, cursor="hand2"
        )
        self.btn_crear_user.pack(fill="x")
        self.btn_crear_user.configure(command=self._crear_usuario)

        # Módulo Derecho: Mantenimiento Preventivo e Infraestructura Local de Datos
        infra_frame = tk.LabelFrame(
            self, text=" Infraestructura de Base de Datos Local ", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_WHITE, fg="#201F1E", bd=1, relief="solid", padx=20, pady=15
        )
        infra_frame.pack(side="right", fill="both", expand=True)
        
        tk.Label(
            infra_frame, text="Copias de Seguridad (Backups):", font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_WHITE, fg="#201F1E"
        ).pack(anchor="w", pady=(5, 2))
        
        tk.Label(
            infra_frame, text="Permite duplicar de forma binaria el archivo físico local .db para resguardo integral ante fallos de hardware en el área local.",
            font=("Segoe UI", 9), bg=self.COLOR_WHITE, fg="#605E5C", wraplength=350, justify="left"
        ).pack(anchor="w", pady=(0, 15))

        self.btn_backup = tk.Button(
            infra_frame, text="Ejecutar Copia de Seguridad Manual", font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_LIGHT_GRAY, fg=self.COLOR_MATTE_BLUE, bd=1, relief="solid",
            pady=8, cursor="hand2", activebackground=self.COLOR_WHITE
        )
        self.btn_backup.pack(fill="x", pady=(10, 0))
        self.btn_backup.configure(command=self._ejecutar_backup)

    def _crear_usuario(self):
        success, msg = self.controller.registrar_usuario_sistema(
            self.ent_username.get(), self.ent_password.get(),
            self.cmb_rol.get(), self.ent_extendido.get()
        )
        if success:
            messagebox.showinfo("Dental Home", msg)
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
            self.ent_extendido.delete(0, tk.END)
        else:
            messagebox.showwarning("Atención", msg)

    def _ejecutar_backup(self):
        directorio = filedialog.askdirectory(title="Seleccionar carpeta de resguardo")
        if directorio:
            success, msg = self.controller.ejecutar_respaldo_manual(directorio)
            if success:
                messagebox.showinfo("Dental Home Backup", msg)
            else:
                messagebox.showerror("Error de Respaldo", msg)
