from django.urls import path
from . import views as catalogo_views

app_name = 'catalogo'

urlpatterns = [
    path('', catalogo_views.landing_page, name='landing'),
    path('libros/', catalogo_views.lista_libros, name='lista_libros'),
    path('libro/<int:pk>/', catalogo_views.detalle_libro, name='detalle_libro'),
    path('registro/', catalogo_views.registro_usuario, name='registro'),
    path('login/', catalogo_views.login_view, name='login'),
    path('logout/', catalogo_views.logout_view, name='logout'),
    path('estudiante/dashboard/', catalogo_views.estudiante_dashboard, name='estudiante_dashboard'),
    path('estudiante/prestamo/<int:libro_pk>/', catalogo_views.estudiante_solicitar_prestamo, name='solicitar_prestamo'),
    path('estudiante/prestamos/', catalogo_views.estudiante_mis_prestamos, name='mis_prestamos'),
    path('bibliotecario/dashboard/', catalogo_views.bibliotecario_dashboard, name='bibliotecario_dashboard'),
    path('bibliotecario/registrar-libro/', catalogo_views.bibliotecario_registrar_libro, name='registrar_libro'),
    path('bibliotecario/editar-libro/<int:pk>/', catalogo_views.bibliotecario_editar_libro, name='editar_libro'),
]