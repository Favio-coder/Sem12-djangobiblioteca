# Guía de Ejecución - Biblioteca UNCP

## Prerrequisitos
- Python 3.11 o superior
- Git
- Navegador web moderno

## Pasos para Ejecutar el Proyecto

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd biblioteca-uncp
```

### 2. Crear Entorno Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```
*O instalar Django manualmente:*
```bash
pip install django==5.1.6 pillow
```

### 4. Configurar la Base de Datos
```bash
# Migrar esquemas
python manage.py makemigrations catalogo
python manage.py migrate

# Poblar datos de demostración
python manage.py poblar_datos
```

### 5. Iniciar el Servidor
```bash
python manage.py runserver 0.0.0.0:8000
```
*El servidor estará disponible en http://localhost:8000*

### 6. Acceder al Sistema
- **Página principal**: `/`
- **Catálogo de libros**: `/libros/`
- **Registro**: `/registro/`
- **Login**: `/login/`

## Credenciales de Prueba
Ejecutando `python manage.py poblar_datos` se crean estos usuarios:

| Usuario | Correo | Contraseña | Rol |
|---------|--------|------------|-----|
| estudiante1 | estudiante1@uncp.edu.pe | 12345 | Estudiante |
| estudiante2 | estudiante2@uncp.edu.pe | 12345 | Estudiante |
| bibliotecario1 | bibliotecario1@uncp.edu.pe | 12345 | Bibliotecario |
| admin1 | admin1@uncp.edu.pe | 12345 | Administrador |

## Comandos Útiles
```bash
# Verificar configuración
python manage.py check

# Verificar despliegue
python manage.py check --deploy

# Ejecutar pruebas
python manage.py test catalogo.tests

# Acceder a Django Admin
# http://localhost:8000/admin/
# Usuario: admin1 / Contraseña: 12345
```

## Estructura de URLs Principales
- `/` - Landing page de Biblioteca UNCP
- `/libros/` - Catálogo de libros
- `/libro/<int:pk>/` - Detalle de libro
- `/registro/` - Registro de usuario
- `/login/` - Inicio de sesión
- `/logout/` - Cierre de sesión
- `/estudiante/dashboard/` - Dashboard estudiantil
- `/bibliotecario/dashboard/` - Dashboard bibliotecario
- `/api/catalogo/` - API JSON del catálogo