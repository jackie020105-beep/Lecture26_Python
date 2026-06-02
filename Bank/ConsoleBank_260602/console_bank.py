from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료','로그인','회원가입'] # 시작 메뉴
    banking_menu = ['로그아웃','계좌목록','입금','출금','계좌생성','계좌해지','내정보'] # 회원 메뉴
    member_myinfo_menu = ['돌아가기','내정보보기','비밀번호수정','회원탈퇴'] # 내 정보 메뉴
    admin_menu = ['로그아웃','회원관리','계좌관리'] # 관리자 메뉴
    admin_account_menu = ['돌아가기','전체계좌목록','회원별계좌목록'] # 계좌관리 메뉴
    admin_member_menu = ['돌아가기','회원목록','회원정보조회','회원강퇴'] # 회원관리 메뉴

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        while True:
            # 시작 메뉴
            run_start_menu = self.run_start_menu()
            if run_start_menu == 0:
                break
        self.say_goodbye()




# start_menu ==================================================================

    def show_welcome(self):
        print('================ Jae ConsoleBank ================')

    def say_goodbye(self):
        print('============ 이용해주셔서 감사합니다 ============')
        print()

    def select_menu(self, menu_list):
        # 메뉴 리스트 보여주기
        print()
        print('====================== MENU ======================')
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]} | ', end=' ')
        print(f'0. {menu_list[0]}')
        print('==================================================')
        print()
        # 메뉴 입력 받기
        try:
            menu = int(input('>>메뉴 선택 : '))
            print()
        # 예외처리 (없는 메뉴 선택 에러)
            if not (0 <= menu <= len(menu_list)-1):
                raise Exception('ERROR : 잘못된 입력입니다')
            return menu
        except Exception as e:
            print(e)
            return -1
        # 예외처리 (문자입력 에러)
        except ValueError:
            print()
            print('ERROR : 잘못된 입력입니다')
            return -1


    def run_start_menu(self):
        # 각 메뉴의 동작
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0:
                return False
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()


    # 로그인
    def menu_login(self):
        id = input(f'아이디: ')
        password = input(f'비밀번호: ')
        print()
        if self.msv.login(id, password):
            if self.msv.current_user == MemberService.ADMIN_ID:
                print('관리자 전용 페이지')
                self.run_admin_menu()
            else:
                print('로그인되었습니다')
                self.run_banking_menu()
        else:
            print('ERROR : 아이디 또는 비밀번호가 잘못되었습니다')     
    # 회원가입
    def menu_join(self):
        id = input(f'생성할 아이디: ')
        password = input(f'사용할 비밀번호: ')
        name = input(f'계좌주: ')
        print()
        member = Member(id, password, name)
        if self.msv.join(member) == True:
            print(f'{name}님 회원가입 되었습니다')
        else:
            print('ERROR : 이미 가입된 회원입니다')







# banking_menu ==================================================================

    def run_banking_menu(self):
        # 각 메뉴의 동작
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                return
            elif menu == 1:
                self.menu_list_my_accounts()
            elif menu == 2:
                self.menu_deposit()
            elif menu == 3:
                self.menu_withdraw()
            elif menu == 4:
                self.menu_create_account()
            elif menu == 5:
                self.menu_delete_account()
            elif menu == 6:
                self.menu_myinfo()

    # 계좌목록
    def menu_list_my_accounts(self):
        my_accounts = self.asv.get_members_accounts(self.msv.current_user)
        if my_accounts:
            for account in my_accounts:
                print(account)
        else:
            print('회원님 명의의 계좌가 없습니다')

    # 입금
    def menu_deposit(self):
        account_no = (input(f'입금 계좌번호: '))
        amount = int(input(f'입금 금액: '))
        print()
        deposit_result = self.asv.deposit(account_no, amount)
        if deposit_result == True:
            print('입금되었습니다')
            self.menu_list_my_accounts()
        else:
            print('ERROR : 잘못된 계좌번호입니다')

    # 출금
    def menu_withdraw(self):
        account_no = (input(f'출금 계좌번호: '))
        password = input(f'비밀번호: ')
        amount = int(input(f'출금 금액: '))
        print()
        try:
            withdraw_result = self.asv.withdraw(self.msv.current_user, account_no, amount, password)
            if withdraw_result == True:
                print('출금되었습니다')
                self.menu_list_my_accounts()
            else:
                print('ERROR : 잘못된 계좌번호입니다')
        except KeyError:
            print ('ERROR : 비밀번호가 일치하지 않습니다.')
        except ValueError:
            print('ERROR : 계좌 잔액이 부족합니다.')

    # 계좌생성
    def menu_create_account(self):
        password = input('생성할 계좌 비밀번호 : ')
        print()
        new_account = Account(account_no = 0, owner = self.msv.current_user, balance = 0, password = password)
        create_account = self.asv.create_account(new_account)
        if create_account == True:
            print(f'계좌가 생성되었습니다 [계좌번호: {new_account.get_account_no()}]')
        else:
            print('ERROR : 계좌 생성에 실패했습니다')

    # 계좌해지
    def menu_delete_account(self):
        id = input(f'아이디: ')
        password = input(f'비밀번호: ')
        account_no = input(f'삭제할 계좌번호: ')
        print()
        try:
            delete_account_result = self.asv.delete_account(id, account_no, password)
            if delete_account_result == True:
                print(f'[계좌번호: {account_no}] 계좌가 삭제되었습니다')
            else:
                print('ERROR : 잘못된 계좌번호입니다')
        except KeyError:
            print ('ERROR : 아이디나 비밀번호가 일치하지 않습니다.')

    # 내 정보
    def menu_myinfo(self):
        self.run_my_info_menu()







