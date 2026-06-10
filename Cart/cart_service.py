from .cart import Cart
from .cart_dao import CartDAO
from Book.book_service import BookService
 
class CartService:
    cartId_seq = 111111
    def __init__(self, cart_dao, book_service):
        self.__dao = cart_dao
        self.__bookService = book_service
 
    def view_cart(self, memberId):
        return self.__dao.select_cart_by_member(memberId)
 
    def add_item(self, memberId, bookId):
        book = self.__bookService.get_book_detail(bookId)
        if not book:
            return False
        cart = self.__dao.select_cart_by_member(memberId)
        if cart is None:
            cart = Cart(str(CartService.cartId_seq), [])
            CartService.cartId_seq += 1
            cart.get_cartItems().append(book)
            return self.__dao.insert_cart(memberId, cart)
        cart.get_cartItems().append(book)
        return self.__dao.update_cart(memberId, cart)
 
    def remove_item(self, memberId, bookId):
        cart = self.__dao.select_cart_by_member(memberId)
        if cart:
            items = cart.get_cartItems()
            for book in items:
                if book.get_bookId() == bookId:
                    items.remove(book)
                    if len(items) == 0:
                        return self.__dao.delete_cart(memberId)
                    return self.__dao.update_cart(memberId, cart)
        return False
 
    def clear_cart(self, memberId):
        return self.__dao.delete_cart(memberId)

# 테스트
if __name__ == '__main__':
    from Book.book_dao import BookDAO
 
    book_dao = BookDAO()
    book_service = BookService(book_dao)
    book_service.add_book('축구의 이해', '정원재', 10000, 5)
    book_service.add_book('농구의 정석', '전민수', 20000, 3)
 
    cart_service = CartService(CartDAO(), book_service)
 
    cart_service.add_item('member_1', '1')
    cart_service.add_item('member_1', '2')
    print(cart_service.view_cart('member_1'))
 
    cart_service.remove_item('member_1', '1')
    print(cart_service.view_cart('member_1'))
 
    cart_service.clear_cart('member_1')
    print(cart_service.view_cart('member_1'))
