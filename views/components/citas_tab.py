# views/components/citas_tab.py
import tkinter as tk
from tkinter import ttk, messagebox

class CitasTab(ttk.Frame):
    def __init__(self, parent, clinic_controller):
        super().__init__(parent)
        self.controller = clinic_controller
        self.configure(style="Corporate.TFrame")
        
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_LIGHT_GRAY = "#F3F4F6"
        self.COLOR_MATTE_BLUE = "#106EBE"
        
        self._setup_ui()

    def _setup_ui(self):
        # Encabezado Operativo de la Agenda
        header_frame = tk.Frame(self, bg=self.COLOR_WHITE, pady=10)
        header_frame.pack(fill="x", pady=(0, 15))
        
        lbl_titulo = tk.Label(header_frame, text="Planificación y Control de Agenda", font=("Segoe UI", 16, "bold"), bg=self.COLOR_WHITE, fg="#201F1E")
        lbl_titulo.pack(side="left")

        # Selectores de período estilo Microsoft Segmented Control
        period_frame = tk.Frame(header_frame, bg=self.COLOR_WHITE)
        period_frame.pack(side="right")
        
        for periodo in ["Día", "Semana", "Mes"]:
            btn = tk.Button(
                period_frame, text=periodo, font=("Segoe UI", 9, "bold"),
                bg=self.COLOR_LIGHT_GRAY, fg="#201F1E", bd=0, padx=15, pady=5, cursor="hand2"
            )
            btn.pack(side="left", padx=2)

        # Contenedor Principal Separador
        main_content = tk.Frame(self, bg=self.COLOR_WHITE, bd=1, relief="solid")
        main_content.pack(fill="both", expand=True)

        # Formulario de Nueva Cita (Superior)
        form_cita = tk.Frame(main_content, bg=self.COLOR_WHITE, padx=15, pady=15)
        form_cita.pack(fill="x", side="top")
        
        # Grid de campos limpios alineados horizontalmente
        labels = ["ID Paciente:", "ID Doctor:", "Fecha (YYYY-MM-DD):", "Hora (HH:MM):"]
        self.fields = {}
        
        for i, label_text in enumerate(labels):
            lbl = tk.Label(form_cita, text=label_text, bg=self.COLOR_WHITE, font=("Segoe UI", 9, "bold"))
            lbl.grid(row=0, column=i*2, padx=(10, 5), sticky="w")
            entry = ttk.Entry(form_cita, width=15, font=("Segoe UI", 10))
            entry.grid(row=0, column=i*2+1, pady=5)
            self.fields[label_text] = entry

        self.btn_agendar = tk.Button(
            form_cita, text="Agendar Cita", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_MATTE_BLUE, fg=self.COLOR_WHITE, bd=0, padx=20, cursor="hand2"
        )
        self.btn_agendar.grid(row=0, column=8, padx=20, sticky="e")
        self.btn_agendar.configure(command=self._agendar_cita)

        # Tabla de visualización de Citas Existentes
        self.tree_citas = ttk.Treeview(main_content, columns=("ID", "Paciente", "Doctor", "Fecha", "Hora", "Estado"), show="headings")
        self.tree_citas.heading("ID", text="ID")
        self.tree_citas.heading("Paciente", text="Paciente")
        self.tree_citas.heading("Doctor", text="Médico Especialista")
        self.tree_citas.heading("Fecha", text="Fecha")
        self.tree_citas.heading("Hora", text="Hora Bloque")
        self.tree_citas.heading("Estado", text="Estado Cita")
        
        self.tree_citas.pack(fill="both", expand=True, padx=15, pady=15)

    def _agendar_cita(self):
        success, msg = self.controller.agendar_citas(
            self.fields["ID Paciente:"].get(), self.fields["ID Doctor:"].get(),
            self.fields["Fecha (YYYY-MM-DD):"].get(), self.fields["Hora (HH:MM):"].get()
        )
        if success:
            messagebox.showinfo("Dental Home", msg)
            for entry in self.fields.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Conflicto", msg)
