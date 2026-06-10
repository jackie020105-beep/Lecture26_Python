class Delivery:
    def __init__(self, deliveryId, orderId, memberId, address, status):
        self.__deliveryId = deliveryId
        self.__orderId = orderId
        self.__memberId = memberId
        self.__address = address
        self.__status = status

    def get_deliveryId(self):
        return self.__deliveryId

    def get_orderId(self):
        return self.__orderId

    def get_memberId(self):
        return self.__memberId

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status

    def set_deliveryId(self, deliveryId):
        self.__deliveryId = deliveryId

    def set_orderId(self, orderId):
        self.__orderId = orderId

    def set_memberId(self, memberId):
        self.__memberId = memberId

    def set_address(self, address):
        self.__address = address

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return f'배송번호 : {self.__deliveryId} 주문번호 : {self.__orderId} 회원아이디 : {self.__memberId} 주소 : {self.__address} 배송상태 : {self.__status}'