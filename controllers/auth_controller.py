# controllers/auth_controller.py
import hashlib
from datetime import datetime

class AuthController:
    def __init__(self, db_connection):
        self.db = db_connection
        self.usuario_actual = None

    def iniciar_sesion(self, nombre_usuario, contrasena):
        """
        Valida las credenciales del usuario contra la base de datos local[cite: 12].
        Aplica hash seguro SHA-256 para proteger datos sensibles[cite: 148].
        """
        # Validación de campos obligatorios vacíos [cite: 11]
        if not nombre_usuario.strip() or not contrasena.strip():
            return False, "El nombre de usuario y la contraseña no pueden estar vacíos." [cite: 11]

        # Convertir la contraseña ingresada a su representación hash SHA-256 [cite: 148]
        contrasena_hash = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Consulta relacional 3FN uniendo la tabla base con sus subclases específicas
            query = """
                SELECT u.id, u.nombreUsuario, u.rol, u.activo,
                       d.numeroColegiatura, s.turno
                FROM usuario u
                LEFT JOIN doctor d ON u.id = d.usuarioId
                LEFT JOIN secretaria s ON u.id = s.usuarioId
                WHERE u.nombreUsuario = ? AND u.contraseña = ? AND u.activo = 1
            """
            cursor.execute(query, (nombre_usuario.strip(), contrasena_hash))
            row = cursor.fetchone()

            if row:
                # Mapear el registro a un diccionario legible para la sesión activa [cite: 14]
                self.usuario_actual = {
                    "id": row["id"],
                    "nombreUsuario": row["nombreUsuario"],
                    "rol": row["rol"], # Identificación estricta del rol asignado [cite: 14]
                    "detalles": {
                        "numeroColegiatura": row["numeroColegiatura"] if row["rol"] == "Doctor" else None,
                        "turno": row["turno"] if row["rol"] == "Secretaria" else None
                    }
                }
                return True, self.usuario_actual
            else:
                return False, "Nombre de usuario o contraseña incorrectos, o cuenta inactiva."
                
        except Exception as e:
            return False, f"Error de infraestructura de red local: {str(e)}"
        finally:
            conn.close()

    def cerrar_sesion(self):
        """Limpia el estado de la sesión actual del sistema."""
        self.usuario_actual = None
        return True
