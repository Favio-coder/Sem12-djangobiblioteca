from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Libro, Categoria, Prestamo, PerfilUsuario
from .forms import (
    LibroModelForm,
    PrestamoModelForm,
    RegistroUsuarioForm,
    BusquedaLibrosForm,
    ContactoForm,
    SolicitudPrestamoForm,
)


def landing_page(request):
    """Vista de landing page de Biblioteca UNCP."""
    libros_destacados = Libro.objects.filter(disponible=True)[:6]
    categorias = Categoria.objects.all()[:5]

    contexto = {
        'titulo': 'Biblioteca UNCP',
        'libros_destacados': libros_destacados,
        'categorias': categorias,
    }
    return render(request, 'catalogo/landing.html', contexto)


def lista_libros(request):
    """Vista del catálogo de libros con búsqueda y filtros."""
    form = BusquedaLibrosForm(request.GET or None)
    query = request.GET.get('query', '')
    por = request.GET.get('por', 'titulo')
    categoria_id = request.GET.get('categoria', '')

    libros = Libro.objects.all().order_by('titulo')

    if form.is_valid():
        query = form.cleaned_data.get('query', query)
        por = form.cleaned_data.get('por', por)
        categoria_id = form.cleaned_data.get('categoria', categoria_id)

    if query:
        if por == 'titulo':
            libros = libros.filter(titulo__icontains=query)
        elif por == 'autor':
            libros = libros.filter(autor__icontains=query)
        elif por == 'categoria' and categoria_id:
            libros = libros.filter(categoria_id=categoria_id)

    # Paginación
    paginator = Paginator(libros, 12)  # 12 libros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'titulo': 'Catálogo de Libros',
        'form_busqueda': form,
        'page_obj': page_obj,
        'query': query,
        'por': por,
    }
    return render(request, 'catalogo/lista_libros.html', contexto)


def detalle_libro(request, pk):
    """Vista de detalle de un libro específico."""
    libro = get_object_or_404(Libro, pk=pk)
    # Libros relacionados por misma categoría
    relacionados = Libro.objects.filter(
        categoria=libro.categoria
    ).exclude(pk=libro.pk)[:4] if libro.categoria else []

    # Verificar si el usuario ya tiene un préstamo activo
    prestamo_activo = None
    if request.user.is_authenticated:
        try:
            prestamo_activo = Prestamo.objects.get(
                libro=libro,
                usuario=request.user,
                devuelto=False
            )
        except Prestamo.DoesNotExist:
            prestamo_activo = None

    contexto = {
        'titulo': f'Detalle: {libro.titulo}',
        'libro': libro,
        'relacionados': relacionados,
        'prestamo_activo': prestamo_activo,
    }
    return render(request, 'catalogo/detalle_libro.html', contexto)


@require_http_methods(["GET", "POST"])
def registro_usuario(request):
    """Vista para registro de nuevos usuarios."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Cuenta creada exitosamente para {user.username}.")
            return redirect('catalogo:login')
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        form = RegistroUsuarioForm()

    contexto = {
        'formulario': form,
        'es_registro': True,
    }
    return render(request, 'catalogo/registro.html', contexto)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de inicio de sesión."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Determinar redirección basada en el rol
            perfil, created = PerfilUsuario.objects.get_or_create(user=user)
            if perfil.rol == 'bibliotecario':
                return redirect('catalogo:bibliotecario_dashboard')
            else:
                return redirect('catalogo:estudiante_dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'catalogo/login.html', {'es_registro': False})


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Vista de cierre de sesión."""
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('catalogo:landing')


@login_required
def estudiante_dashboard(request):
    """Dashboard para estudiantes."""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)

    # Obtener préstamos del usuario
    mis_prestamos = Prestamo.objects.filter(
        usuario=request.user
    ).order_by('-fecha_prestamo')

    # Contadores
    total_prestamos = mis_prestamos.count()
    prestamos_activos = mis_prestamos.filter(devuelto=False).count()
    prestamos_devueltos = mis_prestamos.filter(devuelto=True).count()

    contexto = {
        'titulo': 'Dashboard Estudiantil',
        'perfil': perfil,
        'mis_prestamos': mis_prestamos,
        'total_prestamos': total_prestamos,
        'prestamos_activos': prestamos_activos,
        'prestamos_devueltos': prestamos_devueltos,
    }
    return render(request, 'catalogo/estudiante_dashboard.html', contexto)


