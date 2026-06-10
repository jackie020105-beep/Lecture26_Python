from Book.book import Book

class CartItem:
    def __init__(self, cartItemId, cartId, book, quantity):
        self.__cartItemId = cartItemId
        self.__cartId = cartId
        self.__book = book
        self.__quantity = quantity

    def get_cartItemId(self):
        return self.__cartItemId

    def get_cartId(self):
        return self.__cartId

    def get_book(self):
        return self.__book

    def get_quantity(self):
        return self.__quantity

    def set_cartItemId(self, cartItemId):
        self.__cartItemId = cartItemId

    def set_cartId(self, cartId):
        self.__cartId = cartId

    def set_book(self, book):
        self.__book = book

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def add_quantity(self, quantity=1):
        self.__quantity += quantity

    def get_subtotal(self):
        return self.__book.get_price() * self.__quantity

    def __str__(self):
        return (f'장바구니상품번호 : {self.__cartItemId} | 책번호 : {self.__book.get_bookId()} | '
                f'제목 : {self.__book.get_title()} | 저자 : {self.__book.get_author()} | '
                f'가격 : {self.__book.get_price()}원 | 수량 : {self.__quantity} | '
                f'소계 : {self.get_subtotal()}원')
