# 🦷 Consultorio Odontológico "Saca Muela"
> **Sistema de digitalización de pacientes y seguimiento clínico local.**  
> Una solución de escritorio ágil, segura y diseñada a medida para la transición eficiente de registros físicos a formato digital.

---

## 🎯 Propósito del Proyecto
El sistema tiene como objetivo principal optimizar la gestión de pacientes y la evolución de sus historias clínicas dentro de la clínica **"Saca Muela"**. Reemplaza el uso tradicional de fichas de papel por una interfaz de escritorio intuitiva y rápida, asegurando que el almacenamiento de datos sea local, privado e inalterable bajo las normativas legales de salud vigentes.

---

## 🛠️ Características y Funcionalidades Clave

El sistema se divide en tres módulos esenciales de fácil acceso desde una terminal única:

### 👤 1. Registro y Gestión de Pacientes (CRUD)
* **Altas con validación inteligente:** Registro completo de datos personales (filiación, obra social, contactos de emergencia y antecedentes médicos).
* **Búsqueda e indexación rápida:** Filtrado instantáneo por nombre, apellido o DNI desde la pantalla principal.
* **Control de estado (Baja Lógica):** Cumpliendo con la consistencia de datos, los pacientes nunca se eliminan físicamente; se desactivan para mantener su historial clínico a salvo.

### 📝 2. Evolución de Historias Clínicas
* **Historial cronológico:** Registro detallado de diagnósticos, consultas y tratamientos odontológicos por paciente.
* **Seguridad legal (Anulación lógica):** En cumplimiento con normativas de salud, las anotaciones médicas no se pueden editar ni borrar una vez guardadas. Si ocurre un error, la entrada se "anula" visualmente manteniendo el registro original intacto para auditoría.

### 🛡️ 3. Auditoría e Integridad Local
* **Trazabilidad total:** Cada alta, modificación o anulación genera automáticamente un registro de log inalterable con marcas temporales precisas.
* **Persistencia robusta:** Utiliza una base de datos local SQLite con transacciones protegidas ante cortes de energía imprevistos.

---

## 📋 Alcance del Sistema

Para mantener un software enfocado, robusto y eficiente para la terminal de trabajo de la clínica, el alcance se delimita estrictamente de la siguiente manera:

### ✅ Qué incluye (Dentro del alcance)
* Gestión integral de perfiles de pacientes y estados de afiliación.
* Evolución histórica e inalterable de consultas odontológicas.
* Base de datos local segura con cero dependencias en la nube.
* Registro automático de logs para auditoría interna.
* Copias de seguridad locales y exportación de datos con un clic.

### ❌ Qué NO incluye (Fuera del alcance)
* **Gestión de Agenda:** No gestiona turnos ni calendarios (se registran las atenciones cuando ocurren).
* **Control Financiero:** No incluye facturación, cobros ni liquidaciones de obras sociales.
* **Inventario:** No administra stock de insumos clínicos.
* **Acceso Multiusuario:** No requiere inicio de sesión con roles; la seguridad de acceso se delega directamente al sistema operativo de la computadora de escritorio.

---

## 💻 Arquitectura y Stack Tecnológico

El software está desarrollado bajo un paradigma monolítico de escritorio ligero y de alta portabilidad:

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter (GUI nativa, optimizada para pantallas estándar a partir de 1366x768 px).
* **Base de Datos:** SQLite3 (Persistencia local en un único archivo de base de datos transaccional con modo *Write-Ahead Logging*).
* **Distribución:** Compatible con entornos Windows y Linux de manera nativa.

---

## 🚀 Guía de Inicio Rápido (Desarrollo)

### Requisitos Previos
* Tener instalado **Python 3.8** o superior en el sistema.

### Instalación y Ejecución
1. Clona este repositorio o descarga el código fuente:
   ```bash
   git clone https://github.com/tu-usuario/saca-muela-app.git
   cd saca-muela-app
   ```
2. Ejecuta el archivo principal de la aplicación:
   ```bash
   python main.py
   ```
*Nota: Al ejecutarse por primera vez, el sistema creará automáticamente la base de datos local y las tablas necesarias en el directorio de la aplicación.*
