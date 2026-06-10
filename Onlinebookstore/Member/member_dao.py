from .member import Member

class MemberDAO:
    def __init__(self):
        self.__memberDB = {}
        self.insert_member(Member('admin', '1234', '관리자', '010-0000-0000', 'jae@bookstore.com'))

    def insert_member(self, member):
        id = member.get_id()
        if not self.select_member_by_id(id):
            self.__memberDB[id] = member
            return True
        else:
            return False

    def select_member_by_id(self, id):
        if id in self.__memberDB:
            return self.__memberDB[id]
        else:
            return None

    def select_all_members(self):
        member_list = list(self.__memberDB.values())
        if len(member_list):
            return member_list
        else:
            return None

    def update_member(self, id, member):
        if id in self.__memberDB:
            self.__memberDB[id] = member
            return True
        else:
            return False

    def delete_member(self, id):
        if id in self.__memberDB:
            self.__memberDB.pop(id)
            return True
        else:
            return False


if __name__ == '__main__':
    dao = MemberDAO()
    dao.insert_member(Member('member_1', '1111', '정원재', '010-1234-5678', 'test@test.com'))
    print(dao.select_member_by_id('member_1'))
    for member in dao.select_all_members():
        print(member)
