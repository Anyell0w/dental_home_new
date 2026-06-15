# models/paciente.py
from datetime import datetime

class Paciente:
    def __init__(self, id_paciente=None, nombre=None, apellido=None, dni=None, telefono=None, sexo=None, fecha_nacimiento=None, direccion=None, estado=1, registrado_por=None):
        self.id = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni [cite: 25, 147]
        self.telefono = telefono [cite: 25, 147]
        self.sexo = sexo [cite: 25]
        self.fechaNacimiento = fecha_nacimiento [cite: 147]
        self.direccion = direccion [cite: 147]
        self.estado = estado
        self.registradoPor = registrado_por

    def save(self, db_conn):
        """Guarda o actualiza la información personal de cada paciente."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO paciente (nombre, apellido, dni, telefono, sexo, fechaNacimiento, direccion, estado, registradoPor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (self.nombre, self.apellido, self.dni, self.telefono, self.sexo, self.fechaNacimiento, self.direccion, self.estado, self.registradoPor))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self.id


class HistorialClinico:
    def __init__(self, id_historial=None, paciente_id=None, fecha_creacion=None, observaciones=None, activo=1):
        self.id = id_historial
        self.pacienteId = paciente_id
        self.fechaCreacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.observaciones = observaciones
        self.activo = activo

    @classmethod
    def get_by_paciente_id(cls, db_conn, paciente_id):
        """Recupera el historial clínico asociado de forma ordenada[cite: 73, 147]."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM historial_clinico WHERE pacienteId = ?"
        cursor.execute(query, (paciente_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["pacienteId"], row["fechaCreacion"], row["observaciones"], row["activo"])
        return None
