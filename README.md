# Dental Home - Sistema de Gestión de Pacientes y Citas Dentales

¡Bienvenido al repositorio oficial de **Dental Home**! Este es un sistema de escritorio diseñado específicamente para centralizar la administración de pacientes, control de agendas clínicas, emisión de recetas y auditorías operacionales de un consultorio dental.

El software opera de forma puramente local en una Red de Área Local (LAN), eliminando dependencias de conexiones externas a internet.

## 👥 Equipo de Desarrollo y Autores

Este proyecto es desarrollado de manera colaborativa por:

* 
**Lizbeth Estefany Caceres Tacora** 


* 
**Tania Karin Butron Maquera** 


* 
**Ronaldo Carlos Mamamani Mena** 


* 
**Angello Marcelo Zamora Valencia** 



---

## 🛠️ Tecnologías y Requisitos del Entorno

Para mantener una infraestructura ligera, rápida y portable para despliegues locales, se utiliza el siguiente stack técnico:

* 
**Lenguaje Base:** Python 3.11+ 


* **Motor de Persistencia:** SQLite 3 (Configurado con integridad referencial estricta `PRAGMA foreign_keys = ON;`)
* **Interfaz Gráfica (UI):** Tkinter & Ttk (Estilizado bajo una línea estética minimalista, limpia y corporativa basada en entornos profesionales de Microsoft).

---

## 📂 Mapa Completo de la Estructura del Proyecto

Para mantener una separación absoluta de responsabilidades, el proyecto implementa una arquitectura **MVC (Modelo-Vista-Controlador)** pura y **Programación Orientada a Objetos (POO)**. Aquí se detalla la ubicación exacta de cada archivo:

```text
dental_home/
│
├── main.py                 # Orquestador del ciclo de vida y punto de entrada de la aplicación.
├── config.py               # Centralización de estilos visuales, colores Microsoft y constantes de rutas.
│
├── database/               # CAPA DE ALMACENAMIENTO DE DATOS (Persistencia Local)
│   ├── connection.py       # Gestor de conexiones a SQLite y sembrado automático de datos de prueba.
│   ├── schema.sql          # Script DDL normalizado en 3FN que define la estructura relacional de las tablas.
│   └── dental_home.db      # Archivo físico binario que contiene la base de datos (se autogenera al iniciar).
│
├── models/                 # CAPA DE MODELOS (Entidades de Negocio y Abstracción de Datos)
│   ├── __init__.py         # Exportador unificado de las entidades del paquete.
│   ├── usuario.py          # Clases: Usuario, Doctor y Secretaria (Herencia de tabla por clase).
│   ├── paciente.py         # Clases: Paciente e HistorialClinico (Relación de composición).
│   ├── cita.py             # Clases: Cita, RegistroClinico, Receta y Medicamento.
│   └── administracion.py   # Clases: CopiaSeguridad y Reporte.
│
├── controllers/            # CAPA DE CONTROLADORES (Orquestación y Reglas de Validación)
│   ├── __init__.py         # Exportador unificado de los controladores del paquete.
│   ├── auth_controller.py  # Manejo de sesiones seguras, hashes SHA-256 e identificación de roles.
│   ├── clinic_controller.py # Control operacional de pacientes, agendas, cruces de horarios e historias.
│   └── admin_controller.py  # Funciones del sistema: creación de personal y copias de seguridad físicas.
│
└── views/                  # CAPA DE VISTAS (Presentación Gráfica y UI Corporativa)
    ├── __init__.py         # Exportador unificado del módulo de vistas.
    ├── login_view.py       # Ventana compacta de acceso restringido con isotipo vectorial integrado.
    ├── dashboard_view.py   # Shell principal adaptativo que monta las pestañas según el rol jerárquico.
    └── components/         # Módulos gráficos independientes para evitar archivos densos
        ├── __init__.py     # Exportador del paquete de componentes visuales.
        ├── pacientes_tab.py # UI para altas y búsquedas avanzadas de pacientes por DNI.
        ├── citas_tab.py     # Panel de visualización de la agenda por día, semana o mes.
        ├── historias_tab.py # Consola clínica exclusiva para Odontólogos para registrar evoluciones.
        └── admin_tab.py     # Panel administrativo para copias de seguridad e infraestructura de datos.

```

