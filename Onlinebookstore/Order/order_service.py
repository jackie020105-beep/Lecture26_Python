from .order import Order
from .order_item import OrderItem

class OrderService:
    orderId_seq = 111111
    orderItemId_seq = 1

    def __init__(self, order_dao, order_item_dao, cart_service, delivery_service):
        self.__dao = order_dao
        self.__orderItemDAO = order_item_dao
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

        orderItems = []
        totalPrice = 0
        for cart_item in cart.get_cartItems():
            book = cart_item.get_book()
            quantity = cart_item.get_quantity()

            # 주문 직전에 재고를 한 번 더 확인한다.
            if quantity > book.get_stock():
                return 'STOCK_ERROR'

            price = book.get_price()
            orderItemId = 'OI' + str(OrderService.orderItemId_seq)
            OrderService.orderItemId_seq += 1

            order_item = OrderItem(orderItemId, orderId, book, quantity, price)
            orderItems.append(order_item)
            totalPrice += order_item.get_subtotal()

        order = Order(orderId, memberId, orderItems, totalPrice, address, '주문완료')
        if self.__dao.insert_order(order):
            for order_item in orderItems:
                self.__orderItemDAO.insert_order_item(order_item)

                # 주문이 완료되면 주문한 수량만큼 도서 재고를 감소시킨다.
                book = order_item.get_book()
                book.set_stock(book.get_stock() - order_item.get_quantity())

            self.__cartService.clear_cart(memberId)
            self.__deliveryService.create_delivery(orderId, memberId, address)
            return True
        else:
            return False

    def get_order_detail(self, orderId):
        order = self.__dao.select_order_by_id(orderId)
        if order:
            order_items = self.__orderItemDAO.select_order_items_by_order(orderId)
            order.set_orderItems(order_items)
        return order

    def get_member_orders(self, memberId):
        orders = self.__dao.select_order_by_member(memberId)
        if orders:
            for order in orders:
                order_items = self.__orderItemDAO.select_order_items_by_order(order.get_orderId())
                order.set_orderItems(order_items)
        return orders

    def get_all_orders(self):
        orders = self.__dao.select_all_orders()
        if orders:
            for order in orders:
                order_items = self.__orderItemDAO.select_order_items_by_order(order.get_orderId())
                order.set_orderItems(order_items)
        return orders

    def cancel_order(self, orderId):
        order = self.__dao.select_order_by_id(orderId)
        if order:
            order.set_status('주문취소')
            return self.__dao.update_order(orderId, order)
        else:
            return False
