class Member:
    def __init__(self, id, password, name):
        self.__id = id
        self.__password = password
        self.__name = name

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
    def set_name(self, name):
        self.__name = name

    def __str__(self):
        return f'아이디 : {self.__id} 이름 : {self.__name}'


if __name__ == '__main__':
    m = Member('member_1', '1111', '정원재')
    print(m)
    m.set_password('2222')
    print(m.get_password())