@login_required
def estudiante_solicitar_prestamo(request, libro_pk):
    """Vista para que un estudiante solicite un préstamo."""
    libro = get_object_or_404(Libro, pk=libro_pk)
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)

    # Verificar que el estudiante pueda solicitar
    if perfil.rol != 'estudiante':
        return HttpResponseForbidden("No tiene permisos para solicitar préstamos.")

    # Verificar si ya tiene un préstamo activo de este libro
    prestamo_existente = Prestamo.objects.filter(
        libro=libro,
        usuario=request.user,
        devuelto=False
    ).first()

    if request.method == 'POST':
        # Procesar la solicitud
        from django.utils import timezone

        if prestamo_existente:
            messages.warning(request, "Ya tienes un préstamo activo de este libro.")
            return redirect('catalogo:detalle_libro', pk=libro.pk)

        # Verificar disponibilidad
        if not libro.disponible:
            messages.error(request, "Lo siento, este libro no está disponible.")
            return redirect('catalogo:detalle_libro', pk=libro.pk)

        # Crear el préstamo
        from datetime import timedelta
        fecha_devolucion = timezone.now().date() + timedelta(days=15)  # 15 días

        Prestamo.objects.create(
            libro=libro,
            usuario=request.user,
            fecha_devolucion_esperada=fecha_devolucion,
        )

        libro.disponible = False
        libro.save()

        messages.success(request, f"Solicitud de préstamo para '{libro.titulo}' exitosamente.")
        return redirect('catalogo:estudiante_dashboard')

    contexto = {
        'titulo': f'Solicitar préstamo: {libro.titulo}',
        'libro': libro,
        'perfil': perfil,
    }
    return render(request, 'catalogo/solicitar_prestamo.html', contexto)


@login_required
def estudiante_mis_prestamos(request):
    """Vista para ver los préstamos del estudiante."""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    mis_prestamos = Prestamo.objects.filter(
        usuario=request.user
    ).order_by('-fecha_prestamo')

    contexto = {
        'titulo': 'Mis Préstamos',
        'perfil': perfil,
        'mis_prestamos': mis_prestamos,
    }
    return render(request, 'catalogo/mis_prestamos.html', contexto)


@login_required
def bibliotecario_dashboard(request):
    """Dashboard para bibliotecarios con estadísticas."""
    from django.db.models import Count

    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if perfil.rol != 'bibliotecario' and not request.user.is_superuser:
        return HttpResponseForbidden("No tiene permisos para ver el panel bibliotecario.")

    # Estadísticas generales
    total_libros = Libro.objects.count()
    libros_disponibles = Libro.objects.filter(disponible=True).count()
    libros_prestados = Libro.objects.filter(disponible=False).count()
    total_prestamos = Prestamo.objects.count()
    prestamos_pendientes = Prestamo.objects.filter(devuelto=False).count()
    prestamos_devueltos = Prestamo.objects.filter(devuelto=True).count()

    # Libros más prestados
    libros_mas_prestados = Libro.objects.annotate(
        num_prestamos=Count('prestamos')
    ).order_by('-num_prestamos')[:5]

    contexto = {
        'titulo': 'Dashboard Bibliotecario',
        'total_libros': total_libros,
        'libros_disponibles': libros_disponibles,
        'libros_prestados': libros_prestados,
        'total_prestamos': total_prestamos,
        'prestamos_pendientes': prestamos_pendientes,
        'prestamos_devueltos': prestamos_devueltos,
        'libros_mas_prestados': libros_mas_prestados,
    }
    return render(request, 'catalogo/bibliotecario_dashboard.html', contexto)


