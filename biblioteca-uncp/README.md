# Biblioteca UNCP - Sistema de Gestión Bibliotecaria

## Descripción General
Sistema de gestión bibliotecaria universitaria para la Universidad Nacional del Centro del Perú (UNCP), desarrollado con Django 5.x.

## Tecnologías Utilizadas
- Python 3.12
- Django 5.1.6
- SQLite (desarrollo)
- Bootstrap 5 (frontend)
- HTML5, CSS3, JavaScript
- Django Templates, Forms, ModelForms
- Django Admin
- Middleware personalizado
- Autenticación y sesiones nativas de Django
- Git para control de versiones

## Estructura del Proyecto
```
biblioteca-uncp/
├── .venv/              # Entorno virtual
├── db.sqlite3          # Base de datos
├── manage.py           # Punto de entrada Django
├── biblioteca_uncp/    # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── catalogo/           # Aplicación de catálogo
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── management/     # Comandos personalizados
│   │   └── commands/
│   │       └── poblar_datos.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   └── static/
├── capturas/           # Evidencias de la práctica
│   ├── 01_configuracion/
│   ├── 02_formularios/
│   ├── 03_validaciones/
│   ├── 04_django_admin/
│   ├── 05_middleware_sesiones/
│   ├── 06_autenticacion_permisos/
│   ├── 07_postman/
│   ├── 08_pruebas_finales/
│   └── INDICE_EVIDENCIAS.md
├── docs/               # Documentación técnica
│   ├── ARQUITECTURA.md
│   ├── GUIA_EJECUCION.md
│   ├── PRUEBAS.md
│   ├── USO_IA.md
│   └── CUMPLIMIENTO_SEMANA_12.md
└── requirements.txt
```

## Modelos Principales
- `Categoria`: Categorías de libros (Literatura, Ciencias, Historia, etc.)
- `Libro`: Libros del catálogo con título, autor, ISBN, categoría, disponibilidad
- `Prestamo`: Registro de préstamos con fechas y estado de devolución
- `PerfilUsuario`: Perfiles extendidos con roles (estudiante, bibliotecario, administrador)

## Usuarios y Roles
- **Estudiante**: Puede consultar catálogo, solicitar préstamos, ver sus préstamos
- **Bibliotecario**: Puede registrar libros, actualizar información, administrar préstamos
- **Administrador**: Acceso total, Django Admin, gestión de usuarios

## Usuarios de Prueba
Se han creado usuarios de demostración tras ejecutar `python manage.py poblar_datos`:
- `estudiante1` / `estudiante1@uncp.edu.pe` (password: 12345) - Rol: Estudiante
- `estudiante2` / `estudiante2@uncp.edu.pe` (password: 12345) - Rol: Estudiante
- `bibliotecario1` / `bibliotecario1@uncp.edu.pe` (password: 12345) - Rol: Bibliotecario
- `admin1` / `admin1@uncp.edu.pe` (password: 12345) - Rol: Administrador

## Comandos Disponibles
- `python manage.py runserver`: Iniciar servidor de desarrollo
- `python manage.py poblar_datos`: Poblar base de datos con datos de demostración
- `python manage.py check`: Verificar configuración del sistema
- `python manage.py test`: Ejecutar pruebas automatizadas

## Capturas de Pantalla
Todas las evidencias se encuentran en la carpeta `capturas/` organizada por fases:
- `01_configuracion/`: Configuración del proyecto
- `02_formularios/`: Formularios implementados
- `03_validaciones/`: Validaciones realizadas
- `04_django_admin/`: Panel administrativo
- `05_middleware_sesiones/`: Middleware y sesiones
- `06_autenticacion_permisos/`: Autenticación y permisos
- `07_postman/`: Colecciones Postman
- `08_pruebas_finales/`: Resultados de pruebas

## Documentación Adicional
- `docs/ARQUITECTURA.md`: Arquitectura del sistema
- `docs/GUIA_EJECUCION.md`: Guía de ejecución paso a paso
- `docs/PRUEBAS.md`: Resultados de pruebas
- `docs/USO_IA.md`: Registro de uso de IA
- `docs/CUMPLIMIENTO_SEMANA_12.md`: Tabla de cumplimiento de fases