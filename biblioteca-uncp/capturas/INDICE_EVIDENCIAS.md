# Biblioteca UNCP - Práctica Semana 12
## Índice de Evidencias

### Configuración del Proyecto
- [x] 01_Configuracion_Entorno_Virtual: Estructura de `.venv` y `requirements.txt`
  - evidencia_01_estructura.txt - Estructura completa del proyecto
- [x] 01_Configuracion_Proyecto: Proyecto Django iniciado con estructura correcta
  - evidencia_01_estructura.txt - Archivos clave verificados
- [x] 01_Configuracion_Migraciones: Migraciones aplicadas exitosamente
  - python manage.py migrate - Sin issues

### Formularios
- [x] 02_Formularios_Registro: Formulario de registro de usuarios con validación
  - evidencia_02_formularios.txt - RegistroUsuarioForm, LibroModelForm, SolicitudPrestamoForm
- [x] 02_Formularios_Login: Formulario de inicio de sesión
  - evidencia_02_formularios.txt - Formularios auth nativo
- [x] 02_Formularios_ModelForm: `LibroModelForm` y `PrestamoModelForm`
  - evidencia_02_formularios.txt - ModelForm con validaciones personalizadas
- [x] 02_Formularios_Busqueda: `BusquedaLibrosForm` para catálogo
  - evidencia_02_formularios.txt - Formulario de búsqueda con filtros

### Validaciones
- [x] 03_Validaciones_Formularios: Validación personalizada en `clean_<campo>()` y `clean()`
  - evidencia_03_validaciones.txt - clean_isbn(), clean(), clean_username(), clean_email()
- [x] 03_Validaciones_ISBN: Validación de ISBN único y checksum ISBN-13
  - evidencia_03_validaciones.txt - Validación de checksum ISBN-13 en form
- [x] 03_Validaciones_Fechas: Validación de fechas de devolución
  - evidencia_03_validaciones.txt - Fechas de devolución inválidas
- [x] 03_Validaciones_Cruzada: Validación cruzada de préstamos duplicados
  - evidencia_03_validaciones.txt - Validación cruzada en PrestamoModelForm
- [x] 03_Validaciones_Modelo: Validaciones a nivel de modelo (ISBN, cantidades)
  - evidencia_03_validaciones.txt - Validaciones a nivel de modelo

### Django Admin
- [x] 04_Admin_Categorias: Configuración de `list_display`, `list_filter`, `search_fields`
  - evidencia_04_admin.txt - CategoriaAdmin configurado
- [x] 04_Admin_Libros: Configuración completa de `LibroAdmin` con acciones masivas
  - evidencia_04_admin.txt - LibroAdmin con acciones y filtros
- [x] 04_Admin_Prestamos: Configuración de `PrestamoAdmin` con acciones de devolución
  - evidencia_04_admin.txt - PrestamoAdmin con acciones masivas
- [x] 04_Admin_Perfiles: Configuración de `PerfilUsuarioAdmin`
  - evidencia_04_admin.txt - PerfilUsuarioAdmin con roles

### Middleware y Sesiones
- [x] 05_Middleware_Sesiones: Middleware personalizado con registro de solicitudes
  - evidencia_05_middleware.txt - Middleware con __init__ y __call__
- [x] 05_Logs_Cookies: Logs con método HTTP, ruta, estado y duración
  - evidencia_05_middleware.txt - Configuración de logging en settings
- [x] 05_Cookies_Seguras: Configuración de cookies de sesión seguras
  - evidencia_05_middleware.txt - Configuración de sesión y CSRF

### Autenticación y Permisos
- [x] 06_Autenticacion_Registro: Flujo de registro de nuevos usuarios
  - evidencia_06_autenticacion.txt - Registro con create_user y login
- [x] 06_Autenticacion_Login: Flujo de inicio de sesión con `authenticate()` y `login()`
  - evidencia_06_autenticacion.txt - Login con authenticate + login
- [x] 06_Autenticacion_Roles: Roles de Estudiante, Bibliotecario y Administrador
  - evidencia_06_autenticacion.txt - Tres roles con propiedades y colores
- [x] 06_Autenticacion_Permisos: `@login_required`, `PermissionRequiredMixin`, grupos
  - evidencia_06_autenticacion.txt - Decoradores y mixins implementados
- [x] 06_Autenticacion_CSRF: Protección CSRF en formularios y pruebas
  - evidencia_06_autenticacion.txt - CSRF token en formularios POST

### Postman
- [x] 07_Postman_Collection: `Biblioteca_UNCP.postman_collection.json`
  - evidencia_07_postman.txt - Colección con 12 endpoints
- [x] 07_Postman_Environment: `Biblioteca_UNCP_Local.postman_environment.json`
  - evidencia_07_postman.txt - Environment con variables de entorno
- [x] 07_Postman_Readme: `README_POSTMAN.md` con descripción de endpoints
  - evidencia_07_postman.txt - Documentación de endpoints

### Pruebas Finales
- [x] 08_Pruebas_Tests: Tests automatizados con `python manage.py test`
  - evidencia_08_pruebas.txt - 17/17 tests aprobados
- [x] 08_Pruebas_Check: `python manage.py check` y `python manage.py check --deploy`
  - evidencia_08_pruebas.txt - Check OK, check --deploy warnings documentados
- [x] 08_Resultados_Tests: Resultados de tests y evidencias
  - evidencia_08_pruebas.txt - Resumen ejecutivo de pruebas

### Evidencias Cruzadas
- [x] capturas/INDICE_EVIDENCIAS.md - Índice general con descripción de cada evidencia
  - INDICE_EVIDENCIAS.md - Índice actualizado con todas las secciones

---

**Fecha de generación:** 18 de noviembre de 2026  
**Autor:** Fabio Coder  
**Proyecto:** Biblioteca UNCP - Práctica Semana 12  
**Estado:** COMPLETADO - Todas las evidencias generadas y verificadas