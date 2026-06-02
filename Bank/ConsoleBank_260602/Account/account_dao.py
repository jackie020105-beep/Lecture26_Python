from Account.account import Account

class AccountDAO:
    def __init__(self):
        self.__accountDB = {} # 계좌번호 : account 객체

    def insert_account(self, account):
        account_no = account.get_account_no()
        if not self.select_account_by_account_no(account_no):
            self.__accountDB[account_no] = account
            return True
        else:
            return False

    def select_account_by_account_no(self, account_no):
        if account_no in self.__accountDB:
            return self.__accountDB[account_no]
        else:
            return None

    def select_accounts_by_member_id(self, member_id):
        account_list = []
        for account in self.__accountDB.values():
            if account.get_owner() == member_id:
                account_list.append(account)  
        if len(account_list):
            return account_list
        else:
            return None

    def select_all_accounts(self):
        account_list = list(self.__accountDB.values())
        if len(account_list):
            return account_list
        else:
            return None

    def update_account(self, account_no, account):
        if account_no in self.__accountDB:
            self.__accountDB[account_no] = account
            return True
        else:
            return False

    def delete_account(self, account_no):
        if account_no in self.__accountDB:
            self.__accountDB.pop(account_no)
            return True
        else:
            return False

# 테스트
if __name__ == '__main__':
    dao = AccountDAO()
    ac_list = dao.select_all_accounts()
    print(ac_list)

    # insert_account
    dao.insert_account(Account('111111','정원재',10000,'1234'))
    dao.insert_account(Account('111112','김민수',20000,'1234'))

    # select_all_accounts
    for account in dao.select_all_accounts():
        print(account)

    # select_account_by_account_no
    print(dao.select_account_by_account_no('111122'))
    for account in dao.select_accounts_by_member_id('김민수'):
        print(account)
    
    # update_account
    dao.update_account('111111', Account('111111','정원재',300000,'1234'))
    print(dao.select_account_by_account_no('111111'))
    print()

    # delete_account
    dao.delete_account('111112')
    print(dao.select_account_by_account_no('111112'))