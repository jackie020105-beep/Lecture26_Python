class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, member_dao):
        self.__dao = member_dao
        self.current_user = None

    def join(self, member):
        return self.__dao.insert_member(member)

    def login(self, id, password):
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == password:
            self.current_user = id
            return True
        else:
            return False

    def logout(self):
        self.current_user = None

    def list_members(self):
        return self.__dao.select_all_members()

    def view_member_info(self, id):
        return self.__dao.select_member_by_id(id)

    def update_member_password(self, id, org_password, new_password):
        member = self.__dao.select_member_by_id(id)
        if member and member.get_password() == org_password:
            member.set_password(new_password)
            return self.__dao.update_member(id, member)
        else:
            return False

    def update_member_name(self, id, name):
        member = self.__dao.select_member_by_id(id)
        if member:
            member.set_name(name)
            return self.__dao.update_member(id, member)
        else:
            return False

    def remove_member(self, id):
        if id == MemberService.ADMIN_ID:
            return False
        return self.__dao.delete_member(id)
