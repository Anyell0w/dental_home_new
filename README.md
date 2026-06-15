
---

# Dental Home - Sistema de Gestión de Pacientes y Citas Dentales

¡Bienvenido al repositorio oficial de **Dental Home**! Este es un sistema de software de escritorio diseñado con el objetivo de centralizar la administración de historias clínicas, control de agendas de citas médicas, emisión de recetas farmacológicas en formato PDF y la auditoría interna del consultorio.

El sistema funciona de forma local en su totalidad y no requiere de ninguna conexión a internet para operar.

## 👥 Equipo de Desarrollo y Autores

Este proyecto es diseñado y mantenido de manera colaborativa por:

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

Para garantizar una implementación ágil y ligera dentro de las estaciones de trabajo de la red local, el entorno utiliza:

* 
**Lenguaje de Programación:** Python 3.11+ 


* **Motor de Base de Datos:** SQLite 3 (Integridad referencial estricta por hardware mediante `PRAGMA foreign_keys = ON;`).
* **Interfaz Gráfica (UI):** Tkinter y variantes estilizadas de `ttk` (Diseño limpio, minimalista y corporativo basado en la paleta cromática de aplicaciones profesionales de Microsoft).

---

## 📂 Arquitectura Estructural del Proyecto (MVC)

El código fuente del sistema está organizado bajo el patrón arquitectónico **Modelo-Vista-Controlador (MVC)**, asegurando que las modificaciones visuales nunca afecten la persistencia de los datos ni las reglas de validación interna:

```text
dental_home/
│
├── main.py                 # Punto de entrada de la aplicación y orquestador del ciclo de vida general.
├── config.py               # Constantes del sistema, rutas físicas de archivos y paleta de colores.
│
├── database/               # CAPA DE PERSISTENCIA DE DATOS
│   ├── connection.py       # Administrador de la conexión SQLite y sembrado de usuarios iniciales.
│   ├── schema.sql          # Script DDL normalizado en 3FN que define la base de datos relacional.
│   └── dental_home.db      # Archivo físico local de base de datos (se autogenera automáticamente).
│
├── models/                 # CAPA DE MODELOS (Entidades POO y Abstracción del Almacenamiento)
│   ├── __init__.py         # Inicializador y exportador unificado del paquete de modelos.
│   ├── usuario.py          # Clases base y subclases: Usuario, Doctor y Secretaria (Herencia 3FN).
│   ├── paciente.py         # Clases vinculadas por ciclo de vida: Paciente e HistorialClinico.
│   ├── cita.py             # Clases operacionales: Cita, RegistroClinico, Receta y Medicamento.
│   └── administracion.py   # Clases de soporte de infraestructura: CopiaSeguridad y Reporte.
│
├── controllers/            # CAPA DE CONTROLADORES (Lógica de Negocio y Validaciones)
│   ├── __init__.py         # Inicializador y exportador unificado del paquete de controladores.
│   ├── auth_controller.py  # Control de sesiones, roles jerárquicos y cifrado hash SHA-256.
│   ├── clinic_controller.py # Validación de agendas, cruces de horarios y control asistencial.
│   └── admin_controller.py  # Lógica de altas de personal y copias de seguridad de archivos binarios.
│
└── views/                  # CAPA DE VISTAS (Presentación Gráfica e Interfaces)
    ├── __init__.py         # Inicializador y exportador de los marcos de ventanas.
    ├── login_view.py       # Pantalla compacta de autenticación con logotipo vectorial nativo.
    ├── dashboard_view.py   # Shell adaptativo que monta pestañas según los permisos del rol.
    └── components/         # Módulos visuales independientes (Pestañas de la consola)
        ├── __init__.py     # Inicializador del paquete de componentes visuales.
        ├── pacientes_tab.py # Formulario de altas y tabla de búsqueda de pacientes por DNI.
        ├── citas_tab.py     # Consola de control de la agenda (Vistas temporales).
        ├── historias_tab.py # Panel de evolución clínica y generación de recetas (Uso del Doctor).
        └── admin_tab.py     # Panel de utilitarios de mantenimiento y backups del Administrador.

```

---

## 🗺️ Matriz de Mapeo: ¿Dónde programar cada Caso de Uso?

