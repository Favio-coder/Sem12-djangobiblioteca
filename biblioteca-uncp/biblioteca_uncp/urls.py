"""biblioteca_uncp URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalogo import views as catalogo_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo_views.landing_page, name='landing'),
    path('libros/', catalogo_views.lista_libros, name='lista_libros'),
    path('libro/<int:pk>/', catalogo_views.detalle_libro, name='detalle_libro'),
    path('registro/', catalogo_views.registro_usuario, name='registro'),
    path('login/', catalogo_views.login_view, name='login'),  # NOTE: will fix
    path('logout/', catalogo_views.logout_view, name='logout'),
    path('estudiante/dashboard/', catalogo_views.estudiante_dashboard, name='estudiante_dashboard'),
    path('estudiante/prestamo/<int:libro_pk>/', catalogo_views.estudiante_solicitar_prestamo, name='solicitar_prestamo'),
    path('estudiante/prestamos/', catalogo_views.estudiante_mis_prestamos, name='mis_prestamos'),
    path('bibliotecario/dashboard/', catalogo_views.bibliotecario_dashboard, name='bibliotecario_dashboard'),
    path('bibliotecario/registrar-libro/', catalogo_views.bibliotecario_registrar_libro, name='registrar_libro'),
    path('bibliotecario/editar-libro/<int:pk>/', catalogo_views.bibliotecario_editar_libro, name='editar_libro'),
    # API endpoints
    path('api/catalogo/', catalogo_views.api_catalogo_json, name='api_catalogo'),
    path('api/libro/<int:pk>/', catalogo_views.api_libro_detalle_json, name='api_libro_detalle'),
    path('api/prestamo/solicitar/', catalogo_views.api_solicitar_prestamo_json, name='api_solicitar_prestamo'),
]

# Servir archivos estáticos y de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)