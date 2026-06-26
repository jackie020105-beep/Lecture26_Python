import pickle
from pathlib import Path


class LPDAO:
    def __init__(self):
        self.__file_path = Path(__file__).resolve().parents[1] / 'Data' / 'lpDB.obj'
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)
        self.__lpDB = self.__load()

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
            pickle.dump(self.__lpDB, f)

    def insert_lp(self, lp):
        lpId = lp.get_lpId()
        if not self.select_lp_by_id(lpId):
            self.__lpDB[lpId] = lp
            self.__save()
            return True
        return False

    def select_lp_by_id(self, lpId):
        return self.__lpDB.get(lpId)

    def select_all_lps(self):
        lp_list = list(self.__lpDB.values())
        return lp_list if lp_list else None

    def select_lps_by_seller(self, sellerId):
        result = [lp for lp in self.__lpDB.values() if lp.get_sellerId() == sellerId]
        return result if result else None

    def select_lps_by_status(self, status):
        result = [lp for lp in self.__lpDB.values() if lp.get_status() == status]
        return result if result else None

    def update_lp(self, lpId, lp):
        if lpId in self.__lpDB:
            self.__lpDB[lpId] = lp
            self.__save()
            return True
        return False

    def update_status(self, lpId, status):
        lp = self.select_lp_by_id(lpId)
        if lp:
            lp.set_status(status)
            self.__lpDB[lpId] = lp
            self.__save()
            return True
        return False

    def delete_lp(self, lpId):
        if lpId in self.__lpDB:
            self.__lpDB.pop(lpId)
            self.__save()
            return True
        return False


# 클래스 다이어그램 명칭과의 호환용 별칭
LP_DAO = LPDAO
