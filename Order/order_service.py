from .order import Order

class OrderService:
    orderId_seq = 111111

    def __init__(self, order_dao, cart_service, delivery_service):
        self.__dao = order_dao
        self.__cartService = cart_service
        self.__deliveryService = delivery_service

    def get_member_address(self, memberId):
        orders = self.__dao.select_order_by_member(memberId)
        if orders:
            return orders[0].get_address()
        else:
            return None

    def order_cart(self, memberId, address=None):
        cart = self.__cartService.view_cart(memberId)
        if not cart or not cart.get_cartItems():
            return False

        saved_address = self.get_member_address(memberId)
        if saved_address:
            address = saved_address
        elif not address:
            return False

        orderId = 'O' + str(OrderService.orderId_seq)
        OrderService.orderId_seq += 1
        orderItems = list(cart.get_cartItems())
        totalPrice = 0
        for book in orderItems:
            totalPrice += book.get_price()

        order = Order(orderId, memberId, orderItems, totalPrice, address, '주문완료')
        if self.__dao.insert_order(order):
            self.__cartService.clear_cart(memberId)
            self.__deliveryService.create_delivery(orderId, memberId, address)
            return True
        else:
            return False

    def get_order_detail(self, orderId):
        return self.__dao.select_order_by_id(orderId)

    def get_member_orders(self, memberId):
        return self.__dao.select_order_by_member(memberId)

    def get_all_orders(self):
        return self.__dao.select_all_orders()

    def cancel_order(self, orderId):
        order = self.__dao.select_order_by_id(orderId)
        if order:
            order.set_status('주문취소')
            return self.__dao.update_order(orderId, order)
        else:
            return False
