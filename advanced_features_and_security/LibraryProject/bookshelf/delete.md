from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Output:
# (1, {'bookshelf.Book': 1})
# <QuerySet []>