# my_info_menu ==================================================================

    def run_my_info_menu(self):
        # 각 메뉴의 동작
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0:
                print('회원메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_update_password()
            elif menu == 3:
                self.menu_delete_membership()

    # 내 정보 보기
    def menu_view_myinfo(self):
        myinfo = self.msv.view_member_info(self.msv.current_user)
        print(myinfo)

    # 비밀번호 수정
    def menu_update_password(self):
        id = input(f'아이디: ')
        org_password = input(f'현재 비밀번호: ')
        new_password = input(f'새 비밀번호: ')
        print()
        member_password = self.msv.update_member_password(id, org_password, new_password)
        if member_password == True:
            print('비밀번호가 바뀌었습니다')
        else:
            print('ERROR : 아이디나 비밀번호가 일치하지 않습니다.')

    # 회원탈퇴
    def menu_delete_membership(self):
        id = input(f'아이디: ')
        print()
        delete_member = self.msv.remove_member(id)
        if delete_member == True:
            print('계정이 삭제되었습니다')
        else:
            print('ERROR : 아이디가 일치하지 않습니다.')


# admin_menu ==================================================================

    def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                return
            elif menu == 1:
                self.menu_manage_members()
            elif menu == 2:
                self.menu_manage_accounts()


    def menu_manage_members(self):
        self.run_admin_member_menu()


    def menu_manage_accounts(self):
        self.run_admin_account_menu()




# admin_account_menu ==================================================================

    def run_admin_account_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0:
                print('관리자메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_list_all_accounts()
            elif menu == 2:
                self.menu_list_member_accounts()

    # 전체계좌목록
    def menu_list_all_accounts(self):
        all_accounts = self.asv.get_all_accounts()
        if all_accounts:
            for accounts in all_accounts:
                print(accounts)
        else:
            print('생성된 계좌가 없습니다')

    # 회원별계좌목록
    def menu_list_member_accounts(self):
        id = input(f'확인할 회원 아이디: ')
        print()
        check_member_accounts = self.asv.get_members_accounts(id)
        if check_member_accounts:
            for member_accounts in check_member_accounts:
                print(member_accounts)
        else:
            print('회원이 보유한 계좌가 없거나 존재하지 않는 회원입니다')


# admin_member_menu ==================================================================

    def run_admin_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0:
                print('관리자 메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_delete_member()

    # 회원목록
    def menu_list_members(self):
        list_members = self.msv.list_members()
        if list_members:
            for members in list_members:
                print(members)
        else:
            print('가입된 회원이 없습니다')

    # 회원정보조회
    def menu_view_member_info(self):
        id = input(f'확인할 회원 아이디: ')
        print()
        check_member_info = self.msv.view_member_info(id)
        print(check_member_info)

    # 회원강퇴
    def menu_delete_member(self):
        id = input(f'아이디: ')
        print()
        delete_member = self.msv.remove_member(id)
        if delete_member == True:
            print('계정이 삭제되었습니다')
        else:
            print('ERROR : 아이디가 일치하지 않습니다.')


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()