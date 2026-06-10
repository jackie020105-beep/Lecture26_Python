# from account import Account, AccountDAO, AccountService

class Book:
    def __init__(self, bookId, title, author, price, stock):
        self.__bookId = bookId
        self.__title = title
        self.__author = author
        self.__price = price
        self.__stock = stock

    def get_bookId(self):
        return self.__bookId
    def get_title(self):
        return self.__title
    def get_author(self):
        return self.__author
    def get_price(self):
        return self.__price
    def get_stock(self):
        return self.__stock
    
    def set_bookId(self, bookId):
        self.__bookId = bookId
    def set_stock(self, stock):
        self.__stock = stock

    def get_list_info(self):
        return f'책번호: {self.__bookId} 제목 : {self.__title} 저자 : {self.__author}'

    def __str__(self):
        return f'책번호 : {self.__bookId} 제목 : {self.__title} 저자 : {self.__author} 가격 : {self.__price} 재고 : {self.__stock}'
    
if __name__ == '__main__':
    bk = Book('1','축구의 이해','정원재',10000,0)
    print(bk)
    bk.set_stock(2)
    print(bk)
    print(bk.get_bookId())