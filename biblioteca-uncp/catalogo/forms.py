from django import forms
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from .models import Libro, Categoria, Prestamo


# --- Formularios basados en ModelForm ---

class LibroModelForm(forms.ModelForm):
    """ModelForm para registro de libros (Vista Bibliotecario)."""

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'categoria', 'fecha_publicacion', 'resumen', 'disponible']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del libro'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-13 (opcional)'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Resumen del libro'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'categoria': 'Categoría',
            'fecha_publicacion': 'Fecha de publicación',
            'resumen': 'Resumen',
            'disponible': '¿Disponible?',
        }
        help_texts = {
            'isbn': 'Formato ISBN-13 opcional',
            'fecha_publicacion': 'Formato AAAA-MM-DD',
        }

    def clean_isbn(self):
        """Validación personalizada de ISBN."""
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            # Quitar guiones y espacios
            isbn_limpio = isbn.replace('-').replace(' ').strip()
            # Validar que tenga 13 dígitos si tiene longitud
            if len(isbn_limpio) == 13 and isbn_limpio.isdigit():
                # Validar checksum del ISBN-13
                checksum = 0
                for i, digito in enumerate(isbn_limpio):
                    numero = int(digito)
                    if i % 2 == 0:
                        checksum += numero
                    else:
                        checksum += numero * 3
                if checksum % 10 != 0:
                    raise ValidationError("ISBN-13 inválido: el dígito de verificación no es correcto.")
            elif len(isbn_limpio) > 0 and not isbn_limpio.isdigit():
                raise ValidationError("El ISBN debe contener solo números y guiones.")
        return isbn


class PrestamoModelForm(forms.ModelForm):
    """ModelForm para solicitud de préstamos (Vista Estudiante)."""

    class Meta:
        model = Prestamo
        fields = ['libro', 'fecha_devolucion_esperada']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'}),
            'fecha_devolucion_esperada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'libro': 'Libro',
            'fecha_devolucion_esperada': 'Fecha de devolución esperada',
        }

    def clean(self):
        """Validación cruzada del préstamo."""
        cleaned_data = super().clean()
        libro = cleaned_data.get('libro')
        fecha_devolucion = cleaned_data.get('fecha_devolucion_esperada')

        if libro and fecha_devolucion:
            from django.utils import timezone
            # No permitir fechas de devolución anteriores al préstamo
            # (usamos la fecha actual como referencia mínima)
            if fecha_devolucion < timezone.now().date():
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior a hoy."
                )
            # Verificar que el libro esté disponible
            if not libro.disponible:
                raise ValidationError(
                    f"El libro '{libro.titulo}' no está disponible para préstamo."
                )
        return cleaned_data


# --- Formularios puros (forms.Form) ---

class RegistroUsuarioForm(forms.Form):
    """Formulario clásico para registro de usuarios."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        help_text="Requerido. 150 caracteres como máximo. Letras, dígitos y @/./+/-/_ solo."
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        help_text="Notificaciones importantes serán enviadas aquí."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        help_text="Tu contraseña se utiliza para autenticarte en el sistema."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita contraseña'}),
        help_text="Ingrese la misma contraseña nuevamente para confirmar."
    )
    rol = forms.ChoiceField(
        choices=[('estudiante', 'Estudiante'), ('bibliotecario', 'Bibliotecario')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='estudiante'
    )

    def clean_username(self):
        """Validar que el nombre de usuario no esté en uso."""
        from django.contrib.auth.models import User
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso. Por favor elija otro.")
        return username

    def clean_email(self):
        """Validar que el email no esté en uso."""
        from django.contrib.auth.models import User
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        """Guardar el usuario usando el sistema de autenticación de Django."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        # Asignar rol mediante el perfil
        from .models import PerfilUsuario
        perfil, created = PerfilUsuario.objects.get_or_create(user=user)
        perfil.rol = self.cleaned_data['rol']
        if commit:
            perfil.save()
        return user


class BusquedaLibrosForm(forms.Form):
    """Formulario para búsqueda de catálogo."""

    BUSCAR_POR_CHOICES = [
        ('titulo', 'Título'),
        ('autor', 'Autor'),
        ('categoria', 'Categoría'),
    ]

    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, autor o categoría...',
            'aria-label': 'Buscar'
        })
    )
    por = forms.ChoiceField(
        choices=BUSCAR_POR_CHOICES,
        initial='titulo',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all().order_by('nombre'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        empty_label="Todas las categorías"
    )


class ContactoForm(forms.Form):
    """Formulario de contacto para consultas."""

    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
        required=False
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo'}),
        required=False
    )
    asunto = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}),
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tu mensaje'}),
    )

    def clean_mensaje(self):
        """Validar que el mensaje no sea solo espacios."""
        mensaje = self.cleaned_data.get('mensaje')
        if mensaje and mensaje.strip() == '':
            raise ValidationError("El mensaje no puede contener solo espacios en blanco.")
        return mensaje


class SolicitudPrestamoForm(forms.Form):
    """Formulario clásico para solicitud de préstamo."""

    libro_id = forms.IntegerField(widget=forms.HiddenInput())
    motivo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del préstamo', 'required': False}),
        required=False
    )

    def clean_libro_id(self):
        """Validar que el libro existe y está disponible."""
        from .models import Libro
        libro_id = self.cleaned_data['libro_id']
        try:
            libro = Libro.objects.get(pk=libro_id)
            if not libro.disponible:
                raise ValidationError(f"El libro '{libro.titulo}' no está disponible.")
            return libro_id
        except Libro.DoesNotExist:
            raise ValidationError("El libro solicitado no existe.")