class Order:
    STATUS_ORDERED = '주문완료'
    STATUS_PREPARING = '배송준비중'
    STATUS_SHIPPING = '배송중'
    STATUS_DELIVERED = '배송완료'
    STATUS_CANCEL_REQUEST = '취소요청'
    STATUS_CANCELLED = '주문취소'

    def __init__(self, orderId, memberId, lpId, price, deliveryprice, totalprice, address, status=STATUS_ORDERED, trackingNo=''):
        self.__orderId = orderId
        self.__memberId = memberId
        self.__lpId = lpId
        self.__price = int(price)
        self.__deliveryprice = int(deliveryprice)
        self.__totalprice = int(totalprice)
        self.__address = address
        self.__status = status
        self.__trackingNo = trackingNo

    def get_orderId(self):
        return self.__orderId

    def get_memberId(self):
        return self.__memberId

    def get_lpId(self):
        return self.__lpId

    def get_price(self):
        return self.__price

    def get_deliveryprice(self):
        return self.__deliveryprice

    def get_totalprice(self):
        return self.__totalprice

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status

    def get_trackingNo(self):
        return self.__trackingNo

    def set_orderId(self, orderId):
        self.__orderId = orderId

    def set_memberId(self, memberId):
        self.__memberId = memberId

    def set_lpId(self, lpId):
        self.__lpId = lpId

    def set_price(self, price):
        self.__price = int(price)
        self.__totalprice = self.__price + self.__deliveryprice

    def set_deliveryprice(self, deliveryprice):
        self.__deliveryprice = int(deliveryprice)
        self.__totalprice = self.__price + self.__deliveryprice

    def set_totalprice(self, totalprice):
        self.__totalprice = int(totalprice)

    def set_address(self, address):
        self.__address = address

    def set_status(self, status):
        self.__status = status

    def set_trackingNo(self, trackingNo):
        self.__trackingNo = trackingNo

    def get_list_info(self, lp=None, seller=None, buyer=None):
        if lp:
            lp_text = f'LP번호 : {lp.get_lpId()} | 앨범명 : {lp.get_title()} | 아티스트 : {lp.get_artist()}'
        else:
            lp_text = f'LP번호 : {self.__lpId}'
        seller_text = f' | 판매자명 : {seller.get_name()}' if seller else ''
        buyer_text = f' | 구매자명 : {buyer.get_name()}' if buyer else ''
        return f'주문번호 : {self.__orderId} | {lp_text}{seller_text}{buyer_text} | 주문상태 : {self.__status}'

    def get_detail_info(self, lp=None, seller=None):
        if lp:
            lp_info = (f'LP번호 : {lp.get_lpId()}\n'
                       f'앨범명 : {lp.get_title()}\n'
                       f'아티스트 : {lp.get_artist()}\n'
                       f'내용 : {lp.get_description()}\n')
        else:
            lp_info = f'LP번호 : {self.__lpId}\n'
        seller_name = seller.get_name() if seller else '-'
        return (lp_info +
                f'가격 : {self.__price}원\n'
                f'배송가격 : {self.__deliveryprice}원\n'
                f'총가격 : {self.__totalprice}원\n'
                f'판매자명 : {seller_name}\n'
                f'배송주소 : {self.__address}\n'
                f'주문상태 : {self.__status}\n'
                f'송장번호 : {self.__trackingNo if self.__trackingNo else "-"}')

    def __str__(self):
        return self.get_detail_info()


# 클래스 다이어그램 명칭과의 호환용 별칭
Order_Entity = Order
