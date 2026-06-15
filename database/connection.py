import os
import sqlite3
import hashlib
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_name="dental_home.db", schema_name="schema.sql"):
        # Determinar las rutas absolutas dentro del entorno local
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, db_name)
        self.schema_path = os.path.join(self.base_dir, schema_name)
        
        # Inicializar la base de datos si no existe físicamente
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            self._inicializar_base_de_datos()

    def get_connection(self):
        """Retorna una conexión activa con soporte de llaves foráneas y mapeo por diccionario."""
        conn = sqlite3.connect(self.db_path)
        # Habilitar explícitamente las restricciones de clave foránea en SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        # Configurar las filas para que se comporten como diccionarios (scannability de atributos)
        conn.row_factory = sqlite3.Row
        return conn

    def _inicializar_base_de_datos(self):
        """Crea las tablas a partir del archivo schema.sql e inserta los usuarios base."""
        print("[Database] Inicializando base de datos local por primera vez...")
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"No se encontró el archivo de estructura DDL en: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_ddl = f.read()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Ejecutar el script DDL completo
            cursor.executescript(schema_ddl)
            conn.commit()
            print("[Database] Estructura de tablas 3FN creada exitosamente.")
            
            # Sembrado de usuarios iniciales de prueba (Contraseña por defecto: Admin123)
            # Las contraseñas nunca deben guardarse en texto plano bajo ninguna circunstancia 
            password_hash = hashlib.sha256("Admin123".encode()).hexdigest()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 1. Crear Administrador
            cursor.execute(
                "INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion) VALUES (?, ?, ?, ?, ?)",
                ("admin", password_hash, "Administrador", 1, fecha_actual)
            )
            
            # 2. Crear Doctor y su registro extendido
            cursor.execute(
                "INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion) VALUES (?, ?, ?, ?, ?)",
                ("doctor1", password_hash, "Doctor", 1, fecha_actual)
            )
            id_doctor = cursor.lastrowid
            cursor.execute(
                "INSERT INTO doctor (usuarioId, numeroColegiatura) VALUES (?, ?)",
                (id_doctor, "COP-98765")
            )

            # 3. Crear Secretaria y su registro extendido
            cursor.execute(
                "INSERT INTO usuario (nombreUsuario, contraseña, rol, activo, fechaCreacion) VALUES (?, ?, ?, ?, ?)",
                ("secretaria1", password_hash, "Secretaria", 1, fecha_actual)
            )
            id_secretaria = cursor.lastrowid
            cursor.execute(
                "INSERT INTO secretaria (usuarioId, turno) VALUES (?, ?)",
                (id_secretaria, "Mañana")
            )

            conn.commit()
            print("[Database] Usuarios iniciales sembrados correctamente (admin, doctor1, secretaria1).")
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"[Database] Error crítico durante la inicialización: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()
