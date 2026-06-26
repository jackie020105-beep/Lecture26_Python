import pickle
from pathlib import Path
from .member_entity import Member


class MemberDAO:
    def __init__(self):
        self.__file_path = Path(__file__).resolve().parents[1] / 'Data' / 'memberDB.obj'
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)
        self.__memberDB = self.__load()
        self.__ensure_admin()

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
            pickle.dump(self.__memberDB, f)

    def __ensure_admin(self):
        admin = self.__memberDB.get('admin')
        if not admin:
            self.__memberDB['admin'] = Member('admin', '1234', '관리자', '010-0000-0000', 'admin@lpstore.com', '관리자')
            self.__save()
        else:
            # 관리자 계정은 고정값을 유지한다.
            admin.set_password('1234')
            admin.set_name('관리자')
            self.__memberDB['admin'] = admin
            self.__save()

    def insert_member(self, member):
        memberId = member.get_memberId()
        if not self.select_member_by_id(memberId):
            self.__memberDB[memberId] = member
            self.__save()
            return True
        return False

    def select_member_by_id(self, memberId):
        return self.__memberDB.get(memberId)

    def select_member_by_email(self, email):
        for member in self.__memberDB.values():
            if member.get_email() == email:
                return member
        return None

    def select_member_by_phone(self, phone):
        for member in self.__memberDB.values():
            if member.get_phone() == phone:
                return member
        return None

    def select_all_members(self):
        members = list(self.__memberDB.values())
        return members if members else None

    def update_member(self, memberId, member):
        if memberId in self.__memberDB:
            self.__memberDB[memberId] = member
            self.__save()
            return True
        return False

    def delete_member(self, memberId):
        if memberId in self.__memberDB:
            self.__memberDB.pop(memberId)
            self.__save()
            return True
        return False


# 클래스 다이어그램 명칭과의 호환용 별칭
Member_DAO = MemberDAO
