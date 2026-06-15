-- ===========================================================================
-- DENTAL HOME - DISEÑO DE BASE DE DATOS (SQLite)
-- NORMALIZACIÓN: 3FN
-- ===========================================================================

-- Forzar la validación de claves foráneas en cada sesión
PRAGMA foreign_keys = ON;

-- TABLA: Usuario (Clase Padre)
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreUsuario TEXT NOT NULL UNIQUE,
    contraseña TEXT NOT NULL, -- Almacenará hashes SHA-256 
    rol TEXT NOT NULL CHECK(rol IN ('Administrador', 'Doctor', 'Secretaria')),
    activo INTEGER NOT NULL CHECK(activo IN (0, 1)),
    fechaCreacion TEXT NOT NULL
);

-- TABLA: Doctor (Subclase de Usuario)
CREATE TABLE IF NOT EXISTS doctor (
    usuarioId INTEGER PRIMARY KEY,
    numeroColegiatura TEXT NOT NULL UNIQUE,
    FOREIGN KEY (usuarioId) REFERENCES usuario(id) ON DELETE CASCADE
);

-- TABLA: Secretaria (Subclase de Usuario)
CREATE TABLE IF NOT EXISTS secretaria (
    usuarioId INTEGER PRIMARY KEY,
    turno TEXT NOT NULL,
    FOREIGN KEY (usuarioId) REFERENCES usuario(id) ON DELETE CASCADE
);

-- TABLA: Paciente
CREATE TABLE IF NOT EXISTS paciente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    telefono TEXT,
    sexo TEXT,
    fechaNacimiento TEXT,
    direccion TEXT,
    estado INTEGER NOT NULL CHECK(estado IN (0, 1)),
    registradoPor INTEGER,
    FOREIGN KEY (registradoPor) REFERENCES usuario(id) ON DELETE SET NULL
);

-- TABLA: HistorialClinico (Composición 1:1 con Paciente)
CREATE TABLE IF NOT EXISTS historial_clinico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pacienteId INTEGER NOT NULL UNIQUE,
    fechaCreacion TEXT NOT NULL,
    observaciones TEXT,
    activo INTEGER NOT NULL CHECK(activo IN (0, 1)),
    FOREIGN KEY (pacienteId) REFERENCES paciente(id) ON DELETE CASCADE
);

-- TABLA: Cita
CREATE TABLE IF NOT EXISTS cita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pacienteId INTEGER NOT NULL,
    doctorId INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    estado TEXT NOT NULL,
    motivoCancelacion TEXT,
    fechaRegistro TEXT NOT NULL,
    FOREIGN KEY (pacienteId) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (doctorId) REFERENCES doctor(usuarioId) ON DELETE CASCADE
);

-- TABLA: RegistroClinico
CREATE TABLE IF NOT EXISTS registro_clinico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    historialId INTEGER NOT NULL,
    citaId INTEGER UNIQUE,
    doctorId INTEGER NOT NULL,
    diagnostico TEXT NOT NULL,
    tratamiento TEXT NOT NULL,
    observaciones TEXT,
    fechaConsulta TEXT NOT NULL,
    FOREIGN KEY (historialId) REFERENCES historial_clinico(id) ON DELETE CASCADE,
    FOREIGN KEY (citaId) REFERENCES cita(id) ON DELETE SET NULL,
    FOREIGN KEY (doctorId) REFERENCES doctor(usuarioId) ON DELETE CASCADE
);

-- TABLA: Receta
CREATE TABLE IF NOT EXISTS receta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registroClinicoId INTEGER NOT NULL UNIQUE,
    pacienteId INTEGER NOT NULL,
    doctorId INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    indicacionesGenerales TEXT,
    archivoPDF TEXT,
    FOREIGN KEY (registroClinicoId) REFERENCES registro_clinico(id) ON DELETE CASCADE,
    FOREIGN KEY (pacienteId) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (doctorId) REFERENCES doctor(usuarioId) ON DELETE CASCADE
);

-- TABLA: Medicamento (Composición con Receta)
CREATE TABLE IF NOT EXISTS medicamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recetaId INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    cantidad TEXT NOT NULL,
    indicaciones TEXT,
    FOREIGN KEY (recetaId) REFERENCES receta(id) ON DELETE CASCADE
);

-- TABLA: CopiaSeguridad
CREATE TABLE IF NOT EXISTS copia_seguridad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fechaHora TEXT NOT NULL,
    tipo TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    tamaño TEXT NOT NULL,
    generadoPor TEXT NOT NULL
);

-- TABLA: Reporte
CREATE TABLE IF NOT EXISTS reporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generadoPor INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    fechaInicio TEXT,
    fechaFin TEXT,
    formato TEXT NOT NULL,
    fechaGeneracion TEXT NOT NULL,
    archivo TEXT NOT NULL,
    FOREIGN KEY (generadoPor) REFERENCES usuario(id) ON DELETE CASCADE
);
