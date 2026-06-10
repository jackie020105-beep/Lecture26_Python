class OrderDAO:
    def __init__(self):
        self.__orderDB = {}

    def insert_order(self, order):
        orderId = order.get_orderId()
        if not self.select_order_by_id(orderId):
            self.__orderDB[orderId] = order
            return True
        else:
            return False

    def select_order_by_id(self, orderId):
        if orderId in self.__orderDB:
            return self.__orderDB[orderId]
        else:
            return None

    def select_order_by_member(self, memberId):
        result = []
        for order in self.__orderDB.values():
            if order.get_memberId() == memberId:
                result.append(order)
        if len(result):
            return result
        else:
            return None

    def select_all_orders(self):
        order_list = list(self.__orderDB.values())
        if len(order_list):
            return order_list
        else:
            return None

    def update_order(self, orderId, order):
        if orderId in self.__orderDB:
            self.__orderDB[orderId] = order
            return True
        else:
            return False

    def delete_order(self, orderId):
        if orderId in self.__orderDB:
            self.__orderDB.pop(orderId)
            return True
        else:
            return False