---

## 🗺️ ¿Dónde programar cada Caso de Uso?

Para facilitar la colaboración y evitar conflictos de fusión (*merge conflicts*) en Git, consulta la siguiente tabla de referencia antes de modificar el código asociado a un requerimiento o Caso de Uso específico:

| Caso de Uso / Requerimiento | Capa Vista (UI) | Capa Controlador | Capa Modelo |
| --- | --- | --- | --- |
| <br>**CU 1: Ingreso y verificación de usuarios** 

 | `views/login_view.py` | `controllers/auth_controller.py` | `models/usuario.py` |
| <br>**CU 2: Gestión y registro de pacientes** 

 | `views/components/pacientes_tab.py` | `controllers/clinic_controller.py` | `models/paciente.py` |
| <br>**CU 3: CRUD de las citas (Cruce de horarios)** 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| <br>**CU 4: Ver historial de citas de un paciente** 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| <br>**CU 5: Generar reportes en PDF** 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/administracion.py` |
| <br>**CU 6: Visualizar citas por día, semana o mes** 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| <br>**CU 7: Registrar Historial Clínico** 

 | `views/components/historias_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` *(RegistroClinico)* |
| <br>**CU 10: Registrar medicamentos y receta** 

 | `views/components/historias_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` *(Receta / Med)* |
| <br>**CU 12: Gestión de usuarios de sistema** 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/usuario.py` |
| <br>**CU 13: Copias de seguridad (Manual/Auto)** 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/administracion.py` |

---

## 🔑 Guía Rápida para Colaboradores

### 1. Clonar el repositorio localmente

```bash
git clone https://github.com/TU_ORGANIZACION/dental_home.git
cd dental_home

```

### 2. Instalar el driver de conexión de datos

SQLite viene preinstalado en el núcleo de Python, pero asegúrate de tener actualizado el entorno gráfico básico ejecutando:

```bash
pip install mysql-connector-python  # (Opcional, en caso de pruebas de migración cruzada externas)

```

### 3. Ejecutar la aplicación

Para iniciar el entorno gráfico, ejecuta directamente el archivo raíz:

```bash
python main.py

```

### 4. Cuentas de Acceso precargadas para pruebas en el entorno local

Al arrancar la aplicación por primera vez, el módulo `database/connection.py` creará el archivo físico de base de datos e inyectará los siguientes perfiles de prueba automáticos:

> ⚠️ **Nota de Seguridad:** Todas las contraseñas están almacenadas localmente usando hashes criptográficos robustos basados en el algoritmo SHA-256. La contraseña para todos los usuarios de prueba es **`Admin123`** (respetando la mayúscula inicial).

* **Perfil Administrador:** `admin` (Acceso completo a todos los componentes e infraestructura del sistema).
* **Perfil Odontólogo:** `doctor1` (Acceso restringido a la agenda médica y escritura de historias clínicas).
* **Perfil Asistencia:** `secretaria1` (Acceso enfocado a alta de pacientes y agendamientos de turnos).

---

## 🎨 Lineamientos de Diseño (UI/UX de Código Limpio)

Si vas a colaborar creando nuevos campos o ventanas para el sistema, debes seguir de forma estricta las directrices estéticas declaradas en `config.py`:

1. **Lienzo Dominante:** Todo contenedor de formulario o tarjetas de datos debe poseer un color de fondo blanco puro (`#FFFFFF`) para asegurar contraste.
2. **Acentos:** Los botones interactivos de acción positiva deben utilizar el color celeste mate corporativo de Microsoft (`#106EBE`).
3. **Tipografía:** Utiliza la familia de fuentes `Segoe UI` para todos los textos de la interfaz, asegurando la legibilidad del sistema de escritorio en entornos Windows.
