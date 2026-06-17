# models/usuario.py
from datetime import datetime


class Administrador(Usuario):
    def __init__(self, id_usuario=None, nombre_usuario=None, contrasena=None, activo=1, fecha_creacion=None):
        super().__init__(id_usuario, nombre_usuario, contrasena, "Administrador", activo, fecha_creacion)

    def save(self, db_conn):
        """Persiste la información del Administrador aplicando la herencia 3FN."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN TRANSACTION;")
            query = "INSERT INTO administrador (nombreUsuario, contraseña, activo, fechaCreacion) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (self.nombreUsuario, self.contraseña, self.activo, self.fechaCreacion))
            self.id = cursor.lastrowid
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


class Usuario:
    def __init__(self, id_usuario=None, nombre_usuario=None, contrasena=None, rol=None, activo=1, fecha_creacion=None):
        self.id = id_usuario
        self.nombreUsuario = nombre_usuario
        self.contraseña = contrasena
        self.rol = rol  # 'Administrador', 'Doctor', 'Secretaria' [cite: 9, 147]
        self.activo = activo
        self.fechaCreacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_by_username(cls, db_conn, username):
        """Busca un usuario activo por su nombre de usuario[cite: 10, 147]."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM usuario WHERE nombreUsuario = ? AND activo = 1"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["nombreUsuario"], row["contraseña"], row["rol"], row["activo"], row["fechaCreacion"])
        return None


class Doctor(Usuario):
    def __init__(self, id_usuario=None, nombre_usuario=None, contrasena=None, activo=1, fecha_creacion=None, numero_colegiatura=None):
        super().__init__(id_usuario, nombre_usuario, contrasena, "Doctor", activo, fecha_creacion)
        self.numeroColegiatura = numero_colegiatura

    def save(self, db_conn):
        """Persiste la información del Doctor aplicando la herencia 3FN."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN TRANSACTION;")
            # Insertar en tabla padre
            query_u = "INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query_u, (self.nombreUsuario, self.contraseña, self.rol, self.activo, self.fechaCreacion))
            self.id = cursor.lastrowid
            
            # Insertar en tabla hija (Subclase)
            query_d = "INSERT INTO doctor (usuarioId, numeroColegiatura) VALUES (?, ?)"
            cursor.execute(query_d, (self.id, self.numeroColegiatura))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


class Secretaria(Usuario):
    def __init__(self, id_usuario=None, nombre_usuario=None, contrasena=None, activo=1, fecha_creacion=None, turno=None):
        super().__init__(id_usuario, nombre_usuario, contrasena, "Secretaria", activo, fecha_creacion)
        self.turno = turno

    def save(self, db_conn):
        """Persiste la información de la Secretaria aplicando la herencia 3FN."""
        conn = db_conn.get_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN TRANSACTION;")
            query_u = "INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query_u, (self.nombreUsuario, self.contraseña, self.rol, self.activo, self.fechaCreacion))
            self.id = cursor.lastrowid
            
            query_s = "INSERT INTO secretaria (usuarioId, turno) VALUES (?, ?)"
            cursor.execute(query_s, (self.id, self.turno))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
