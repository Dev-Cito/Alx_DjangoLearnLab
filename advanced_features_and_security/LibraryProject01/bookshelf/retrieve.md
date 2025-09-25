from bookshelf.models import Book

# Retrieve the book we created
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# Output:
# ('1984', 'George Orwell', 1949)
