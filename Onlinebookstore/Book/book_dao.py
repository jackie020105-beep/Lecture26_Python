from .book import Book

class BookDAO:
    def __init__(self):
        self.__BookDB = {} # 책번호 : Book 객체

    def insert_book(self, book):
        bookId = book.get_bookId()
        if not self.select_book_by_id(bookId):
            self.__BookDB[bookId] = book
            return True
        else:
            return False

    def select_book_by_id(self, bookId):
        if bookId in self.__BookDB:
            return self.__BookDB[bookId]
        else:
            return None

    def select_all_books(self):
        Book_list = list(self.__BookDB.values())
        if len(Book_list):
            return Book_list
        else:
            return None

    def update_book(self, bookId, book):
        if bookId in self.__BookDB:
            self.__BookDB[bookId] = book
            return True
        else:
            return False
        
    def update_stock(self, bookId, stock):
        if bookId in self.__BookDB:
            self.__BookDB[bookId].set_stock(stock)
            return True
        else:
            return False

    def delete_book(self, bookId):
        if bookId in self.__BookDB:
            self.__BookDB.pop(bookId)
            return True
        else:
            return False

# 테스트
if __name__ == '__main__':
    dao = BookDAO()
    bk_list = dao.select_all_books()
    print(bk_list)
    print()

    # insert_book
    dao.insert_book(Book('1','축구의 이해','정원재',10000,0))
    dao.insert_book(Book('2','농구의 정석','전민수',20000,0))

    # select_all_books
    for book in dao.select_all_books():
        print(book)
    print()

    # select_book_by_id
    print(dao.select_book_by_id('2'))
    print()
    
    # update_book
    dao.update_book('1', Book('1', '축구의 이해', '정원재', 30000, 0))
    print(dao.select_book_by_id('1'))
    print()

    # update_stock
    dao.update_stock('1', 2)
    print(dao.select_book_by_id('1'))
    print()

    # delete_book
    dao.delete_book('2')
    print(bk_list)
    for book in dao.select_all_books():
        print(book)