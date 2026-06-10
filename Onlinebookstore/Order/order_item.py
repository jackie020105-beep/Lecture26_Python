class OrderItem:
    def __init__(self, orderItemId, orderId, book, quantity, price):
        self.__orderItemId = orderItemId
        self.__orderId = orderId
        self.__book = book
        self.__quantity = quantity
        self.__price = price

    def get_orderItemId(self):
        return self.__orderItemId

    def get_orderId(self):
        return self.__orderId

    def get_book(self):
        return self.__book

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def set_orderItemId(self, orderItemId):
        self.__orderItemId = orderItemId

    def set_orderId(self, orderId):
        self.__orderId = orderId

    def set_book(self, book):
        self.__book = book

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, price):
        self.__price = price

    def get_subtotal(self):
        return self.__price * self.__quantity

    def __str__(self):
        return (f'주문상품번호 : {self.__orderItemId} | 책번호 : {self.__book.get_bookId()} | '
                f'제목 : {self.__book.get_title()} | 가격 : {self.__price}원 | '
                f'수량 : {self.__quantity} | 소계 : {self.get_subtotal()}원')
