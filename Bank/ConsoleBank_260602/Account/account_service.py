from Account.account import Account
from Account.account_dao import AccountDAO

class AccountService:
    account_no_seq = 111111
    def __init__(self, account_dao):
        self.__dao = account_dao

    def create_account(self, account):
        #계좌번호를 생성하여 반영
        account.set_account_no(str(AccountService.account_no_seq))
        AccountService.account_no_seq += 1
        return self.__dao.insert_account(account)

    def get_all_accounts(self):
        return self.__dao.select_all_accounts()
            
    def get_members_accounts(self, id):
        return self.__dao.select_accounts_by_member_id(id)

    def deposit(self, account_no, amount):
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            new_balance = account.get_balance() + amount
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        else:
            return False

    def withdraw(self, id, account_no, amount, password):
        # 마이너스 통장 지원 안함
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            # id, password 체크
            if account.get_owner() != id or account.get_password() != password:
                raise KeyError
            # 계좌 잔액 체크
            new_balance = account.get_balance() - amount
            if new_balance < 0:
                raise ValueError
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        else:
            return False

    def delete_account(self, id, account_no, password):
        account = self.__dao.select_account_by_account_no(account_no)
        if not account:
            return False
        if account.get_owner() != id or account.get_password() != password:
            raise KeyError
        return self.__dao.delete_account(account_no)
        

# if __name__ == '__main__':
#     aservice = AccountService(AccountDAO())
#     # 계좌번호 자동 생성 (create_account)
#     aservice.create_account(Account(0,'정원재',10000,'1234'))
#     aservice.create_account(Account(0,'김민수',20000,'1234'))
#     aservice.create_account(Account(0,'전수연',30000,'1234'))
#     for account in aservice.get_all_accounts():
#         print(account)
#     print()

#     # get_members_accounts
#     for account in aservice.get_members_accounts('김민수'):
#         print(account)

#     # deposit
#     aservice.deposit('111113', 10000)
#     print()
#     for account in aservice.get_members_accounts('전수연'):
#         print(account)
#     if aservice.deposit('111114', 10000):
#         for account in aservice.get_all_accounts():
#             print(account)
#     else:
#         print('없는 계좌입니다')
#         print()

#     # withdraw
#     try:
#         aservice.withdraw('정원재', '111111', 5000, '1234')
#     except Exception as e:
#         print(type(e))
#     else:
#         for account in aservice.get_all_accounts():
#             print(account)
#     # 잔액부족
#     try:
#         aservice.withdraw('정원재', '111111', 100000, '1234')
#     except Exception as e:
#         print(type(e))
#     else:
#         for account in aservice.get_all_accounts():
#             print(account)
#     # password 틀리기
#     try:
#         aservice.withdraw('정원재', '111111', 100000, '0000')
#     except Exception as e:
#         print(type(e))
#     else:
#         for account in aservice.get_all_accounts():
#             print(account)
#     # id 틀리기
#     try:
#         aservice.withdraw('정원재', '111112', 100000, '0000')
#     except Exception as e:
#         print(type(e))
#     else:
#         for account in aservice.get_all_accounts():
#             print(account)
#             print()

#     # delete_account
#     try:
#         aservice.delete_account('김민수','111112','1234')
#     except Exception as e:
#         print(type(e))
#     else:
#         for account in aservice.get_all_accounts():
#             print(account)
#             print()