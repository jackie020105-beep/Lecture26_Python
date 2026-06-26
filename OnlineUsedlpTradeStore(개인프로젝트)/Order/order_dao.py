import pickle
from pathlib import Path


class OrderDAO:
    def __init__(self):
        self.__file_path = Path(__file__).resolve().parents[1] / 'Data' / 'orderDB.obj'
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)
        self.__orderDB = self.__load()

    def __load(self):
        if self.__file_path.exists():
            try:
                with open(self.__file_path, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                return {}
        return {}

    def __save(self):
        with open(self.__file_path, 'wb') as f:
            pickle.dump(self.__orderDB, f)

    def insert_order(self, order):
        orderId = order.get_orderId()
        if not self.select_order_by_id(orderId):
            self.__orderDB[orderId] = order
            self.__save()
            return True
        return False

    def select_order_by_id(self, orderId):
        return self.__orderDB.get(orderId)

    def select_orders_by_member(self, memberId):
        result = [order for order in self.__orderDB.values() if order.get_memberId() == memberId]
        return result if result else None

    def select_order_by_lp(self, lpId):
        for order in self.__orderDB.values():
            if order.get_lpId() == lpId and order.get_status() != '주문취소':
                return order
        return None

    def select_all_orders(self):
        orders = list(self.__orderDB.values())
        return orders if orders else None

    def update_order(self, orderId, order):
        if orderId in self.__orderDB:
            self.__orderDB[orderId] = order
            self.__save()
            return True
        return False

    def update_status(self, orderId, status):
        order = self.select_order_by_id(orderId)
        if order:
            order.set_status(status)
            self.__orderDB[orderId] = order
            self.__save()
            return True
        return False

    def update_tracking(self, orderId, trackingNo):
        order = self.select_order_by_id(orderId)
        if order:
            order.set_trackingNo(trackingNo)
            self.__orderDB[orderId] = order
            self.__save()
            return True
        return False

    def delete_order(self, orderId):
        if orderId in self.__orderDB:
            self.__orderDB.pop(orderId)
            self.__save()
            return True
        return False


# 클래스 다이어그램 명칭과의 호환용 별칭
Order_DAO = OrderDAO
