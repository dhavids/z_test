class LibraryBook:
    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
        self.borrower = None

    def borrow_book(self, borrower_name):
        if self.available:
            self.available = False
            self.borrower = borrower_name
            print(f"{self.title} has been borrowed by {borrower_name}.")
        else:
            print(f"{self.title} is currently unavailable.")

    def return_book(self):
        if not self.available:
            self.available = True
            borrower = self.borrower
            self.borrower = None
            print(f"{self.title} has been returned by {borrower}.")
        else:
            print(f"{self.title} was not borrowed.")

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrower}"
        return f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nStatus: {status}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"{book.title} added to the library.")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def display_available_books(self):
        available_books = [book for book in self.books if book.available]
        if available_books:
            for book in available_books:
                print(book)
        else:
            print("No books available at the moment.")

book1 = LibraryBook("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "9780345391803")
book2 = LibraryBook("Pride and Prejudice", "Jane Austen", "9780141439518")

my_library = Library()

my_library.add_book(book1)
my_library.add_book(book2)

my_library.display_available_books()
book_to_borrow = my_library.find_book("The Hitchhiker's Guide to the Galaxy")
if book_to_borrow:
    book_to_borrow.borrow_book("John Doe")
my_library.display_available_books()
book_to_borrow.return_book()
my_library.display_available_books()


class LibraryBook:
    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def checkout(self):
        if self.available:
            self.available = False
            print(f"Book '{self.title}' checked out successfully.")
        else:
            print(f"Book '{self.title}' is not available at this time.")

    def return_book(self):
        self.available = True
        print(f"Book '{self.title}' returned successfully.")

    def __str__(self):
        availability = "Available" if self.available else "Checked Out"
        return f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nStatus: {availability}"

# Create book objects
book1 = LibraryBook("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "9780345391803")
book2 = LibraryBook("Pride and Prejudice", "Jane Austen", "9780141439518")

# Check out and return books
print(book1)  # Display book1 details
book1.checkout()
print(book1)
book1.return_book()
print(book1)

print(book2)
book2.checkout()
print(book2)
