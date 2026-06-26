class LP:
    STATUS_ON_SALE = '판매중'
    STATUS_SOLD = '판매완료'

    def __init__(self, lpId, title, artist, description, price, deliveryprice, sellerId, status=STATUS_ON_SALE):
        self.__lpId = lpId
        self.__title = title
        self.__artist = artist
        self.__description = description
        self.__price = int(price)
        self.__deliveryprice = int(deliveryprice)
        self.__sellerId = sellerId
        self.__status = status

    def get_lpId(self):
        return self.__lpId

    def get_title(self):
        return self.__title

    def get_artist(self):
        return self.__artist

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_deliveryprice(self):
        return self.__deliveryprice

    def get_sellerId(self):
        return self.__sellerId

    def get_status(self):
        return self.__status

    def set_lpId(self, lpId):
        self.__lpId = lpId

    def set_title(self, title):
        self.__title = title

    def set_artist(self, artist):
        self.__artist = artist

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = int(price)

    def set_deliveryprice(self, deliveryprice):
        self.__deliveryprice = int(deliveryprice)

    def set_sellerId(self, sellerId):
        self.__sellerId = sellerId

    def set_status(self, status):
        self.__status = status

    def get_list_info(self):
        return (f'LP번호 : {self.__lpId} | 앨범명 : {self.__title} | 아티스트 : {self.__artist} | '
                f'가격 : {self.__price}원 | 판매상태 : {self.__status}')

    def get_my_list_info(self, order_status='-'):
        return (f'LP번호 : {self.__lpId} | 앨범명 : {self.__title} | 아티스트 : {self.__artist} | '
                f'가격 : {self.__price}원 | 판매상태 : {self.__status} | 주문상태 : {order_status}')

    def get_detail_info(self, seller_name=None):
        seller_text = seller_name if seller_name else self.__sellerId
        return (f'LP번호 : {self.__lpId}\n'
                f'앨범명 : {self.__title}\n'
                f'아티스트 : {self.__artist}\n'
                f'내용 : {self.__description}\n'
                f'가격 : {self.__price}원\n'
                f'배송가격 : {self.__deliveryprice}원\n'
                f'판매자명 : {seller_text}\n'
                f'판매상태 : {self.__status}')

    def __str__(self):
        return self.get_detail_info()


# 클래스 다이어그램 명칭과의 호환용 별칭
LP_Entity = LP
