# controllers/admin_controller.py
import os
import shutil
from datetime import datetime

class AdminController:
    def __init__(self, db_connection, auth_controller):
        self.db = db_connection
        self.auth = auth_controller

    # =========================================================================
    # SECCIÓN: GESTIÓN DE USUARIOS [cite: 118]
    # =========================================================================
    def registrar_usuario_sistema(self, nombre_usuario, contrasena_plana, rol, dato_extendido):
        """
        Crea un nuevo usuario del sistema aplicando herencia de tabla por clase (3FN)[cite: 125, 127].
        Asegura que las contraseñas pasen cifradas por SHA-256[cite: 148].
        """
        if not nombre_usuario.strip() or not contrasena_plana.strip() or not rol:
            return False, "Todos los campos de la ficha de usuario son obligatorios." 

        import hashlib
        contrasena_hash = hashlib.sha256(contrasena_plana.encode('utf-8')).hexdigest()
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            conn.execute("BEGIN TRANSACTION;")

            # 1. Insertar en tabla base Usuario [cite: 127]
            query_usuario = """
                INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion)
                VALUES (?, ?, ?, 1, ?)
            """
            cursor.execute(query_usuario, (nombre_usuario.strip(), contrasena_hash, rol, fecha_creacion))
            nuevo_id = cursor.lastrowid

            # 2. Insertar en subclase correspondiente según patrón estructural de herencia
            if rol == "Doctor":
                if not dato_extendido.strip():
                    raise Exception("El número de colegiatura médica es requerido obligatoriamente para Doctores.")
                cursor.execute("INSERT INTO doctor (usuarioId, numeroColegiatura) VALUES (?, ?)", (nuevo_id, dato_extendido.strip()))
            elif rol == "Secretaria":
                if not dato_extendido.strip():
                    raise Exception("La asignación del turno de trabajo es requerida para Secretarias.")
                cursor.execute("INSERT INTO secretaria (usuarioId, turno) VALUES (?, ?)", (nuevo_id, dato_extendido.strip()))

            conn.commit()
            return True, f"Usuario [{nombre_usuario}] registrado exitosamente bajo el rol de {rol}." 
        except Exception as e:
            conn.rollback()
            return False, f"Error al crear el usuario (el nombre podría ya existir): {str(e)}"
        finally:
            conn.close()

    # =========================================================================
    # SECCIÓN: RESPALDOS Y SEGURIDAD (BACKUPS LOCALES) [cite: 129]
    # =========================================================================
    def ejecutar_respaldo_manual(self, directorio_destino):
        """
        Realiza una copia binaria exacta del archivo físico .db actual en la ruta local elegida[cite: 137].
        Registra la metadata completa del evento en la tabla copia_seguridad[cite: 138].
        """
        if not os.path.exists(directorio_destino):
            return False, "La ruta destino especificada para el respaldo no es válida o no existe."

        origen = self.db.db_path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_dentalhome_{timestamp}.db"
        destino_completo = os.path.join(directorio_destino, nombre_archivo)

        try:
            # Duplicación física nativa de archivos para bases de datos SQLite locales
            shutil.copy2(origen, destino_completo)
            
            # Calcular tamaño legible del archivo generado
            bytes_size = os.path.getsize(destino_completo)
            size_str = f"{round(bytes_size / 1024, 2)} KB"
            fecha_hora_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Registrar la persistencia del control de respaldo
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO copia_seguridad (fechaHora, tipo, ubicacion, tamaño, generadoPor)
                VALUES (?, 'Manual', ?, ?, ?)
            """
            responsable = self.auth.usuario_actual["nombreUsuario"] if self.auth.usuario_actual else "Sistema"
            cursor.execute(query, (fecha_hora_log, destino_completo, size_str, responsable))
            conn.commit()
            conn.close()

            return True, f"Copia de seguridad realizada con éxito en:\n{destino_completo}" 
        except Exception as e:
            return False, f"Fallo crítico al compilar el respaldo local: {str(e)}"
