class CartItemDAO:
    def __init__(self):
        self.__cartItemDB = {} # 장바구니상품번호 : CartItem 객체

    def insert_cart_item(self, cart_item):
        cartItemId = cart_item.get_cartItemId()
        if cartItemId not in self.__cartItemDB:
            self.__cartItemDB[cartItemId] = cart_item
            return True
        return False

    def select_cart_item_by_id(self, cartItemId):
        return self.__cartItemDB.get(cartItemId)

    def select_cart_items_by_cart(self, cartId):
        result = []
        for cart_item in self.__cartItemDB.values():
            if cart_item.get_cartId() == cartId:
                result.append(cart_item)
        return result

    def select_cart_item_by_cart_and_book(self, cartId, bookId):
        for cart_item in self.__cartItemDB.values():
            if cart_item.get_cartId() == cartId and cart_item.get_book().get_bookId() == bookId:
                return cart_item
        return None

    def update_cart_item(self, cartItemId, cart_item):
        if cartItemId in self.__cartItemDB:
            self.__cartItemDB[cartItemId] = cart_item
            return True
        return False

    def delete_cart_item(self, cartItemId):
        if cartItemId in self.__cartItemDB:
            self.__cartItemDB.pop(cartItemId)
            return True
        return False

    def delete_cart_items_by_cart(self, cartId):
        delete_ids = []
        for cartItemId, cart_item in self.__cartItemDB.items():
            if cart_item.get_cartId() == cartId:
                delete_ids.append(cartItemId)
        for cartItemId in delete_ids:
            self.__cartItemDB.pop(cartItemId)
        return True
