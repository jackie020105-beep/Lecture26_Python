from .order_entity import Order
from LP.lp_entity import LP


class OrderService:
    orderId_seq = 1

    def __init__(self, order_dao, wishlist_service, lp_service, member_service):
        self.__DAO = order_dao
        self.__WishlistService = wishlist_service
        self.__LpService = lp_service
        self.__MemberService = member_service
        self.__sync_sequence()

    def __sync_sequence(self):
        orders = self.__DAO.select_all_orders()
        max_no = 0
        if orders:
            for order in orders:
                try:
                    max_no = max(max_no, int(order.get_orderId().replace('O', '')))
                except ValueError:
                    pass
        OrderService.orderId_seq = max_no + 1

    def __new_order_id(self):
        order_id = f'O{OrderService.orderId_seq:06d}'
        OrderService.orderId_seq += 1
        return order_id

    def place_order(self, memberId, lpId, address):
        member = self.__MemberService.view_member_info(memberId)
        lp = self.__LpService.get_lp_detail(lpId)
        if not member:
            return 'LOGIN_ERROR'
        if not lp:
            return False
        if lp.get_sellerId() == memberId:
            return 'SELF_ITEM_ERROR'
        if lp.get_status() != LP.STATUS_ON_SALE:
            return 'SOLD_ERROR'
        if not address.strip():
            return 'ADDRESS_ERROR'

        price = lp.get_price()
        deliveryprice = lp.get_deliveryprice()
        totalprice = price + deliveryprice
        order = Order(self.__new_order_id(), memberId, lpId, price, deliveryprice, totalprice, address, Order.STATUS_ORDERED, '')
        if self.__DAO.insert_order(order):
            self.__LpService.mark_as_sold(lpId)
            self.__WishlistService.remove_lp_from_all(lpId)
            return True
        return False

    def get_order_detail(self, orderId):
        return self.__DAO.select_order_by_id(orderId)

    def get_orders_by_member(self, memberId):
        orders = self.__DAO.select_orders_by_member(memberId)
        if not orders:
            return None
        return sorted(orders, key=lambda order: order.get_orderId())

    def get_all_orders(self):
        orders = self.__DAO.select_all_orders()
        if not orders:
            return None
        return sorted(orders, key=lambda order: order.get_orderId())

    def get_order_by_lp(self, lpId):
        return self.__DAO.select_order_by_lp(lpId)

    def get_seller_orders(self, sellerId):
        orders = self.__DAO.select_all_orders()
        if not orders:
            return None
        result = []
        for order in orders:
            lp = self.__LpService.get_lp_detail(order.get_lpId())
            if lp and lp.get_sellerId() == sellerId:
                result.append(order)
        return sorted(result, key=lambda order: order.get_orderId()) if result else None

    def get_buyer_of_lp(self, lpId):
        order = self.__DAO.select_order_by_lp(lpId)
        if not order:
            return None
        return self.__MemberService.view_member_info(order.get_memberId())

    def change_delivery_status(self, orderId, sellerId, status, trackingNo=None):
        order = self.__DAO.select_order_by_id(orderId)
        if not order:
            return False
        lp = self.__LpService.get_lp_detail(order.get_lpId())
        if not lp or lp.get_sellerId() != sellerId:
            return 'AUTH_ERROR'
        if order.get_status() == Order.STATUS_CANCEL_REQUEST:
            return 'CANCEL_REQUEST_ERROR'
        if order.get_status() == Order.STATUS_CANCELLED:
            return 'CANCELLED_ERROR'
        if status not in [Order.STATUS_PREPARING, Order.STATUS_SHIPPING, Order.STATUS_DELIVERED]:
            return 'STATUS_ERROR'
        if status == Order.STATUS_SHIPPING and not trackingNo:
            return 'TRACKING_ERROR'
        order.set_status(status)
        if trackingNo:
            order.set_trackingNo(trackingNo)
        return self.__DAO.update_order(orderId, order)

    def request_cancel(self, orderId, memberId):
        order = self.__DAO.select_order_by_id(orderId)
        if not order:
            return False
        if order.get_memberId() != memberId:
            return 'AUTH_ERROR'
        if order.get_status() in [Order.STATUS_DELIVERED, Order.STATUS_CANCELLED]:
            return 'STATUS_ERROR'
        order.set_status(Order.STATUS_CANCEL_REQUEST)
        return self.__DAO.update_order(orderId, order)

    def approve_cancel(self, orderId, sellerId=None):
        order = self.__DAO.select_order_by_id(orderId)
        if not order:
            return False
        lp = self.__LpService.get_lp_detail(order.get_lpId())
        if sellerId and lp and lp.get_sellerId() != sellerId:
            return 'AUTH_ERROR'
        if order.get_status() != Order.STATUS_CANCEL_REQUEST:
            return 'STATUS_ERROR'
        order.set_status(Order.STATUS_CANCELLED)
        order.set_trackingNo('')
        self.__DAO.update_order(orderId, order)
        self.__LpService.mark_as_sale(order.get_lpId())
        return True

    def reject_cancel(self, orderId, sellerId=None):
        order = self.__DAO.select_order_by_id(orderId)
        if not order:
            return False
        lp = self.__LpService.get_lp_detail(order.get_lpId())
        if sellerId and lp and lp.get_sellerId() != sellerId:
            return 'AUTH_ERROR'
        if order.get_status() != Order.STATUS_CANCEL_REQUEST:
            return 'STATUS_ERROR'
        order.set_status(Order.STATUS_ORDERED)
        return self.__DAO.update_order(orderId, order)

    def cancel_order(self, orderId):
        order = self.__DAO.select_order_by_id(orderId)
        if not order:
            return False
        order.set_status(Order.STATUS_CANCELLED)
        self.__DAO.update_order(orderId, order)
        self.__LpService.mark_as_sale(order.get_lpId())
        return True


# 클래스 다이어그램 명칭과의 호환용 별칭
Order_Service = OrderService
