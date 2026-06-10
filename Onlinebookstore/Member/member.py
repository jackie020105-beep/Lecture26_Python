class Member:
    def __init__(self, id, password, name, phone, email):
        self.__id = id
        self.__password = password
        self.__name = name
        self.__phone = phone
        self.__email = email

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def set_password(self, password):
        self.__password = password

    def get_list_info(self):
        return f'아이디 : {self.__id} 이름 : {self.__name}'

    def __str__(self):
        return (f'아이디 : {self.__id} 이름 : {self.__name} 전화번호 : {self.__phone} 이메일 : {self.__email}')