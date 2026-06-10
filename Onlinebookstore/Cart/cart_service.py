from .cart import Cart
from .cart_item import CartItem

class CartService:
    cartId_seq = 111111
    cartItemId_seq = 1

    def __init__(self, cart_dao, cart_item_dao, book_service):
        self.__dao = cart_dao
        self.__cartItemDAO = cart_item_dao
        self.__bookService = book_service
 
    def view_cart(self, memberId):
        cart = self.__dao.select_cart_by_member(memberId)
        if cart:
            cart_items = self.__cartItemDAO.select_cart_items_by_cart(cart.get_cartId())
            cart.set_cartItems(cart_items)
        return cart
 
    def add_item(self, memberId, bookId, quantity):
        if quantity <= 0:
            return 'QUANTITY_ERROR'

        book = self.__bookService.get_book_detail(bookId)
        if not book:
            return False

        cart = self.__dao.select_cart_by_member(memberId)
        cart_item = None
        current_quantity = 0
        if cart:
            cart_item = self.__cartItemDAO.select_cart_item_by_cart_and_book(cart.get_cartId(), bookId)
            if cart_item:
                current_quantity = cart_item.get_quantity()

        if current_quantity + quantity > book.get_stock():
            return 'STOCK_ERROR'

        if cart is None:
            cart = Cart('C' + str(CartService.cartId_seq), [])
            CartService.cartId_seq += 1
            if not self.__dao.insert_cart(memberId, cart):
                return False

        if cart_item:
            cart_item.add_quantity(quantity)
            return self.__cartItemDAO.update_cart_item(cart_item.get_cartItemId(), cart_item)

        cartItemId = 'CI' + str(CartService.cartItemId_seq)
        CartService.cartItemId_seq += 1
        cart_item = CartItem(cartItemId, cart.get_cartId(), book, quantity)
        return self.__cartItemDAO.insert_cart_item(cart_item)
 
    def remove_item(self, memberId, bookId, quantity):
        if quantity <= 0:
            return 'QUANTITY_ERROR'

        cart = self.__dao.select_cart_by_member(memberId)
        if cart:
            cart_item = self.__cartItemDAO.select_cart_item_by_cart_and_book(cart.get_cartId(), bookId)
            if cart_item:
                if quantity > cart_item.get_quantity():
                    return 'QUANTITY_ERROR'

                if quantity < cart_item.get_quantity():
                    cart_item.set_quantity(cart_item.get_quantity() - quantity)
                    return self.__cartItemDAO.update_cart_item(cart_item.get_cartItemId(), cart_item)

                self.__cartItemDAO.delete_cart_item(cart_item.get_cartItemId())
                remaining_items = self.__cartItemDAO.select_cart_items_by_cart(cart.get_cartId())
                if len(remaining_items) == 0:
                    return self.__dao.delete_cart(memberId)
                return True
        return False
 
    def clear_cart(self, memberId):
        cart = self.__dao.select_cart_by_member(memberId)
        if cart:
            self.__cartItemDAO.delete_cart_items_by_cart(cart.get_cartId())
        return self.__dao.delete_cart(memberId)
