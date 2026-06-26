class Wishlist:
    def __init__(self, wishlistId, memberId, lpItems=None):
        self.__wishlistId = wishlistId
        self.__memberId = memberId
        self.__lpItems = lpItems if lpItems is not None else []

    def get_wishlistId(self):
        return self.__wishlistId

    def get_memberId(self):
        return self.__memberId

    def get_lpItems(self):
        return self.__lpItems

    def set_wishlistId(self, wishlistId):
        self.__wishlistId = wishlistId

    def set_memberId(self, memberId):
        self.__memberId = memberId

    def set_lpItems(self, lpItems):
        self.__lpItems = lpItems

    def add_lp(self, lpId):
        if lpId not in self.__lpItems:
            self.__lpItems.append(lpId)
            return True
        return False

    def remove_lp(self, lpId):
        if lpId in self.__lpItems:
            self.__lpItems.remove(lpId)
            return True
        return False

    def __str__(self):
        return f'위시리스트번호 : {self.__wishlistId} | 회원아이디 : {self.__memberId} | LP목록 : {self.__lpItems}'


# 클래스 다이어그램 명칭과의 호환용 별칭
Wishlist_Entity = Wishlist
