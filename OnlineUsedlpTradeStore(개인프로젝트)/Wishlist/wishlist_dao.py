import pickle
from pathlib import Path


class WishlistDAO:
    def __init__(self):
        self.__file_path = Path(__file__).resolve().parents[1] / 'Data' / 'wishlistDB.obj'
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)
        self.__wishlistDB = self.__load()  # 회원아이디 : Wishlist 객체

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
            pickle.dump(self.__wishlistDB, f)

    def insert_wishlist(self, wishlist):
        memberId = wishlist.get_memberId()
        if not self.select_wishlist_by_member(memberId):
            self.__wishlistDB[memberId] = wishlist
            self.__save()
            return True
        return False

    def select_wishlist_by_member(self, memberId):
        return self.__wishlistDB.get(memberId)

    def update_wishlist(self, memberId, wishlist):
        if memberId in self.__wishlistDB:
            self.__wishlistDB[memberId] = wishlist
            self.__save()
            return True
        return False

    def delete_wishlist(self, memberId):
        if memberId in self.__wishlistDB:
            self.__wishlistDB.pop(memberId)
            self.__save()
            return True
        return False

    def select_all_wishlists(self):
        wishlists = list(self.__wishlistDB.values())
        return wishlists if wishlists else None


# 클래스 다이어그램 명칭과의 호환용 별칭
Wishlist_DAO = WishlistDAO
