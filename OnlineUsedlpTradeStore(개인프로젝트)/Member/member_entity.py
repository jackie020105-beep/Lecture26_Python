class Member:
    def __init__(self, memberId, password, name, phone, email, address):
        self.__memberId = memberId
        self.__password = password
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__address = address

    def get_memberId(self):
        return self.__memberId

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def set_memberId(self, memberId):
        self.__memberId = memberId

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def isAdmin(self):
        return self.__memberId == 'admin'

    def get_list_info(self):
        return f'아이디 : {self.__memberId} | 이름 : {self.__name} | 전화번호 : {self.__phone} | 주소 : {self.__address}'

    def get_info(self):
        return (f'아이디 : {self.__memberId}\n'
                f'이름 : {self.__name}\n'
                f'전화번호 : {self.__phone}\n'
                f'이메일 : {self.__email}\n'
                f'주소 : {self.__address}')

    def __str__(self):
        return self.get_info()


# 클래스 다이어그램 명칭과의 호환용 별칭
Member_Entity = Member
