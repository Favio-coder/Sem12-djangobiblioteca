from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalogo.models import Libro, Categoria, Prestamo, PerfilUsuario


class Command(BaseCommand):
    help="Pobla la base de datos con datos de demostración"

    def handle(self, *args, **options):
        # Crear categorías
        categorias_data = [
            "Literatura",
            "Ciencias",
            "Historia",
            "Matemáticas",
            "Filosofía",
            "Arte",
            "Tecnología",
            "Ciencias Sociales",
        ]
        categorias = []
        for cat_name in categorias_data:
            cat, created = Categoria.objects.get_or_create(nombre=cat_name)
            categorias.append(cat)
            if created:
                self.stdout.write(f"Creada categoría: {cat_name}")

        # Crear libros de ejemplo (usando fechas válidas YYYY-MM-DD)
        libros_data = [
            {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "categoria_idx": 0, "isbn": "978-84-376-0008-7", "fecha_publicacion": "1605-01-16", "resumen": "La obra cumbre de la literatura española", "disponible": True},
            {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria_idx": 0, "isbn": "978-0-307-38137-8", "fecha_publicacion": "1967-05-30", "resumen": "Multigeneracional historia de la familia Buendía", "disponible": True},
            {"titulo": "Historia de la Filosofía Griega", "autor": "Alfred Edward Taylor", "categoria_idx": 1, "isbn": "978-84-470-3079-1", "fecha_publicacion": "1990-01-15", "resumen": "Origen y desarrollo del pensamiento filosófico griego", "disponible": True},
            {"titulo": "Breve historia del tiempo", "autor": "Stephen Hawking", "categoria_idx": 1, "isbn": "978-84-9759-339-5", "fecha_publicacion": "1988-04-01", "resumen": "Exploración del universo y los agujeros negros", "disponible": True},
            {"titulo": "Los Santos Mártires", "autor": "Anónimo", "categoria_idx": 2, "isbn": "978-84-96388-01-5", "fecha_publicacion": "2000-01-01", "resumen": "Vidas de santos cristianos", "disponible": True},
            {"titulo": "Fundamentos de Programación", "autor": "José González", "categoria_idx": 3, "isbn": "978-84-471-0689-5", "fecha_publicacion": "2015-09-15", "resumen": "Conceptos básicos de programación", "disponible": True},
            {"titulo": "El Principito", "autor": "Antoine de Saint-Exupéry", "categoria_idx": 0, "isbn": "978-84-204-8260-8", "fecha_publicacion": "1943-04-06", "resumen": "Fábula sobre la vida y la amistad", "disponible": True},
            {"titulo": "Arte del Siglo XX", "autor": "Varios autores", "categoria_idx": 5, "isbn": "978-84-9029-953-2", "fecha_publicacion": "2010-03-01", "resumen": "Repaso de las corrientes artísticas modernas", "disponible": True},
            {"titulo": "Introducción a la Física Moderna", "autor": "Luis Álvarez", "categoria_idx": 1, "isbn": "978-84-123456-0-1", "fecha_publicacion": "2020-06-20", "resumen": "Conceptos básicos de física contemporánea", "disponible": True},
            {"titulo": "Química Orgánica", "autor": "Maria Rodríguez", "categoria_idx": 1, "isbn": "978-84-1234567-8-9", "fecha_publicacion": "2018-10-10", "resumen": "Estructura y reacciones de compuestos orgánicos", "disponible": True},
        ]

        for libro_data in libros_data:
            cat_idx = libro_data.pop("categoria_idx")
            categoria = categorias[cat_idx] if cat_idx < len(categorias) else categorias[0]
            libro_data["categoria"] = categoria

            # Quitar el índice antes de crear
            libro_data.pop("categoria_idx", None)

            titulo = libro_data["titulo"]
            isbn = libro_data.get("isbn")

            # Verificar si ya existe por título o ISBN
            libro_filters = {}
            if isbn:
                libro_filters["isbn"] = isbn
            else:
                libro_filters["titulo"] = titulo

            defaults = {k: v for k, v in libro_data.items() if k != "titulo" and k != "isbn"}

            libro, created = Libro.objects.get_or_create(**libro_filters, defaults=defaults)
            if created:
                self.stdout.write(f"Creado libro: {titulo}")
            else:
                self.stdout.write(f"Libro ya existe: {titulo}")

        # Crear usuarios de prueba
        usuarios_data = [
            {"username": "estudiante1", "email": "estudiante1@uncp.edu.pe", "password": "12345", "rol": "estudiante"},
            {"username": "estudiante2", "email": "estudiante2@uncp.edu.pe", "password": "12345", "rol": "estudiante"},
            {"username": "bibliotecario1", "email": "bibliotecario1@uncp.edu.pe", "password": "12345", "rol": "bibliotecario"},
            {"username": "admin1", "email": "admin1@uncp.edu.pe", "password": "12345", "rol": "administrador"},
        ]

        for user_data in usuarios_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"]}
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
                # Crear perfil
                perfil, created = PerfilUsuario.objects.get_or_create(user=user)
                perfil.rol = user_data["rol"]
                perfil.save()
                self.stdout.write(f"Creado usuario: {user_data['username']} ({perfil.get_rol_display()})")
            else:
                self.stdout.write(f"Usuario ya existe: {user_data['username']}")

        # Crear algunos préstamos de demostración
        from django.utils import timezone
        from datetime import timedelta

        # Obtener usuarios y libros
        estudiante1_user = User.objects.get(username="estudiante1")
        estudiante2_user = User.objects.get(username="estudiante2")
        bibliotecario1_user = User.objects.get(username="bibliotecario1")

        # Obtener algunos libros disponibles
        libros_disponibles = Libro.objects.filter(disponible=True)[:5]

        # Préstamo de estudiante 1
        if libros_disponibles.exists():
            libro1 = libros_disponibles.first()
            fecha_devolucion = timezone.now().date() + timedelta(days=15)
            Prestamo.objects.get_or_create(
                libro=libro1,
                usuario=estudiante1_user,
                defaults={
                    "fecha_devolucion_esperada": fecha_devolucion,
                    "devuelto": False,
                }
            )
            libro1.disponible = False
            libro1.save()
            self.stdout.write(f"Préstamo creado para estudiante1 con {libro1.titulo}")

        # Préstamo de estudiante 2
        if libros_disponibles.count() > 1:
            libro2 = libros_disponibles[1]
            fecha_devolucion = timezone.now().date() + timedelta(days=15)
            Prestamo.objects.get_or_create(
                libro=libro2,
                usuario=estudiante2_user,
                defaults={
                    "fecha_devolucion_esperada": fecha_devolucion,
                    "devuelto": False,
                }
            )
            libro2.disponible = False
            libro2.save()
            self.stdout.write(f"Préstamo creado para estudiante2 con {libro2.titulo}")

        # Préstamo de bibliotecario (marcar como devuelto después)
        if libros_disponibles.count() > 2:
            libro3 = libros_disponibles[2]
            Prestamo.objects.get_or_create(
                libro=libro3,
                usuario=bibliotecario1_user,
                defaults={
                    "fecha_devolucion_esperada": timezone.now().date() - timedelta(days=5),
                    "devuelto": True,
                    "observaciones": "Préstamo de prueba devuelto",
                }
            )
            self.stdout.write(f"Préstamo creado para bibliotecario con {libro3.titulo} (devuelto)")

        self.stdout.write(self.style.SUCCESS("¡Datos de demostración poblados exitosamente!"))