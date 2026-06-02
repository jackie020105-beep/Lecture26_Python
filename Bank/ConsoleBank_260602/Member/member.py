# from member import Member, MemberDAO, MemberService

#======================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, id, password, name):
        self.__member_no = 0
        self.__id = id
        self.__password = password
        self.__name = name

    def get_member_no(self):
        return self.__member_no
    def get_id(self):
        return self.__id
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    def set_id(self, id):
        self.__id = id
    def set_password(self, password):
        self.__password = password
    
    def __str__(self):
        return f'{self.__member_no}\t{self.__id}\t{self.__name}\t{self.__password}'
    
# # 클래스 동작 테스트(단위테스트, unit test)
# if __name__ == '__main__':
#     dao = MemberDAO()
#     print(dao.is_exist('wonjae'))
#     member = Member('wonjae', '123', '원재')
#     dao.insert_member(member)
#     member = Member('won', '1234', '원')
#     dao.insert_member(member)
#     print(dao.get_member_info('wonjae'))
#     print(dao.get_member_info('won'))


#     member = dao.get_member_info('wonjae')
#     if member:
#         member.set_password('111')
#     dao.update_member_info('wonjae', member)

#     dao.remove_member('wonjae')


#     member = dao.get_all_members()
#     for member in member:
#         print(member)
    