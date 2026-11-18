# Documento de Arquitectura - Biblioteca UNCP

## Resumen General
Sistema de gestión bibliotecaria desarrollado con Django 5.x siguiendo el patrón MTV (Model-Template-View).

## Arquitectura de Capas

### 1. Capa de Presentación (Frontend)
- **Templates Django**: Plantillas HTML5 con Bootstrap 5
- **CSS Personalizado**: Estilos con colores institucionales UNCP (#164B35, #287A52, #D6AC53)
- **JavaScript**: Interacciones básicas, manejo de modales, validaciones en tiempo real
- **Responsive Design**: La interfaz se adapta a dispositivos móviles y desktop

### 2. Capa de Lógica (Django Views)
- **Vistas Funcionales**: Vistas que manejan la lógica de negocio
- **Vistas por Rol**: Acceso restringido según perfil de usuario (estudiante, bibliotecario, administrador)
- **APIs Ligadas**: Endpoints JSON para integración con Postman y frontend

### 3. Capa de Datos (Models)
- **Modelos Django**: ORM sobre SQLite para desarrollo
- **Modelos Principales**:
  - `Categoria`: Clasificación de libros
  - `Libro`: Recursos bibliográficos
  - `Prestamo`: Historial de préstamos y devoluciones
  - `PerfilUsuario`: Extensión del User model de Django
- **Relaciones**: ForeignKey, OneToOneField, con validaciones integradas

### 4. Capa de Configuración
- **Settings**: Configuración centralizada (middleware, apps, seguridad)
- **URLs**: Enrutamiento con namespace `catalogo`
- **Admin**: Panel personalizado con acciones masivas y filtros
- **Middleware**: Personalizado para logging de solicitudes

## Flujo de Datos

1. **Solicitud HTTP** → Middleware registra petición
2. **Verificación de Autenticación** → `@login_required` o `PermissionRequiredMixin`
3. **Procesamiento de Formulario** → `forms.Form` o `forms.ModelForm` con `clean_*()` methods
4. **Validación y Sanitización** → `ValidationError`, `self.add_error()`, `strip()`
5. **Guardado en Base de Datos** → `model.save()` con validaciones a nivel de campo
6. **Respuesta** → Redirección, JSON o renderizado de template

## Seguridad Implementada
- CSRF Protection (middleware django.middleware.csrf.CsrfViewMiddleware)
- Authentication nativa de Django (`authenticate()`, `login()`)
- Permisos por rol (Grupos: Estudiante, Bibliotecario)
- `@login_required` en vistas protegidas
- `PermissionRequiredMixin` para accesos específicos
- Validación de entradas (no escape() indiscriminado)
- Headers de seguridad por defecto de Django

## Despliegue
- **Desarrollo**: HTTP con DEBUG=True
- **Producción**: HTTPS con configuraciones de seguridad (SECRET_KEY fuerte, ALLOWED_HOSTS, HSTS, SSL_REDIRECT)
- Advertencias identificadas por `python manage.py check --deploy` documentadas en `docs/PRUEBAS.md`