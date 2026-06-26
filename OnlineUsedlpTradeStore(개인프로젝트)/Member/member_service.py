from .member_entity import Member


class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, member_dao):
        self.__DAO = member_dao
        self.current_member = None

    def join(self, member):
        if member.get_memberId() == MemberService.ADMIN_ID:
            return 'ADMIN_ID_ERROR'
        if self.is_exist(member.get_memberId()):
            return 'ID_DUPLICATED'
        if self.is_phone_exist(member.get_phone()):
            return 'PHONE_DUPLICATED'
        return self.__DAO.insert_member(member)

    def login(self, memberId, password):
        member = self.__DAO.select_member_by_id(memberId)
        if member and member.get_password() == password:
            self.current_member = memberId
            return True
        return False

    def logout(self):
        self.current_member = None
        return True

    def is_exist(self, memberId):
        return self.__DAO.select_member_by_id(memberId) is not None

    def is_phone_exist(self, phone):
        return self.__DAO.select_member_by_phone(phone) is not None

    def is_admin(self):
        return self.current_member == MemberService.ADMIN_ID

    def view_member_info(self, memberId):
        return self.__DAO.select_member_by_id(memberId)

    def update_member_info(self, memberId, member):
        old = self.__DAO.select_member_by_id(memberId)
        if not old:
            return False
        if memberId == MemberService.ADMIN_ID:
            return 'ADMIN_UPDATE_ERROR'

        same_phone_member = self.__DAO.select_member_by_phone(member.get_phone())
        if same_phone_member and same_phone_member.get_memberId() != memberId:
            return 'PHONE_DUPLICATED'

        member.set_memberId(memberId)
        member.set_password(old.get_password())
        return self.__DAO.update_member(memberId, member)

    def update_password(self, memberId, org_pw, new_pw):
        member = self.__DAO.select_member_by_id(memberId)
        if not member:
            return False
        if member.get_password() != org_pw:
            return 'PASSWORD_ERROR'
        member.set_password(new_pw)
        return self.__DAO.update_member(memberId, member)

    def remove_member(self, memberId, password=None, by_admin=False):
        member = self.__DAO.select_member_by_id(memberId)
        if not member:
            return False
        if memberId == MemberService.ADMIN_ID:
            return 'ADMIN_DELETE_ERROR'
        if not by_admin and member.get_password() != password:
            return 'PASSWORD_ERROR'
        if self.current_member == memberId:
            self.current_member = None
        return self.__DAO.delete_member(memberId)

    def list_members(self):
        members = self.__DAO.select_all_members()
        if not members:
            return None
        return [m for m in members if m.get_memberId() != MemberService.ADMIN_ID]


# 클래스 다이어그램 명칭과의 호환용 별칭
Member_Service = MemberService
