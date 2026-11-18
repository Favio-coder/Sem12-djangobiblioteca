from django.test import TestCase
from django.contrib.auth.models import User
from catalogo.models import Libro, Categoria, Prestamo, PerfilUsuario
from datetime import date
from django.utils import timezone


class ModeloLibroTest(TestCase):
    """Tests para el modelo Libro."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Literatura")
        self.libro = Libro.objects.create(
            titulo="Test Libro",
            autor="Test Autor",
            isbn="978-1-23456-789-0",
            categoria=self.categoria,
            disponible=True,
        )

    def test_libro_creacion(self):
        """Test que un libro se crea correctamente."""
        self.assertEqual(self.libro.titulo, "Test Libro")
        self.assertEqual(self.libro.autor, "Test Autor")
        self.assertTrue(self.libro.disponible)

    def test_libro_str_representation(self):
        """Test de la representación string del modelo."""
        expected = f"{self.libro.titulo} - {self.libro.autor}"
        self.assertEqual(str(self.libro), expected)

    def test_libro_estatus_disponibilidad(self):
        """Test de la propiedad de estatus de disponibilidad."""
        self.assertEqual(self.libro.estatus_disponibilidad, "Disponible")

    def test_libro_es_reciente(self):
        """Test de la propiedad de libro reciente."""
        # Crear un libro con fecha de publicación del año actual
        Libro.objects.create(
            titulo="Libro Reciente",
            autor="Autor Reciente",
            isbn="978-1-23456-789-1",
            fecha_publicacion=date.today(),
            disponible=True,
        )
        # Verificar que el libro creado es reciente
        libro_reciente = Libro.objects.get(titulo="Libro Reciente")
        self.assertTrue(libro_reciente.es_reciente)


class ModeloCategoriaTest(TestCase):
    """Tests para el modelo Categoria."""

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Test Categoria",
            descripcion="Descripción de prueba"
        )

    def test_categoria_creacion(self):
        """Test que una categoría se crea correctamente."""
        self.assertEqual(self.categoria.nombre, "Test Categoria")

    def test_categoria_str_representation(self):
        """Test de la representación string."""
        self.assertEqual(str(self.categoria), "Test Categoria")


class ModeloPrestamoTest(TestCase):
    """Tests para el modelo Prestamo."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123"
        )
        self.categoria = Categoria.objects.create(nombre="Literatura")
        self.libro = Libro.objects.create(
            titulo="Test Libro Préstamo",
            autor="Test Autor",
            categoria=self.categoria,
            disponible=True,
        )
        fecha_devol = date(2030, 12, 20)  # Fecha futura para testing
        self.prestamo = Prestamo.objects.create(
            libro=self.libro,
            usuario=self.user,
            fecha_devolucion_esperada=fecha_devol,
        )

    def test_prestamo_creacion(self):
        """Test que un préstamo se crea correctamente."""
        self.assertEqual(self.prestamo.libro, self.libro)
        self.assertEqual(self.prestamo.usuario, self.user)
        self.assertFalse(self.prestamo.devuelto)

    def test_prestamo_str_representation(self):
        """Test de la representación string del préstamo."""
        expected = f"{self.libro.titulo} → {self.user.username} ({'Devuelto' if self.prestamo.devuelto else 'Pendiente'})"
        self.assertEqual(str(self.prestamo), expected)

    def test_prestamo_esta_vencido(self):
        """Test de la propiedad de préstamo vencido."""
        # La fecha es futura, por lo tanto no está vencido
        self.assertFalse(self.prestamo.esta_vencido)

    def test_prestamo_dias_atraso(self):
        """Test de la propiedad de días de atraso."""
        self.assertEqual(self.prestamo.dias_atraso, 0)


class ModeloPerfilUsuarioTest(TestCase):
    """Tests para el modelo PerfilUsuario."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@test.com",
            password="testpass123"
        )
        self.perfil = PerfilUsuario.objects.create(
            user=self.user,
            rol="estudiante",
            telefono="987654321",
            direccion="Test Address",
        )

    def test_perfil_creacion(self):
        """Test que un perfil se crea correctamente."""
        self.assertEqual(self.perfil.user, self.user)
        self.assertEqual(self.perfil.rol, "estudiante")

    def test_perfil_rol_estudiante(self):
        """Test de la propiedad es_estudiante."""
        self.assertTrue(self.perfil.es_estudiante)

    def test_perfil_rol_bibliotecario(self):
        """Test de la propiedad es_bibliotecario."""
        self.perfil.rol = "bibliotecario"
        self.perfil.save()
        self.assertTrue(self.perfil.es_bibliotecario)

    def test_perfil_get_rol_color(self):
        """Test de la función get_rol_color."""
        color = self.perfil.get_rol_color()
        self.assertEqual(color, "#287A52")  # Color de estudiante


class ModeloRelacionesTest(TestCase):
    """Tests para las relaciones entre modelos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="reltest",
            email="rel@test.com",
            password="testpass123"
        )
        self.categoria = Categoria.objects.create(nombre="Historia")
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba",
            autor="Autor Prueba",
            categoria=self.categoria,
        )
        self.perfil = PerfilUsuario.objects.create(
            user=self.user,
            rol="estudiante",
        )
        self.prestamo = Prestamo.objects.create(
            libro=self.libro,
            usuario=self.user,
            fecha_devolucion_esperada="2025-01-01",
        )

    def test_usuario_tiene_perfil(self):
        """Test que un usuario tiene perfil asociado."""
        self.assertIsNotNone(self.user.perfil)

    def test_prestamos_del_usuario(self):
        """Test que un usuario tiene préstamos."""
        prestamos = Prestamo.objects.filter(usuario=self.user)
        self.assertEqual(prestamos.count(), 1)

    def test_libros_por_categoria(self):
        """Test que se pueden obtener libros por categoría."""
        libros = Libro.objects.filter(categoria=self.categoria)
        self.assertEqual(libros.count(), 1)
        self.assertEqual(libros[0].titulo, "Libro de Prueba")