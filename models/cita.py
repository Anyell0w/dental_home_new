# models/cita.py
class Cita:
    def __init__(self, id_cita=None, paciente_id=None, doctor_id=None, fecha=None, hora=None, estado='Pendiente', motivo_cancelacion=None, fecha_registro=None):
        self.id = id_cita
        self.pacienteId = paciente_id
        self.doctorId = doctor_id
        self.fecha = fecha  # Formato YYYY-MM-DD [cite: 38, 147]
        self.hora = hora    # Formato HH:MM [cite: 38, 147]
        self.estado = estado  # 'Pendiente', 'Completada', 'Cancelada' [cite: 36, 51]
        self.motivoCancelacion = motivo_cancelacion 
        self.fechaRegistro = fecha_registro

    @classmethod
    def get_active_appointments(cls, db_conn, date_str):
        """Retorna todas las citas de un día determinado para la pantalla clara de la agenda[cite: 65, 147]."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT c.*, p.nombre || ' ' || p.apellido AS paciente_nombre 
            FROM cita c
            JOIN paciente p ON c.pacienteId = p.id
            WHERE c.fecha = ? AND c.estado != 'Cancelada'
            ORDER BY c.hora ASC
        """
        cursor.execute(query, (date_str,))
        rows = cursor.fetchall()
        conn.close()
        return rows


class RegistroClinico:
    def __init__(self, id_registro=None, historial_id=None, cita_id=None, doctor_id=None, diagnostico=None, tratamiento=None, observaciones=None, fecha_consulta=None):
        self.id = id_registro
        self.historialId = historial_id
        self.citaId = cita_id
        self.doctorId = doctor_id
        self.diagnostico = diagnostico 
        self.tratamiento = tratamiento 
        self.observaciones = observaciones 
        self.fechaConsulta = fecha_consulta


class Receta:
    def __init__(self, id_receta=None, registro_clinico_id=None, paciente_id=None, doctor_id=None, fecha=None, indicaciones_generales=None, archivo_pdf=None):
        self.id = id_receta
        self.registroClinicoId = registro_clinico_id
        self.pacienteId = paciente_id
        self.doctorId = doctor_id
        self.fecha = fecha 
        self.indicacionesGenerales = indicaciones_generales
        self.archivoPDF = archivo_pdf 


class Medicamento:
    def __init__(self, id_medicamento=None, receta_id=None, nombre=None, cantidad=None, indicaciones=None):
        self.id = id_medicamento
        self.recetaId = receta_id
        self.nombre = nombre 
        self.cantidad = cantidad
        self.indicaciones = indicaciones 
