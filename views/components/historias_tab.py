# views/components/historias_tab.py
import tkinter as tk
from tkinter import ttk, messagebox

class HistoriasTab(ttk.Frame):
    def __init__(self, parent, clinic_controller):
        super().__init__(parent)
        self.controller = clinic_controller
        self.configure(style="Corporate.TFrame")
        
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_MATTE_BLUE = "#106EBE"
        
        self._setup_clinical_ui()

    def _setup_clinical_ui(self):
        # Panel superior de selección rápida de historia clínica activa
        top_selector = tk.Frame(self, bg=self.COLOR_WHITE, bd=1, relief="solid", pady=12, padx=15)
        top_selector.pack(fill="x", pady=(0, 15))
        
        tk.Label(top_selector, text="ID Expediente Paciente:", font=("Segoe UI", 10, "bold"), bg=self.COLOR_WHITE).pack(side="left", padx=(0, 10))
        self.ent_paciente_id = ttk.Entry(top_selector, width=15, font=("Segoe UI", 10))
        self.ent_paciente_id.pack(side="left", padx=(0, 15))
        
        tk.Label(top_selector, text="ID Cita Asociada (Opcional):", font=("Segoe UI", 10, "bold"), bg=self.COLOR_WHITE).pack(side="left", padx=(0, 10))
        self.ent_cita_id = ttk.Entry(top_selector, width=15, font=("Segoe UI", 10))
        self.ent_cita_id.pack(side="left")

        # Área de captura de notas evolutivas médicas
        content_frame = tk.Frame(self, bg=self.COLOR_WHITE, bd=1, relief="solid", padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)

        tk.Label(content_frame, text="Diagnóstico Clínico:", font=("Segoe UI", 10, "bold"), bg=self.COLOR_WHITE).pack(anchor="w", pady=(5, 2))
        self.txt_diagnostico = tk.Text(content_frame, height=4, font=("Segoe UI", 10), bd=1, relief="solid")
        self.txt_diagnostico.pack(fill="x", pady=(0, 10))

        tk.Label(content_frame, text="Tratamiento Realizado:", font=("Segoe UI", 10, "bold"), bg=self.COLOR_WHITE).pack(anchor="w", pady=(5, 2))
        self.txt_tratamiento = tk.Text(content_frame, height=4, font=("Segoe UI", 10), bd=1, relief="solid")
        self.txt_tratamiento.pack(fill="x", pady=(0, 10))

        tk.Label(content_frame, text="Observaciones de Control:", font=("Segoe UI", 10, "bold"), bg=self.COLOR_WHITE).pack(anchor="w", pady=(5, 2))
        self.txt_observaciones = tk.Text(content_frame, height=3, font=("Segoe UI", 10), bd=1, relief="solid")
        self.txt_observaciones.pack(fill="x", pady=(0, 15))

        # Botón corporativo alineado a la derecha
        self.btn_finalizar = tk.Button(
            content_frame, text="Guardar Atención Clínica y Generar Receta", font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_MATTE_BLUE, fg=self.COLOR_WHITE, bd=0, pady=8, cursor="hand2"
        )
        self.btn_finalizar.pack(side="right")
        self.btn_finalizar.configure(command=self._guardar_evolucion)

    def _guardar_evolucion(self):
        success, msg = self.controller.registrar_atencion_clinica(
            self.ent_paciente_id.get(), self.ent_cita_id.get(),
            self.txt_diagnostico.get("1.0", tk.END), self.txt_tratamiento.get("1.0", tk.END),
            self.txt_observaciones.get("1.0", tk.END)
        )
        if success:
            messagebox.showinfo("Dental Home", msg)
            self.txt_diagnostico.delete("1.0", tk.END)
            self.txt_tratamiento.delete("1.0", tk.END)
            self.txt_observaciones.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Error de validación", msg)
