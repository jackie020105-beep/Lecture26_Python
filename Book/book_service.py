from .book import Book

class BookService:
    bookId_seq = 1
    def __init__(self, book_dao):
        self.__dao = book_dao



    def get_all_books(self):
        return self.__dao.select_all_books()
            
    def get_book_detail(self, bookId):
        return self.__dao.select_book_by_id(bookId)



    def add_book(self, title, author, price, stock):
        add_new_book = Book(str(BookService.bookId_seq), title, author, price, stock)
        BookService.bookId_seq += 1
        return self.__dao.insert_book(add_new_book)

    def edit_book(self, bookId, book):
        editing = self.__dao.select_book_by_id(bookId)
        if editing:
            return self.__dao.update_book(bookId, book)
        return False

    def remove_book(self, bookId):
        return self.__dao.delete_book(bookId)