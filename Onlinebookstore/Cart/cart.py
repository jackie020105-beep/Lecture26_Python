from Book.book import Book
 
class Cart:
    def __init__(self, cartId, cartItems):
        self.__cartId = cartId
        self.__cartItems = cartItems
 
    def get_cartId(self):
        return self.__cartId
    def get_cartItems(self):
        return self.__cartItems
 
    def set_cartId(self, cartId):
        self.__cartId = cartId
    def set_cartItems(self, cartItems):
        self.__cartItems = cartItems
 
    def __str__(self):
        if not self.__cartItems:
            return f'장바구니번호 : {self.__cartId} 책 : []'
        result = f'장바구니번호 : {self.__cartId}\n'
        for book in self.__cartItems:
            result += (f'책번호 : {book.get_bookId()} | 제목 : {book.get_title()} | 저자 : {book.get_author()} | 가격 : {book.get_price()}원')
        return result
 
 
if __name__ == '__main__':
    c = Cart('111111', [])
    c.get_cartItems().append(Book('1', '축구의 이해', '정원재', 10000, 5))
    print(c)
    print(c.get_cartId())
