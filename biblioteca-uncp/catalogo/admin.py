from django.contrib import admin
from .models import Libro, Categoria, Prestamo, PerfilUsuario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Administrador para el modelo Categoria."""
    list_display = ('nombre', 'descripcion_corta', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('created_at',)

    @admin.display(description='Descripción')
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] if obj.descripcion else "-"


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """Administrador para el modelo Libro."""
    list_display = ('titulo', 'autor', 'categoria', 'disponible', 'isbn_corto', 'created_at')
    list_filter = ('disponible', 'categoria', 'created_at')
    search_fields = ('titulo', 'autor', 'isbn')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()  # ManyToMany no usado, dejar vacío

    @admin.display(description='ISBN', ordering='isbn')
    def isbn_corto(self, obj):
        """Muestra los primeros 10 caracteres del ISBN."""
        if obj.isbn:
            return obj.isbn[:13]
        return "-"

    actions = ['marcar_disponible', 'marcar_no_disponible']

    @admin.action(description='Marcar libros como disponibles')
    def marcar_disponible(self, request, queryset):
        """Acción masiva: marcar libros como disponibles."""
        updated = queryset.update(disponible=True)
        self.message_user(
            request,
            f"{updated} libro(s) marcado(s) como disponibles.",
            level='success'
        )

    @admin.action(description='Marcar libros como no disponibles')
    def marcar_no_disponible(self, request, queryset):
        """Acción masiva: marcar libros como no disponibles."""
        updated = queryset.update(disponible=False)
        self.message_user(
            request,
            f"{updated} libro(s) marcado(s) como no disponibles.",
            level='warning'
        )


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    """Administrador para el modelo Prestamo."""
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion_esperada', 'devuelto', 'dias_atraso')
    list_filter = ('devuelto', 'fecha_prestamo', 'fecha_devolucion_esperada')
    search_fields = ('libro__titulo', 'usuario__username', 'observaciones')
    readonly_fields = ('fecha_prestamo',)
    date_hierarchy = 'fecha_prestamo'

    actions = ['marcar_como_devuelto']

    @admin.action(description='Marcar préstamos como devueltos')
    def marcar_como_devuelto(self, request, queryset):
        """Acción masiva: marcar préstamos como devueltos."""
        from django.utils import timezone
        actual = timezone.now().date()
        updated = 0
        for prestamo in queryset.filter(devuelto=False):
            prestamo.devuelto = True
            prestamo.fecha_devolucion_real = actual
            prestamo.save()
            updated += 1
        self.message_user(
            request,
            f"{updated} préstamo(s) marcado(s) como devueltos.",
            level='success'
        )


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Administrador para el modelo PerfilUsuario."""
    list_display = ('user', 'rol', 'telefono', 'fecha_nacimiento')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email', 'telefono')
    readonly_fields = ('creado_en', 'actualizado_en')