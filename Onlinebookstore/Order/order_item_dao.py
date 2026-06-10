class OrderItemDAO:
    def __init__(self):
        self.__orderItemDB = {} # 주문상품번호 : OrderItem 객체

    def insert_order_item(self, order_item):
        orderItemId = order_item.get_orderItemId()
        if orderItemId not in self.__orderItemDB:
            self.__orderItemDB[orderItemId] = order_item
            return True
        return False

    def select_order_item_by_id(self, orderItemId):
        return self.__orderItemDB.get(orderItemId)

    def select_order_items_by_order(self, orderId):
        result = []
        for order_item in self.__orderItemDB.values():
            if order_item.get_orderId() == orderId:
                result.append(order_item)
        return result

    def update_order_item(self, orderItemId, order_item):
        if orderItemId in self.__orderItemDB:
            self.__orderItemDB[orderItemId] = order_item
            return True
        return False

    def delete_order_item(self, orderItemId):
        if orderItemId in self.__orderItemDB:
            self.__orderItemDB.pop(orderItemId)
            return True
        return False

    def delete_order_items_by_order(self, orderId):
        delete_ids = []
        for orderItemId, order_item in self.__orderItemDB.items():
            if order_item.get_orderId() == orderId:
                delete_ids.append(orderItemId)
        for orderItemId in delete_ids:
            self.__orderItemDB.pop(orderItemId)
        return True
