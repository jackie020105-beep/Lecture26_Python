from .delivery import Delivery
from .delivery_dao import DeliveryDAO

class DeliveryService:
    deliveryId_seq = 111111

    def __init__(self, delivery_dao):
        self.__dao = delivery_dao

    def create_delivery(self, orderId, memberId, address):
        deliveryId = 'D' + str(DeliveryService.deliveryId_seq)
        DeliveryService.deliveryId_seq += 1

        delivery = Delivery(deliveryId, orderId, memberId, address, '배송준비중')
        return self.__dao.insert_delivery(delivery)

    def view_delivery(self, deliveryId):
        return self.__dao.select_delivery_by_id(deliveryId)

    def view_member_deliveries(self, memberId):
        return self.__dao.select_delivery_by_member(memberId)
    
    def view_delivery_by_order(self, orderId):
        return self.__dao.select_delivery_by_order(orderId)

    def change_status(self, deliveryId, status):
        delivery = self.__dao.select_delivery_by_id(deliveryId)
        if delivery:
            delivery.set_status(status)
            return self.__dao.update_delivery(deliveryId, delivery)
        return False


# 테스트
if __name__ == '__main__':
    delivery_service = DeliveryService(DeliveryDAO())

    delivery_service.create_delivery('O111111', 'member_1', '서울시 강남구')
    delivery_service.create_delivery('O111112', 'member_1', '서울시 서초구')

    print(delivery_service.view_delivery('D111111'))
    print()

    delivery_service.change_status('D111111', '배송중')
    print(delivery_service.view_delivery('D111111'))
    print()

    for delivery in delivery_service.view_member_deliveries('member_1'):
        print(delivery)

    print()
    delivery_service.cancel_delivery('D111111')
    print(delivery_service.view_delivery('D111111'))