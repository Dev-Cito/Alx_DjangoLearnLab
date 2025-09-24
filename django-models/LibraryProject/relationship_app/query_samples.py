import os
import django

# Set up the Django environment (Needed if running as a standalone script)
# NOTE: This assumes 'LibraryProject.settings' is your correct settings module path.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings') 
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Creates sample data to test the queries."""
    print("--- Creating Sample Data ---")
    
    # 1. Authors
    author_a, _ = Author.objects.get_or_create(name='Jane Austen')
    author_b, _ = Author.objects.get_or_create(name='George Orwell')

    # 2. Books
    book1, _ = Book.objects.get_or_create(title='Pride and Prejudice', author=author_a)
    book2, _ = Book.objects.get_or_create(title='Sense and Sensibility', author=author_a)
    book3, _ = Book.objects.get_or_create(title='1984', author=author_b)
    book4, _ = Book.objects.get_or_create(title='Animal Farm', author=author_b)

    # 3. Libraries
    lib_main, _ = Library.objects.get_or_create(name='Main City Library')
    lib_branch, _ = Library.objects.get_or_create(name='Suburban Branch')

    # 4. ManyToMany relationship (Library <-> Books)
    lib_main.books.set([book1, book3, book4])
    lib_branch.books.set([book2, book3])

    # 5. Librarian (OneToOne relationship to Library)
    Librarian.objects.get_or_create(name='Alice Smith', library=lib_main)
    Librarian.objects.get_or_create(name='Bob Johnson', library=lib_branch)
    
    print("Sample data created successfully.\n")
    return author_a, lib_main

def run_sample_queries(author_a, library_main):
    """Executes the relationship queries."""
    print("--- Running Sample Queries ---")

    # 1. Query all books by a specific author (ForeignKey reverse lookup)
    print("\n[ForeignKey Query] Query all books by Jane Austen:")
    # We use the related_name='books' defined on the Author model
    jane_austen_books = author_a.books.all()
    for book in jane_austen_books:
        print(f"  - {book.title}")

    # 2. List all books in a library (ManyToManyField)
    print("\n[ManyToManyField Query] List all books in Main City Library:")
    # We use the 'books' attribute defined on the Library model
    main_library_books = library_main.books.all()
    for book in main_library_books:
        print(f"  - {book.title} (by {book.author.name})")

    # 3. Retrieve the librarian for a library (OneToOneField reverse lookup)
    print("\n[OneToOneField Query] Retrieve the librarian for Main City Library:")
    # We can access the related Librarian object directly using the model's lowercase name
    try:
        librarian = library_main.librarian
        print(f"  - Librarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print("  - No librarian found.")

if __name__ == '__main__':
    # Clean up old data to ensure a fresh run
    Author.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()

    author_a, lib_main = create_sample_data()
    run_sample_queries(author_a, lib_main)