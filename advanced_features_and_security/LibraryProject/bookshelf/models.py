from django.db import models

# Create your models here.


class Book(models.Model):
    """
    Represents a book in the library.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """
        String representation of the Book model.
        """
        return f"{self.title} by {self.author} ({self.publication_year})"



from django.contrib import admin
from .models import Book   # ✅ Import the Book model

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # ✅ fields to show
    search_fields = ('title', 'author')                     # ✅ search box
    list_filter = ('publication_year',)                     # ✅ filter sidebar

# LibraryProject/bookshelf/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
