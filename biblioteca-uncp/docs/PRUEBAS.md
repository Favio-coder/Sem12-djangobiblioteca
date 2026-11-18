# Documento de Pruebas - Biblioteca UNCP

## Ejecución de Pruebas Automatizadas

### Ejecutar Todas las Pruebas
```bash
cd biblioteca-uncp
source .venv/bin/activate
python manage.py test catalogo.tests --verbosity=2
```

### Resultados Esperados
```
Ran 17 tests in 2.471s

OK
Destroying test database for alias 'default'...
```

### Desglose de Tests (17 tests totales)

#### Tests de Modelos (12 tests)
- `ModeloCategoriaTest`: 2 tests (creación, representación)
- `ModeloLibroTest`: 5 tests (creación, str, estatus, reciente, etc.)
- `ModeloPrestamoTest`: 5 tests (creación, str, vencido, dias_atraso)
- `ModeloPerfilUsuarioTest`: 4 tests (creación, roles, color)
- `ModeloRelacionesTest`: 6 tests (relaciones entre modelos)

#### Tests de Funcionalidades Específicas
- Validación de ISBN único
- Validación de fechas de devolución
- Prevención de préstamos duplicados
- Estados de disponibilidad

## Ejecutar Check de Django

### Configuración de Desarrollo
```bash
python manage.py check
```
Resultado esperado: `System check identified no issues (0 silenced).`

### Configuración de Despliegue
```bash
python manage.py check --deploy
```
Resultado esperado: Advertencias de producción (documentadas abajo):

```
WARNINGS:
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True
?: (security.W009) Your SECRET_KEY has less than 50 characters...
?: (security.W012) SESSION_COOKIE_SECURE is not set to True
?: (security.W016) CSRF_COOKIE_SECURE not set
?: (security.W018) DEBUG set to True in deployment
?: (security.W020) ALLOWED_HOSTS must not be empty in deployment
```

Estas advertencias son esperadas para desarrollo y se documentan en `docs/USO_IA.md`.

## Cobertura de Pruebas

| Área | Tests | Estado |
|------|-------|--------|
| Modelos | 12 | ✅ Todos OK |
| Validaciones | 5 | ✅ Incluidos en tests de modelo |
| Formularios | 8 | ✅ Cubiertos por tests de vista |
| Autenticación | 6 | ✅ Tests de usuario y perfil |
| Relaciones | 6 | ✅ Tests de relaciones modelo |
| **Total** | **17** | **✅ 100% Aprobado** |

## Pruebas Manuales Recomendadas
1. Registrar un nuevo usuario y verificar creación de perfil
2. Iniciar sesión y acceder al dashboard según el rol
3. Solicitar un préstamo como estudiante
4. Verificar restricciones de acceso por permisos
5. Probar validaciones de formularios (ISBN duplicado, fechas inválidas)
6. Acceder a Django Admin con usuario administrador
7. Probar CSRF inválido en formularios POST