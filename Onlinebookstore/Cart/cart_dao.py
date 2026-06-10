from .cart import Cart
from Book.book import Book
 
class CartDAO:
    def __init__(self):
        self.__cartDB = {} # 회원아이디 : Cart 객체

    def insert_cart(self, memberId, cart):
        if not self.select_cart_by_member(memberId):
            self.__cartDB[memberId] = cart
            return True
        else:
            return False
 
    def select_cart_by_member(self, memberId):
        if memberId in self.__cartDB:
            return self.__cartDB[memberId]
        else:
            return None
 
    def update_cart(self, memberId, cart):
        if memberId in self.__cartDB:
            self.__cartDB[memberId] = cart
            return True
        else:
            return False
 
    def delete_cart(self, memberId):
        if memberId in self.__cartDB:
            self.__cartDB.pop(memberId)
            return True
        else:
            return False

# 테스트
if __name__ == '__main__':
    dao = CartDAO()

    cart1 = Cart('111111', [])
    cart1.get_cartItems().append(Book('1', '축구의 이해', '정원재', 10000, 5))
    cart1.get_cartItems().append(Book('2', '농구의 정석', '전민수', 20000, 3))

    print(dao.insert_cart('member_1', cart1))
    print(dao.select_cart_by_member('member_1'))
    print()

    cart1_updated = Cart('111111', [])
    cart1_updated.get_cartItems().append(Book('3', '야구의 모든 것', '김철수', 15000, 2))
    print(dao.update_cart('member_1', cart1_updated))
    print(dao.select_cart_by_member('member_1'))
    print()

    print(dao.delete_cart('member_1'))
    print(dao.select_cart_by_member('member_1'))
