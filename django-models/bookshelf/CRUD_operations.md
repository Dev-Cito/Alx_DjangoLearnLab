create.md
from bookshelf.models import Book

# Create a book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
book
# Output:
# <Book: 1984 by George Orwell (1949)>



retrieve.md
from bookshelf.models import Book

# Retrieve the book we created
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# Output:
# ('1984', 'George Orwell', 1949)


update.md
from bookshelf.models import Book

# Update the title of the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# Output:
# 'Nineteen Eighty-Four'





delete.md
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Output:
# (1, {'bookshelf.Book': 1})
# <QuerySet []>