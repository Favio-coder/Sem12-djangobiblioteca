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

        # Crear libros de ejemplo
        libros_data = [
            {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "categoria": categorias[0], "isbn": "978-84-376-0008-7", "fecha_publicacion": "1605-01-16", "resumen": "La obra cumbre de la literatura española", "disponible": True},
            {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": categorias[0], "isbn": "978-0-307-38137-8", "fecha_publicacion": "1967-05-30", "resumen": "Multigeneracional historia de la familia Buendía", "disponible": True},
            {"titulo": "Historia de la Filosofía Griega", "autor": "Alfred Edward Taylor", "categoria": categorias[1], "isbn": "978-84-470-3079-1", "fecha_publicacion": "1990-01-01", "resumen": "Origen y desarrollo del pensamiento filosófico griego", "disponible": True},
            {"titulo": "Breve historia del tiempo", "autor": "Stephen Hawking", "categoria": categorias[1], "isbn": "978-84-9759-339-5", "fecha_publicacion": "1988-04-01", "resumen": "Exploración del universo y los agujeros negros", "disponible": True},
            {"titulo": "Los Santos Mártires", "autor": "Anónimo", "categoria": categorias[2], "isbn": "978-84-96388-01-5", "fecha_publicacion": "2000-01-01", "resumen": "Vidas de santos cristianos", "disponible": True},
            {"titulo": "La Odisea", "autor": "Homero", "categoria": categorias[2], "isbn": "978-84-205-0694-7", "fecha_publicacion": "-0800-01-01", "resumen": "Épica jornada de Odiseo de regreso a Ítaca", "disponible": True},
            {"titulo": "Introducción a la Matemática", "autor": "Richard Rusczyk", "categoria": categorias[3], "isbn": "978-1-934124-11-5", "fecha_publicacion": "2007-01-01", "resumen": "Fundamentos de matemáticas para estudiantes", "disponible": True},
            {"titulo": "El Principito", "autor": "Antoine de Saint-Exupéry", "categoria": categorias[0], "isbn": "978-84-204-8260-8", "fecha_publicacion": "1943-04-06", "resumen": "Fábula sobre la vida y la amistad", "disponible": True},
            {"titulo": "Fundamentos de Programación", "autor": "José González", "categoria": categorias[4], "isbn": "978-84-471-0689-5", "fecha_publicacion": "2015-09-15", "resumen": "Conceptos básicos de programación", "disponible": True},
            {"titulo": "Arte del Siglo XX", "autor": "Varios autores", "categoria": categorias[5], "isbn": "978-84-9029-953-2", "fecha_publicacion": "2010-03-01", "resumen": "Repaso de las corrientes artísticas modernas", "disponible": True},
        ]

        for libro_data in libros_data:
            # Crear o obtener el libro por ISBN
            libro, created = Libro.objects.get_or_create(
                isbn=libro_data["isbn"],
                defaults={
                    "titulo": libro_data["titulo"],
                    "autor": libro_data["autor"],
                    "categoria": libro_data["categoria"],
                    "fecha_publicacion": libro_data["fecha_publicacion"],
                    "resumen": libro_data["resumen"],
                    "disponible": libro_data["disponible"],
                }
            )
            if created:
                self.stdout.write(f"Creado libro: {libro.titulo}")
            else:
                self.stdout.write(f"Libro ya existe: {libro.titulo}")

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

        # Obtener algunos libros y usuarios
        estudiante_user = User.objects.get(username="estudiante1")
        estudiante_perfil = PerfilUsuario.objects.get(user=estudiante_user)
        libro1 = Libro.objects.first()
        libro2 = Libro.objects.second() if Libro.objects.count() > 1 else Libro.objects.first()

        # Préstamo de estudiante 1
        if libro1 and libro1.disponible:
            fecha_devolucion = timezone.now().date() + timedelta(days=15)
            Prestamo.objects.get_or_create(
                libro=libro1,
                usuario=estudiante_user,
                defaults={
                    "fecha_devolucion_esperada": fecha_devolucion,
                    "devuelto": False,
                }
            )
            libro1.disponible = False
            libro1.save()
            self.stdout.write(f"Préstamo creado para estudiante1 con {libro1.titulo}")

        # Préstamo de estudiante 2
        if libro2 and libro2.disponible:
            fecha_devolucion = timezone.now().date() + timedelta(days=15)
            Prestamo.objects.get_or_create(
                libro=libro2,
                usuario=User.objects.get(username="estudiante2"),
                defaults={
                    "fecha_devolucion_esperada": fecha_devolucion,
                    "devuelto": False,
                }
            )
            libro2.disponible = False
            libro2.save()
            self.stdout.write(f"Préstamo creado para estudiante2 con {libro2.titulo}")

        self.stdout.write(self.style.SUCCESS("¡Datos de demostración poblados exitosamente!"))