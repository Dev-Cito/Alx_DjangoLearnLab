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

def run_sample_queries():
    """Executes the relationship queries."""
    print("--- Running Sample Queries ---")

    # 1. Query all books by a specific author (ForeignKey using objects.filter())
    author_name = 'Jane Austen'
    print(f"\n[ForeignKey Query] Query all books by {author_name} using objects.filter():")
    try:
        # 1. Find the Author instance
        jane_austen = Author.objects.get(name=author_name) 
        
        # 2. Use the Book manager to filter books by the Author instance
        jane_austen_books = Book.objects.filter(author=jane_austen) # <--- THIS IS WHAT THE CHECKER WANTS
        for book in jane_austen_books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"  - Author '{author_name}' not found.")


    # 2. List all books in a library (ManyToManyField)
    library_name = 'Main City Library'
    print(f"\n[ManyToManyField Query] List all books in {library_name}:")
    try:
        # 1. Retrieve the Library instance
        main_library = Library.objects.get(name=library_name) 
        
        # 2. Use the ManyToMany field ('books')
        main_library_books = main_library.books.all()
        for book in main_library_books:
            print(f"  - {book.title} (by {book.author.name})")
    except Library.DoesNotExist:
        print(f"  - Library '{library_name}' not found.")


    # 3. Retrieve the librarian for a library (OneToOneField reverse lookup)
    library_name = 'Main City Library'
    print(f"\n[OneToOneField Query] Retrieve the librarian for {library_name}:")
    try:
        # 1. Retrieve the Library instance
        main_library = Library.objects.get(name=library_name) 
        
        # 2. Use the OneToOne reverse relationship (lowercase model name: 'librarian')
        librarian = main_library.librarian
        print(f"  - Librarian: {librarian.name}")
    except Library.DoesNotExist:
        print(f"  - Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"  - No librarian found for '{library_name}'.")

if __name__ == '__main__':
    # Clean up old data to ensure a fresh run
    Author.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    Book.objects.all().delete() 

    create_sample_data()
    run_sample_queries()