Para coordinar las tareas del equipo sin generar conflictos en los archivos de Git, localiza el **Caso de Uso (CU)** asignado en la siguiente tabla reglamentaria para identificar con precisión qué archivos debes modificar en cada capa de la arquitectura:

| ID | Nombre del Caso de Uso | Capa de Presentación (Vista) | Capa de Lógica (Controlador) | Capa de Datos (Modelo) |
| --- | --- | --- | --- | --- |
| **CU 1** | Ingreso y verificación de usuarios 

 | `views/login_view.py` | `controllers/auth_controller.py` | `models/usuario.py` |
| **CU 2** | Gestión y registro de pacientes 

 | `views/components/pacientes_tab.py` | `controllers/clinic_controller.py` | `models/paciente.py` |
| **CU 3** | El CRUD de las citas (Bloqueo de cruces) 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| **CU 4** | Ver historial de citas de un paciente 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| **CU 5** | Generar reportes de citas en PDF 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/administracion.py` |
| **CU 6** | Visualizar citas por día, semana o mes 

 | `views/components/citas_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| **CU 7** | Registrar Historial clínico 

 | `views/components/historias_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` *(RegistroClinico)* |
| **CU 8** | Mostrar recordatorio de cita programada (alerta) 

 | `views/dashboard_view.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| **CU 9** | Consultar citas pasadas de un paciente 

 | `views/components/historias_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` |
| **CU 10** | Registrar medicamentos y generar receta en PDF 

 | `views/components/historias_tab.py` | `controllers/clinic_controller.py` | `models/cita.py` *(Receta / Medicamento)* |
| **CU 11** | Exportar historial del paciente 

 | `views/components/historias_tab.py` | `controllers/admin_controller.py` | `models/administracion.py` |
| **CU 12** | Gestión de usuarios del sistema 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/usuario.py` |
| **CU 13** | Gestión de copias de seguridad 

 | `views/components/admin_tab.py` | `controllers/admin_controller.py` | `models/administracion.py` *(CopiaSeguridad)* |

---

## 🔑 Guía de Puesta en Marcha (Entorno Local)

### 1. Clonar el repositorio en tu estación de trabajo

```bash
git clone https://github.com/TU_ORGANIZACION/dental_home.git
cd dental_home

```

### 2. Arrancar la aplicación

Debido a que el motor SQLite 3 viene integrado en la biblioteca estándar de Python, no se requieren instalaciones complejas de bases de datos externas. Lanza el archivo raíz de forma directa:

```bash
python main.py

```

### 3. Cuentas de Prueba Precargadas (Base de datos local)

Al ejecutar el sistema por primera vez, el módulo de conexión creará automáticamente el archivo físico `dental_home.db` y sembrará tres perfiles operativos para realizar pruebas de visualización inmediata.

> ⚠️ **Importante:** La contraseña única de acceso configurada de fábrica para todas las cuentas es **`Admin123`** (respetando de forma estricta la letra inicial mayúscula).

* 
**Usuario Administrador:** `admin` (Acceso irrestricto a todos los módulos y utilitarios del sistema).


* 
**Usuario Odontólogo:** `doctor1` (Acceso exclusivo a la agenda de atención médica e historias clínicas).


* 
**Usuario Asistencia:** `secretaria1` (Acceso exclusivo al módulo operativo de altas de pacientes y agendamiento).



---

## 🎨 Directrices Estéticas para Nuevos Módulos (UI/UX Corporate)

Cualquier interfaz o elemento gráfico auxiliar que sea añadido por el equipo al proyecto debe cumplir obligatoriamente con los estándares declarados en `config.py`:

1. **Lienzo Limpio:** El fondo de los frames de contenido debe ser blanco sólido (`#FFFFFF`) con bordes sutiles en gris suave (`#E1DFDD`).
2. **Acentos:** Los botones de confirmación o llamadas a la acción principal deben utilizar la variante azul celeste mate corporativa de Microsoft (`#106EBE`).
3. **Tipografías:** Se debe implementar la fuente tipográfica de Windows `Segoe UI` en tamaños proporcionales (18pt para títulos de pestañas, 10pt para entradas de datos y 9pt en negrita para etiquetas de formulario).
