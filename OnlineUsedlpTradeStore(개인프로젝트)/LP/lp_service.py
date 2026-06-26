from .lp_entity import LP


class LPService:
    lpId_seq = 1

    def __init__(self, lp_dao, member_service):
        self.__DAO = lp_dao
        self.__MemberService = member_service
        self.__sync_sequence()

    def __sync_sequence(self):
        lps = self.__DAO.select_all_lps()
        max_no = 0
        if lps:
            for lp in lps:
                try:
                    max_no = max(max_no, int(lp.get_lpId().replace('LP', '')))
                except ValueError:
                    pass
        LPService.lpId_seq = max_no + 1

    def __new_lp_id(self):
        lp_id = f'LP{LPService.lpId_seq:04d}'
        LPService.lpId_seq += 1
        return lp_id

    def get_all_lps(self):
        lps = self.__DAO.select_all_lps()
        if not lps:
            return None
        return sorted(lps, key=lambda lp: lp.get_lpId())

    def get_sale_lps(self):
        lps = self.__DAO.select_lps_by_status(LP.STATUS_ON_SALE)
        if not lps:
            return None
        return sorted(lps, key=lambda lp: lp.get_lpId())

    def get_lp_detail(self, lpId):
        return self.__DAO.select_lp_by_id(lpId)

    def register_lp(self, title, artist, price, description, deliveryprice, sellerId):
        if not self.__MemberService.view_member_info(sellerId):
            return False
        lp = LP(self.__new_lp_id(), title, artist, description, price, deliveryprice, sellerId, LP.STATUS_ON_SALE)
        return self.__DAO.insert_lp(lp)

    def edit_lp(self, lpId, title, artist, description, price, deliveryprice, sellerId):
        lp = self.__DAO.select_lp_by_id(lpId)
        if not lp:
            return False
        if lp.get_sellerId() != sellerId:
            return 'AUTH_ERROR'
        if lp.get_status() == LP.STATUS_SOLD:
            return 'SOLD_ERROR'
        lp.set_title(title)
        lp.set_artist(artist)
        lp.set_description(description)
        lp.set_price(price)
        lp.set_deliveryprice(deliveryprice)
        return self.__DAO.update_lp(lpId, lp)

    def update_lp(self, lpId, lp):
        return self.__DAO.update_lp(lpId, lp)

    def remove_lp(self, lpId, requesterId, by_admin=False):
        lp = self.__DAO.select_lp_by_id(lpId)
        if not lp:
            return False
        if lp.get_status() == LP.STATUS_SOLD:
            return 'SOLD_ERROR'
        if by_admin or lp.get_sellerId() == requesterId:
            return self.__DAO.delete_lp(lpId)
        return 'AUTH_ERROR'

    def get_my_lps(self, sellerId):
        lps = self.__DAO.select_lps_by_seller(sellerId)
        if not lps:
            return None
        return sorted(lps, key=lambda lp: lp.get_lpId())

    def get_sold_lps(self, sellerId):
        lps = self.__DAO.select_lps_by_seller(sellerId)
        if not lps:
            return None
        result = [lp for lp in lps if lp.get_status() == LP.STATUS_SOLD]
        return sorted(result, key=lambda lp: lp.get_lpId()) if result else None

    def mark_as_sold(self, lpId):
        return self.__DAO.update_status(lpId, LP.STATUS_SOLD)

    def mark_as_sale(self, lpId):
        return self.__DAO.update_status(lpId, LP.STATUS_ON_SALE)


# 클래스 다이어그램 명칭과의 호환용 별칭
LP_Service = LPService
