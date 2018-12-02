from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    """
    Modelo que representa un genero literario(p- ej. ciencia ficción, poesía, etc).
    """
    name = models.CharField(max_length=200, help_text="Ingresa un genero de libro (e.g. Ciencia ficción, French Poetry etc)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej en el sitio de Administración)
        :return:
        """
        return self.name

class Book(models.Model):
    """
    Modelo que representa un libro (pero no un ejemplar específico).
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    #ForeignKey, ya que in libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    #'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")

    isbn = models.CharField("ISBN", max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        """
        String que representa al objecto Nook
        :return:
        """
        return self.title

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        :return:
        """
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """
        Creaste un string para el genre. Esto se requiere para mostrar el genre en Admin
        :return:
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que pueda ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda"
                                                                          " la biblioteca")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="m", help_text="Disponibilidad de Libro")

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String para representar el Objecto del Modelo
        :return:
        """
        return "%s, %s, %s, %s" % (self.book, self.status, self.due_back, self.id)
class Author(models.Model):
    """
    Modelo que representa a un Autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor
        :return:
        """
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):

        return "%s, %s" % (self.last_name, self.first_name)

from datetime import date
@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False


