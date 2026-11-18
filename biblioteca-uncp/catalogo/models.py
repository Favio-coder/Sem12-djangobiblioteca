from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


def imagen_default():
    """Ruta de imagen por defecto para libros sin imagen."""
    return 'libros/default.jpg'


class Categoria(models.Model):
    """Modelo para categorizar libros."""
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Ej.: Literatura, Ciencias, Historia, etc."
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción opcional de la categoría"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('catalogo:categoria_detalle', kwargs={'pk': self.pk})


class Libro(models.Model):
    """Modelo principal para los libros de la biblioteca."""
    titulo = models.CharField(
        max_length=200,
        help_text="Título completo del libro"
    )
    autor = models.CharField(
        max_length=150,
        help_text="Nombre del autor o autores"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        help_text="ISBN-13 (opcional), formato: 978-3-16-148410-0"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='libros',
        help_text="Categoría del libro"
    )
    fecha_publicacion = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de publicación (AAAA-MM-DD)"
    )
    resumen = models.TextField(
        blank=True,
        help_text="Resumen o descripción del libro"
    )
    disponible = models.BooleanField(
        default=True,
        help_text="Indica si el libro está disponible para préstamo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['isbn']),
            models.Index(fields=['disponible']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    def get_absolute_url(self):
        return reverse('catalogo:libro_detalle', kwargs={'pk': self.pk})

    @property
    def es_reciente(self):
        """Propiedad: ¿es del último año?"""
        from datetime import date
        if self.fecha_publicacion:
            return self.fecha_publicacion.year >= date.today().year - 1
        return False

    @property
    def estatus_disponibilidad(self):
        """Propiedad: estado visual de disponibilidad."""
        if self.disponible:
            return "Disponible"
        return "No disponible"


class Prestamo(models.Model):
    """Modelo para registrar préstamos de libros."""
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='prestamos',
        help_text="Libro prestado"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='prestamos',
        help_text="Usuario que solicita el préstamo"
    )
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en que fue devuelto realmente"
    )
    devuelto = models.BooleanField(
        default=False,
        help_text="Indica si el libro fue devuelto"
    )
    observaciones = models.TextField(
        blank=True,
        help_text="Comentarios sobre el préstamo o devolución"
    )

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']
        unique_together = ['libro', 'usuario']
        indexes = [
            models.Index(fields=['libro', 'usuario']),
            models.Index(fields=['-fecha_prestamo']),
            models.Index(fields=['devuelto']),
        ]

    def __str__(self):
        return f"{self.libro.titulo} → {self.usuario.username} ({'Devuelto' if self.devuelto else 'Pendiente'})"

    @property
    def esta_vencido(self):
        """Propiedad: ¿la fecha de devolución esperada ya pasó?"""
        from django.utils import timezone
        if self.devuelto:
            return False
        return self.fecha_devolucion_esperada < timezone.now().date()

    @property
    def dias_atraso(self):
        """Propiedad: días de retraso en la devolución."""
        from django.utils import timezone
        if self.esta_vencido:
            return (timezone.now().date() - self.fecha_devolucion_esperada).days
        return 0


class PerfilUsuario(models.Model):
    """Perfil extendido para estudiantes y bibliotecarios."""
    ROLE_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('bibliotecario', 'Bibliotecario'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        unique=True
    )
    rol = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='estudiante',
        help_text="Rol del usuario en el sistema"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        help_text="Número de contacto"
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
        help_text="Dirección actual"
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de nacimiento"
    )
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        help_text="Foto de perfil del usuario"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.get_rol_display()})"

    @property
    def es_estudiante(self):
        return self.rol == 'estudiante'

    @property
    def es_bibliotecario(self):
        return self.rol == 'bibliotecario'

    @property
    def es_administrador(self):
        return self.rol == 'administrador'

    def get_rol_color(self):
        """Retorna un color asociado al rol para UI."""
        colores = {
            'estudiante': '#287A52',
            'bibliotecario': '#164B35',
            'administrador': '#D6AC53',
        }
        return colores.get(self.rol, '#6c757d')