@login_required
@require_http_methods(["GET", "POST"])
def bibliotecario_registrar_libro(request):
    """Vista para que un bibliotecario registre un nuevo libro."""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)

    if perfil.rol != 'bibliotecario' and not request.user.is_superuser:
        return HttpResponseForbidden("No tiene permisos para registrar libros.")

    if request.method == 'POST':
        form = LibroModelForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            # Verificar ISBN duplicado
            isbn = form.cleaned_data.get('isbn')
            if isbn and Libro.objects.filter(isbn=isbn).exclude(pk=request.POST.get('id', None)).exists():
                form.add_error('isbn', "Ya existe un libro con este ISBN.")
                return render(request, 'catalogo/registrar_libro.html', {'formulario': form, 'perfil': perfil})
            libro.save()
            messages.success(request, f"Libro '{libro.titulo}' registrado exitosamente.")
            return redirect('catalogo:bibliotecario_dashboard')
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        form = LibroModelForm()

    contexto = {
        'titulo': 'Registrar Nuevo Libro',
        'formulario': form,
        'perfil': perfil,
    }
    return render(request, 'catalogo/registrar_libro.html', contexto)


@login_required
@require_http_methods(["GET", "POST"])
def bibliotecario_editar_libro(request, pk):
    """Vista para editar información de un libro."""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)

    if perfil.rol != 'bibliotecario' and not request.user.is_superuser:
        return HttpResponseForbidden("No tiene permisos para editar libros.")

    libro = get_object_or_404(Libro, pk=pk)

    if request.method == 'POST':
        form = LibroModelForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f"Libro '{libro.titulo}' actualizado exitosamente.")
            return redirect('catalogo:detalle_libro', pk=libro.pk)
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        form = LibroModelForm(instance=libro)

    contexto = {
        'titulo': f'Editar libro: {libro.titulo}',
        'formulario': form,
        'libro': libro,
        'perfil': perfil,
    }
    return render(request, 'catalogo/editar_libro.html', contexto)


# API ligera en JSON para integración con Postman y frontend

def api_catalogo_json(request):
    """Endpoint JSON para obtener el catálogo filtrado."""
    import json
    query = request.GET.get('q', '')
    libros = Libro.objects.filter(disponible=True)

    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query)
        )

    data = []
    for libro in libros[:20]:
        data.append({
            'id': libro.pk,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'isbn': libro.isbn,
            'categoria': str(libro.categoria) if libro.categoria else '',
            'disponible': libro.disponible,
        })

    return JsonResponse({'libros': data, 'total': len(data)})


def api_libro_detalle_json(request, pk):
    """Endpoint JSON para detalle de un libro."""
    libro = get_object_or_404(Libro, pk=pk)
    return JsonResponse({
        'id': libro.pk,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'isbn': libro.isbn,
        'categoria': str(libro.categoria) if libro.categoria else '',
        'fecha_publicacion': str(libro.fecha_publicacion) if libro.fecha_publicacion else None,
        'resumen': libro.resumen,
        'disponible': libro.disponible,
    })


@csrf_exempt  # Solo para demostración; en producción usar CSRF proper
def api_solicitar_prestamo_json(request):
    """Endpoint JSON para solicitar préstamo vía AJAX."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    from django.utils import timezone
    from .models import Libro, Prestamo

    libro_id = request.POST.get('libro_id')
    if not libro_id:
        return JsonResponse({'error': 'ID de libro requerido'}, status=400)

    try:
        libro = Libro.objects.get(pk=libro_id)
    except Libro.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)

    if not libro.disponible:
        return JsonResponse({'error': 'Libro no disponible'}, status=400)

    # Verificar préstamo activo existente
    prestamo_existente = Prestamo.objects.filter(
        libro=libro,
        usuario=request.user,
        devuelto=False
    ).first()
    if prestamo_existente:
        return JsonResponse({'error': 'Ya tienes un préstamo activo de este libro'}, status=400)

    from datetime import timedelta
    fecha_devolucion = timezone.now().date() + timedelta(days=15)

    Prestamo.objects.create(
        libro=libro,
        usuario=request.user,
        fecha_devolucion_esperada=fecha_devolucion,
    )

    libro.disponible = False
    libro.save()

    return JsonResponse({
        'success': True,
        'mensaje': f"Préstamo solicitado para '{libro.titulo}'",
        'fecha_devolucion': str(fecha_devolucion),
    })
