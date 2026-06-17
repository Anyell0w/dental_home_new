# controllers/clinic_controller.py
from datetime import datetime

class ClinicController:
    def __init__(self, db_connection, auth_controller):
        self.db = db_connection
        self.auth = auth_controller

    # =========================================================================
    # SECCIÓN: GESTIÓN DE PACIENTES 
    # =========================================================================
    def registrar_paciente(self, nombre, apellido, dni, telefono, sexo, fecha_nacimiento, direccion):
        """Valida e inserta un nuevo paciente, inicializando su historial clínico de forma atómica."""
        # Validación de campos obligatorios mínimos 
        if not nombre.strip() or not apellido.strip() or not dni.strip():
            return False, "Los campos Nombre, Apellido y DNI son obligatorios para el expediente." 

        conn = self.db.get_connection()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn.execute("BEGIN TRANSACTION;") # Garantiza atomicidad de composición (Paciente + Historial)
            
            # 1. Registrar Paciente 
            query_paciente = """
                INSERT INTO paciente (nombre, apellido, dni, telefono, sexo, fechaNacimiento, direccion, estado, registradoPor)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
            """
            cursor.execute(query_paciente, (
                nombre.strip(), apellido.strip(), dni.strip(), 
                telefono.strip(), sexo, fecha_nacimiento, direccion.strip(),
                self.auth.usuario_actual["id"]
            ))
            paciente_id = cursor.lastrowid

            # 2. Inicializar Historial Clínico (Relación de Composición 1:1 estricta)
            query_historial = """
                INSERT INTO historial_clinico (pacienteId, fechaCreacion, observaciones, activo)
                VALUES (?, ?, 'Historial de atención abierto de forma automática.', 1)
            """
            cursor.execute(query_historial, (paciente_id, fecha_actual))
            
            conn.commit()
            return True, f"Paciente registrado exitosamente con ID interno: {paciente_id}." 
        except Exception as e:
            conn.rollback()
            return False, f"Error al guardar la ficha (posible DNI duplicado): {str(e)}"
        finally:
            conn.close()

    def buscar_pacientes(self, termino_busqueda):
        """Permite localizar de forma ágil a un paciente por nombre, apellido o DNI[cite: 4, 147]."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM paciente 
            WHERE nombre LIKE ? OR apellido LIKE ? OR dni LIKE ?
        """
        like_param = f"%{termino_busqueda.strip()}%"
        cursor.execute(query, (like_param, like_param, like_param))
        resultados = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return resultados

    # =========================================================================
    # SECCIÓN: AGENDA Y CITAS 
    # =========================================================================
    def verificar_cruce_horario(self, doctor_id, fecha, hora, cita_id_ignorar=None):
        """Verifica que no exista otra cita programada en el mismo horario para un doctor específico."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if cita_id_ignorar:
            query = "SELECT COUNT(*) FROM cita WHERE doctorId = ? AND fecha = ? AND hora = ? AND id != ? AND estado != 'Cancelada'"
            cursor.execute(query, (doctor_id, fecha, hora, cita_id_ignorar))
        else:
            query = "SELECT COUNT(*) FROM cita WHERE doctorId = ? AND fecha = ? AND hora = ? AND estado != 'Cancelada'"
            cursor.execute(query, (doctor_id, fecha, hora))
            
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def agendar_citas(self, paciente_id, doctor_id, fecha, hora):
        """Inserta una nueva cita validando previamente la disponibilidad de agenda."""
        if self.verificar_cruce_horario(doctor_id, fecha, hora):
            return False, "Conflicto de Agenda: El doctor seleccionado ya cuenta con una cita en ese bloque horario." 

        conn = self.db.get_connection()
        cursor = conn.cursor()
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            query = """
                INSERT INTO cita (pacienteId, doctorId, fecha, hora, estado, fechaRegistro)
                VALUES (?, ?, ?, ?, 'Pendiente', ?)
            """
            cursor.execute(query, (paciente_id, doctor_id, fecha, hora, fecha_registro))
            conn.commit()
            return True, "Cita agendada correctamente." 
        except Exception as e:
            return False, f"Error al procesar el agendamiento: {str(e)}"
        finally:
            conn.close()

    def cancelar_cita(self, cita_id, motivo):
        """Modifica el estado de la cita a Cancelada registrando obligatoriamente el motivo"""
        if not motivo.strip():
            return False, "Debe ingresar obligatoriamente un motivo para proceder con la cancelación." 
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE cita SET estado = 'Cancelada', motivoCancelacion = ? WHERE id = ?"
            cursor.execute(query, (motivo.strip(), cita_id))
            conn.commit()
            return True, "La cita fue cancelada de forma exitosa."
        except Exception as e:
            return False, f"Error al cancelar la cita: {str(e)}"
        finally:
            conn.close()

    # =========================================================================
    # SECCIÓN: ATENCIÓN CLÍNICA (REQUISITOS EXCLUSIVOS DEL DOCTOR) 
    # =========================================================================
    def registrar_atencion_clinica(self, paciente_id, cita_id, diagnostico, tratamiento, observaciones, medicamentos=None):
        """
        Registra las notas evolutivas de la consulta asociadas al historial clínico[cite: 74, 75, 77].
        Si incluye medicamentos, genera automáticamente la estructura de la receta[cite: 100, 103].
        """
        if not diagnostico.strip() or not tratamiento.strip():
            return False, "Los campos Diagnóstico y Tratamiento no pueden estar vacíos en el registro."
        conn = self.db.get_connection()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn.execute("BEGIN TRANSACTION;")

            # 1. Recuperar el ID del Historial Clínico del paciente
            cursor.execute("SELECT id FROM historial_clinico WHERE pacienteId = ?", (paciente_id,))
            historial_row = cursor.fetchone()
            if not historial_row:
                raise Exception("No se localizó un Historial Clínico estructurado para este paciente.")
            historial_id = historial_row["id"]

            # 2. Insertar Registro Clínico [cite: 77]
            query_registro = """
                INSERT INTO registro_clinico (historialId, citaId, doctorId, diagnostico, tratamiento, observaciones, fechaConsulta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_registro, (
                historial_id, cita_id, self.auth.usuario_actual["id"],
                diagnostico.strip(), tratamiento.strip(), observaciones.strip(), fecha_consulta
            ))
            registro_id = cursor.lastrowid

            # 3. Si la atención viene de una cita agendada, marcarla como Completada
            if cita_id:
                cursor.execute("UPDATE cita SET estado = 'Completada' WHERE id = ?", (cita_id,))

            # 4. Procesar Receta y Medicamentos de forma estructurada si existen 
            if medicamentos:
                query_receta = """
                    INSERT INTO receta (registroClinicoId, pacienteId, doctorId, fecha, indicacionesGenerales, archivoPDF)
                    VALUES (?, ?, ?, ?, 'Tomar según las indicaciones adjuntas por cada medicamento.', ?)
                """
                pdf_path = f"recetas/receta_{registro_id}.pdf"
                cursor.execute(query_receta, (registro_id, paciente_id, self.auth.usuario_actual["id"], fecha_actual, pdf_path))
                receta_id = cursor.lastrowid

                # Insertar cada medicamento de la lista (Composición) [cite: 101, 103]
                query_med = "INSERT INTO medicamento (recetaId, nombre, cantidad, indicaciones) VALUES (?, ?, ?, ?)"
                for med in medicamentos:
                    cursor.execute(query_med, (receta_id, med['nombre'], med['cantidad'], med['indicaciones']))

            conn.commit()
            return True, "Evolución clínica y receta médica guardadas correctamente en el historial." 
        except Exception as e:
            conn.rollback()
            return False, f"Fallo al registrar la consulta en la base de datos local: {str(e)}"
        finally:
            conn.close()
