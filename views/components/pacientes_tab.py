# views/components/pacientes_tab.py
import tkinter as tk
from tkinter import ttk, messagebox

class PacientesTab(ttk.Frame):
    def __init__(self, parent, clinic_controller):
        super().__init__(parent)
        self.controller = clinic_controller
        self.configure(style="Corporate.TFrame")
        
        # Paleta de Colores Estilo Microsoft
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_LIGHT_GRAY = "#F3F4F6"
        self.COLOR_BORDER = "#E1DFDD"
        self.COLOR_MATTE_BLUE = "#106EBE"
        
        self._setup_layout()

    def _setup_layout(self):
        # Panel Izquierdo: Formulario (Fondo Blanco Tipo Tarjeta)
        self.form_frame = tk.LabelFrame(
            self, text=" Registro de Paciente ", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_WHITE, fg="#201F1E", bd=1, relief="solid", padx=20, pady=15,
            width=350

        )
        self.form_frame.pack(side="left", fill="both", expand=False, padx=(0, 20))
        self.form_frame.pack_propagate(False)

        # Atributos normalizados unificados según especificaciones técnicas
        fields = [
            ("Nombre", "entry_nom"), ("Apellido", "entry_ape"), 
            ("DNI / Cédula", "entry_dni"), ("Teléfono", "entry_tel"), 
            ("Sexo", "entry_sexo"), ("Fecha Nacimiento (YYYY-MM-DD)", "entry_fnac"), 
            ("Dirección", "entry_dir"), ("Edad", "entry_edad")
        ]
        
        self.entries = {}
        for label_text, var_name in fields:
            lbl = tk.Label(self.form_frame, text=label_text, bg=self.COLOR_WHITE, fg="#201F1E", font=("Segoe UI", 9, "bold"))
            lbl.pack(anchor="w", pady=(8, 2))
            
            entry = ttk.Entry(self.form_frame, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 5))
            self.entries[var_name] = entry

        self.btn_guardar = tk.Button(
            self.form_frame, text="Registrar Ficha", font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_MATTE_BLUE, fg=self.COLOR_WHITE, activebackground="#005A9E",
            activeforeground=self.COLOR_WHITE, bd=0, cursor="hand2", pady=6
        )
        self.btn_guardar.pack(fill="x", pady=(15, 0))
        self.btn_guardar.configure(command=self._guardar_paciente)

        # Panel Derecho: Visualizador de Registros y Consultas
        self.view_frame = tk.Frame(self, bg=self.COLOR_WHITE, bd=1, relief="solid")
        self.view_frame.pack(side="right", fill="both", expand=True)

        # Barra de Búsqueda Superior
        self.search_bar = tk.Frame(self.view_frame, bg=self.COLOR_LIGHT_GRAY, pady=10, padx=15)
        self.search_bar.pack(fill="x")
        
        lbl_buscar = tk.Label(self.search_bar, text="Búsqueda Avanzada:", bg=self.COLOR_LIGHT_GRAY, fg="#201F1E", font=("Segoe UI", 9, "bold"))
        lbl_buscar.pack(side="left", padx=(0, 10))
        
        self.ent_buscar = ttk.Entry(self.search_bar, font=("Segoe UI", 10), width=35)
        self.ent_buscar.pack(side="left", padx=(0, 10))
        
        self.btn_buscar = tk.Button(
            self.search_bar, text="Filtrar", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_WHITE, fg=self.COLOR_MATTE_BLUE, bd=1, relief="solid",
            activebackground=self.COLOR_LIGHT_GRAY, cursor="hand2", padx=15
        )
        self.btn_buscar.pack(side="left")
        self.btn_buscar.configure(command=self._cargar_tabla)

        # Tabla de Datos (Treeview) Estilizada de Microsoft
        self.tree = ttk.Treeview(self.view_frame, columns=("ID", "Nombre", "Apellido", "DNI", "Teléfono"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Teléfono", text="Teléfono")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)
        
        self._cargar_tabla()

    def _guardar_paciente(self):
        # Captura y envío de datos hacia el controlador lógico
        success, msg = self.controller.registrar_paciente(
            self.entries["entry_nom"].get(), self.entries["entry_ape"].get(),
            self.entries["entry_dni"].get(), self.entries["entry_tel"].get(),
            self.entries["entry_sexo"].get(), self.entries["entry_fnac"].get(),
            self.entries["entry_dir"].get()
        )
        if success:
            messagebox.showinfo("Dental Home", msg)
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self._cargar_tabla()
        else:
            messagebox.showwarning("Atención", msg)

    def _cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        pacientes = self.controller.buscar_pacientes(self.ent_buscar.get())
        for p in pacientes:
            self.tree.insert("", "end", values=(p['id'], p['nombre'], p['apellido'], p['dni'], p['telefono']))
