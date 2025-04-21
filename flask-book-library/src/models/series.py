class Series:
    def __init__(self, id, title, description=None):
        self.id = id
        self.title = title
        self.description = description
        self.books = []

    def add_book(self, book):
        self.books.append(book)