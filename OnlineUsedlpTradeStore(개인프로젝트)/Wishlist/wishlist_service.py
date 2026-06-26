from .wishlist_entity import Wishlist
from LP.lp_entity import LP


class WishlistService:
    wishlistId_seq = 1

    def __init__(self, wishlist_dao, lp_service):
        self.__DAO = wishlist_dao
        self.__LpService = lp_service
        self.__sync_sequence()

    def __sync_sequence(self):
        wishlists = self.__DAO.select_all_wishlists()
        max_no = 0
        if wishlists:
            for wishlist in wishlists:
                try:
                    max_no = max(max_no, int(wishlist.get_wishlistId().replace('W', '')))
                except ValueError:
                    pass
        WishlistService.wishlistId_seq = max_no + 1

    def __new_wishlist_id(self):
        wid = f'W{WishlistService.wishlistId_seq:04d}'
        WishlistService.wishlistId_seq += 1
        return wid

    def __get_or_create_wishlist(self, memberId):
        wishlist = self.__DAO.select_wishlist_by_member(memberId)
        if not wishlist:
            wishlist = Wishlist(self.__new_wishlist_id(), memberId, [])
            self.__DAO.insert_wishlist(wishlist)
        return wishlist

    def view_wishlist(self, memberId):
        wishlist = self.__DAO.select_wishlist_by_member(memberId)
        if not wishlist:
            return None
        lp_list = []
        changed = False
        for lpId in list(wishlist.get_lpItems()):
            lp = self.__LpService.get_lp_detail(lpId)
            if lp:
                lp_list.append(lp)
            else:
                wishlist.remove_lp(lpId)
                changed = True
        if changed:
            self.__DAO.update_wishlist(memberId, wishlist)
        return lp_list if lp_list else None

    def add_item(self, memberId, lpId):
        lp = self.__LpService.get_lp_detail(lpId)
        if not lp:
            return False
        if lp.get_sellerId() == memberId:
            return 'SELF_ITEM_ERROR'
        if lp.get_status() != LP.STATUS_ON_SALE:
            return 'SOLD_ERROR'
        wishlist = self.__get_or_create_wishlist(memberId)
        if not wishlist.add_lp(lpId):
            return 'DUPLICATED'
        return self.__DAO.update_wishlist(memberId, wishlist)

    def remove_item(self, memberId, lpId):
        wishlist = self.__DAO.select_wishlist_by_member(memberId)
        if not wishlist:
            return False
        if not wishlist.remove_lp(lpId):
            return False
        return self.__DAO.update_wishlist(memberId, wishlist)

    def clear_wishlist(self, memberId):
        return self.__DAO.delete_wishlist(memberId)

    def remove_lp_from_all(self, lpId):
        wishlists = self.__DAO.select_all_wishlists()
        if not wishlists:
            return True
        for wishlist in wishlists:
            if lpId in wishlist.get_lpItems():
                wishlist.remove_lp(lpId)
                self.__DAO.update_wishlist(wishlist.get_memberId(), wishlist)
        return True


# 클래스 다이어그램 명칭과의 호환용 별칭
Wishlist_Service = WishlistService
