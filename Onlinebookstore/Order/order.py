class Order:
    def __init__(self, orderId, memberId, orderItems, totalPrice, address, status):
        self.__orderId = orderId
        self.__memberId = memberId
        self.__orderItems = orderItems
        self.__totalPrice = totalPrice
        self.__address = address
        self.__status = status

    def get_orderId(self):
        return self.__orderId
    def get_memberId(self):
        return self.__memberId
    def get_orderItems(self):
        return self.__orderItems
    def get_totalPrice(self):
        return self.__totalPrice
    def get_address(self):
        return self.__address
    def get_status(self):
        return self.__status

    def set_orderId(self, orderId):
        self.__orderId = orderId
    def set_memberId(self, memberId):
        self.__memberId = memberId
    def set_orderItems(self, orderItems):
        self.__orderItems = orderItems
    def set_totalPrice(self, totalPrice):
        self.__totalPrice = totalPrice
    def set_address(self, address):
        self.__address = address
    def set_status(self, status):
        self.__status = status

    def __str__(self):
        item_info = []
        for order_item in self.__orderItems:
            item_info.append(f'{order_item.get_book().get_title()} {order_item.get_quantity()}권')
        return f'주문번호 : {self.__orderId} 회원아이디 : {self.__memberId} 책 : {item_info} 총금액 : {self.__totalPrice} 주소 : {self.__address} 주문상태 : {self.__status}'
