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
        for cart_item in self.__cartItems:
            result += str(cart_item) + '\n'
        return result
