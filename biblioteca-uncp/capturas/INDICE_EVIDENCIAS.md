# Biblioteca UNCP - Práctica Semana 12
## Índice de Evidencias

### Configuración del Proyecto
- [ ] 01_Configuracion_Entorno_Virtual: Estructura de `.venv` y `requirements.txt`
- [ ] 01_Configuracion_Proyecto: Proyecto Django iniciado con estructura correcta
- [ ] 01_Configuracion_Migraciones: Migraciones aplicadas exitosamente (`python manage.py migrate`)

### Formularios
- [ ] 02_Formularios_Registro: Formulario de registro de usuarios con validación
- [ ] 02_Formularios_Login: Formulario de inicio de sesión
- [ ] 02_Formularios_ModelForm: `LibroModelForm` y `PrestamoModelForm`
- [ ] 02_Formularios_Busqueda: `BusquedaLibrosForm` para catálogo

### Validaciones
- [ ] 03_Validaciones_Formularios: Validación personalizada en `clean_<campo>()` y `clean()`
- [ ] 03_Validaciones_ISBN: Validación de ISBN único y checksum ISBN-13
- [ ] 03_Validaciones_Fechas: Validación de fechas de devolución
- [ ] 03_Validaciones_Cruzada: Validación cruzada de préstamos duplicados
- [ ] 03_Validaciones_Modelo: Validaciones a nivel de modelo (ISBN, cantidades)

### Django Admin
- [ ] 04_Admin_Categorias: Configuración de `list_display`, `list_filter`, `search_fields`
- [ ] 04_Admin_Libros: Configuración completa de `LibroAdmin` con acciones masivas
- [ ] 04_Admin_Prestamos: Configuración de `PrestamoAdmin` con acciones de devolución
- [ ] 04_Admin_Perfiles: Configuración de `PerfilUsuarioAdmin`

### Middleware y Sesiones
- [ ] 05_Middleware_Sesiones: Middleware personalizado con registro de solicitudes
- [ ] 05_Middleware_Logs: Logs con método HTTP, ruta, estado y duración
- [ ] 05_Sesiones_Cookies: Configuración de cookies de sesión seguras

### Autenticación y Permisos
- [ ] 06_Autenticacion_Registro: Flujo de registro de nuevos usuarios
- [ ] 06_Autenticacion_Login: Flujo de inicio de sesión con `authenticate()` y `login()`
- [ ] 06_Autenticacion_Roles: Roles de Estudiante, Bibliotecario y Administrador
- [ ] 06_Autenticacion_Permisos: `@login_required`, `PermissionRequiredMixin`, grupos
- [ ] 06_Autenticacion_CSRF: Protección CSRF en formularios y pruebas

### Postman
- [ ] 07_Postman_Collection: `Biblioteca_UNCP.postman_collection.json`
- [ ] 07_Postman_Environment: `Biblioteca_UNCP_Local.postman_environment.json`
- [ ] 07_Postman_Readme: `README_POSTMAN.md` con descripción de endpoints
- [ ] 07_Postman_Pruebas: Tests con Newman verificando status codes y estructura

### Pruebas Finales
- [ ] 08_Pruebas_Tests: Tests automatizados con `python manage.py test`
- [ ] 08_Pruebas_Check: `python manage.py check` y `python manage.py check --deploy`
- [ ] 08_Pruebas_Servidor: Servidor Django funcionando en `localhost:8000`

### Pruebas Finales Globales
- [ ] Capturas de: Estructura del proyecto, servidor funcionando, página de inicio
- [ ] Capturas de: Catálogo de libros, formulario de registro
- [ ] Capturas de: Errores de validación, panel Django Admin
- [ ] Capturas de: Sesiones y cookies, restricciones de acceso
- [ ] Capturas de: Pruebas Postman, resultados de tests
- [ ] Resultados de: `manage.py check`

---

**Fecha de generación:** 18 de noviembre de 2026  
**Autor:** Fabio Coder  
**Estado:** En desarrollo - Fase 12: Pruebas y Documentación