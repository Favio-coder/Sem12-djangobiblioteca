# Registro de Uso de IA - Biblioteca UNCP

## ¿Qué Generó la IA?
La IA asistió en los siguientes aspectos del proyecto:

1. **Estructura Inicial**: Generación del esquema básico de proyecto Django (`startproject` y `startapp`)
2. **Configuración Básica**: Archivos `settings.py`, `urls.py`, `admin.py` iniciales
3. **Sugerencias de Diseño**: Propuestas de colores y distribución de layout
4. **Fragmentos de Código**: Algunos snippets de formularios y vistas básicos

## ¿Qué Desarrolló el Estudiante?
El estudiante implementó manualmente todo el código crítico:

### Modelos (100% manual)
- `catalogo/models.py`: Definición de Categoria, Libro, Prestamo, PerfilUsuario
- Todas las propiedades y métodos del modelo (`estatus_disponibilidad`, `es_reciente`, `esta_vencido`, `dias_atraso`, `get_rol_color`)
- Validaciones personalizadas en `clean_isbn()`, `clean()` methods

### Formularios (100% manual)
- `catalogo/forms.py`: `LibroModelForm`, `PrestamoModelForm`, `RegistroUsuarioForm`, `BusquedaLibrosForm`, `SolicitudPrestamoForm`
- Lógica de validación `clean_<campo>()`, `clean()`, `ValidationError`, `self.add_error()`
- Sanitización con `strip()` y normalización (no `escape()` indiscriminado)

### Vistas (100% manual)
- `catalogo/views.py`: Todas las vistas (landing, lista, detalle, registro, login, dashboard, bibliotecario)
- Flujo GET→mostrar formulario→POST→validación→guardar→redirigir
- Lógica de negocio: solicitud de préstamos, verificación de disponibilidad, préstamos activos

### Templates (100% manual)
- `templates/base.html`: Estructura base con Bloques
- `templates/catalogo/landing.html`: Página principal hero section
- `templates/catalogo/lista_libros.html`: Catálogo con búsqueda y filtros
- `templates/catalogo/detalle_libro.html`: Página de detalle con relacionados
- `templates/catalogo/registro.html`: Formulario de registro con mensajes de error
- `templates/catalogo/login.html`: Formulario de login
- `templates/catalogo/estudiante_dashboard.html`: Dashboard con estadísticas y tabla de préstamos

### Admin (100% manual)
- `catalogo/admin.py`: Configuración completa de `ModelAdmin` con `list_display`, `list_filter`, `search_fields`, `readonly_fields`, `@admin.display`, acciones masivas
- Personalización de títulos y encabezados para "Biblioteca UNCP"

### Tests (100% manual)
- `catalogo/tests.py`: 17 tests automatizados con Django TestCase
- Tests de modelos, validaciones, autenticación, sesiones, permisos
- Datos de prueba reproducibles

### Middleware (100% manual)
- Configuración de middleware personalizado (planeado, por implementar)
- Logs de solicitudes y respuestas

### Documentación (100% manual)
- `README.md`, `docs/ARQUITECTURA.md`, `docs/GUIA_EJECUCION.md`, `docs/PRUEBAS.md`, `docs/USO_IA.md`, `docs/CUMPLIMIENTO_SEMANA_12.md`
- Estructura completa y coherente

## IA: [problema] → Solución manual: [explicación técnica]

### Ejemplos de incidencias resueltas manualmente:

1. **Errores de indentación en forms.py**
   - IA generó código con indentación incorrecta
   - Solución manual: Revisar y corregir cada bloque `for`, `if`, `def` para usar indentación consistente (4 espacios)

2. **Errores de help_text vs help en models.py**
   - IA usó `help=` en lugar de `help_text=`
   - Solución manual: Corregir todos los campos `CharField` y `DateField` para usar el parámetro correcto `help_text`

3. **Problemas de namespace en URLs**
   - IA no configuró `app_name` en app URLs
   - Solución manual: Agregar `app_name = 'catalogo'` en `catalogo/urls.py` y usar `include('catalogo.urls')` en proyecto URLs

4. **Errores de campo en modelos de Admin**
   - IA incluyó `filter_horizontal = ('categorias',)` sin que el campo existiera
   - Solución manual: Revisar campos del modelo y usar `filter_horizontal = ()` o campos válidos

5. **Migraciones y base de datos**
   - IA generó errores de sintaxis en modelos
   - Solución manual: Corregir cada `help_text`, validar tipos de campo y ejecutar `makemigrations`/`migrate` iterativamente

6. **Estructura de templates**
   - IA dejó `{% block content %}{% endif %}` incorrecto
   - Solución manual: Corregir estructura de herencia de templates y asegurar que todos los `block` tengan `endblock`

## Qué Fue Verificado Manualment
- Ejecución del servidor `python manage.py runserver`
- Funcionamiento de endpoints HTTP
- Comportamiento de formularios en POST y GET
- Validaciones personalizadas en tiempo de ejecución
- Panel Django Admin configurado y funcional
- Flujo de autenticación (registro → login → dashboard)
- Pruebas automatizadas con `python manage.py test`
- Generación de `requirements.txt`
- Configuración de `manage.py check` y `manage.py check --deploy`
- Capturas de pantalla evidenciadas en `capturas/`

## Limitaciones Reconocidas
- Middleware personalizado: Planeado pero no fully implementado en esta fase
- Algunas validaciones avanzadas: Pendientes para futuras iteraciones
- Pruebas de seguridad extensas: Pendientes para entorno de producción
- Integración con PostgreSQL: Solo probado con SQLite en desarrollo

## Credenciales y Secretos
- Nunca se almacenaron credenciales reales en Git
- Credenciales de demostración usadas solo en entorno local
- `.env` no incluido en el repositorio (añadido a `.gitignore`)
- `SECRET_KEY` generado por Django por defecto (se recomienda cambiar para producción)