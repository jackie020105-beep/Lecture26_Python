from .delivery import Delivery

class DeliveryDAO:
    def __init__(self):
        self.__deliveryDB = {}

    def insert_delivery(self, delivery):
        deliveryId = delivery.get_deliveryId()
        if deliveryId not in self.__deliveryDB:
            self.__deliveryDB[deliveryId] = delivery
            return True
        return False

    def select_delivery_by_id(self, deliveryId):
        return self.__deliveryDB.get(deliveryId)
    
    def select_delivery_by_order(self, orderId):
        for delivery in self.__deliveryDB.values():
            if delivery.get_orderId() == orderId:
                return delivery
        return None

    def select_delivery_by_member(self, memberId):
        result = []
        for delivery in self.__deliveryDB.values():
            if delivery.get_memberId() == memberId:
                result.append(delivery)
        return result

    def update_delivery(self, deliveryId, delivery):
        if deliveryId in self.__deliveryDB:
            self.__deliveryDB[deliveryId] = delivery
            return True
        return False

    def delete_delivery(self, deliveryId):
        if deliveryId in self.__deliveryDB:
            self.__deliveryDB.pop(deliveryId)
            return True
        return False


# 테스트
if __name__ == '__main__':
    dao = DeliveryDAO()

    d1 = Delivery('D111111', 'O111111', 'member_1', '서울시 강남구', '배송준비중')
    d2 = Delivery('D111112', 'O111112', 'member_1', '서울시 서초구', '배송중')

    print(dao.insert_delivery(d1))
    print(dao.insert_delivery(d2))
    print()

    print(dao.select_delivery_by_id('D111111'))
    print()

    for delivery in dao.select_delivery_by_member('member_1'):
        print(delivery)
    print()

    d1.set_status('배송완료')
    print(dao.update_delivery('D111111', d1))
    print(dao.select_delivery_by_id('D111111'))
    print()

    print(dao.delete_delivery('D111111'))
    print(dao.select_delivery_by_id('D111111'))