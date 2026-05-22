from member import MemberDAO, MemberService, Member

class MemberManager():
    start_menu = ['종료','로그인','회원가입']
    admin_menu = ['로그아웃','회원목록','회원정보조회','회원탈퇴']
    member_menu = ['로그아웃','내정보조회','내정보수정','회원탈퇴']
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self):
        self.member_dao = MemberDAO()
        self.ms = MemberService(self.member_dao)
        self.current_user = None

    def main(self):
        self.show_welcome()
        self.ms.join(Member(MemberManager.ADMIN_ID, MemberManager.ADMIN_PASSWORD, None))
        while True:
            menu = self.select_menu(self.start_menu)

            if menu == 0:
                self.say_goodbye()
                break

            elif menu == 1:
                id = input('>> id : ')
                password = input('>> password : ')
                self.current_user = self.ms.login(id, password)
                if self.current_user:
                    if self.current_user == MemberManager.ADMIN_ID:
                        self.start_admin_menu()
                    else:
                        self.start_member_menu()  #과제
                else:
                    print('로그인에 실패하였습니다')

            elif menu == 2:
                id = input('>> id : ')
                password = input('>> password : ')
                name = input('>> name : ')
                member = Member(id, password, name)
                if self.ms.join(member):
                    print('회원가입되었습니다')
                else:
                    print('회원가입에 실패하였습니다')
            else:
                print('없는 메뉴입니다')

    def start_admin_menu(self):
        print('관리자메뉴')
        while True:
            menu = self.select_menu(self.admin_menu)
            if menu == 0:
                break
            elif menu == 1: #회원목록
                self.list_all_member()
            elif menu == 2: #회원정보조회 #과제
                self.view_member_info()
            elif menu == 3: #회원강퇴 #과제
                self.delete_member()
            else:
                print('없는 메뉴입니다')

    def list_all_member(self):
        if self.current_user != MemberManager.ADMIN_ID:
            print('사용권한이 없습니다')
            return
        member_list = self.ms.list_member()
        if len(member_list) == 1:
            print('가입한 회원이 없습니다')
        else:
            for member in member_list[1:]:
                print(member)

    def view_member_info(self):
        id = input('>> id : ')
        member = self.ms.view_member_info(id)
        if member:
            print(member)
        else:
            print('존재하지 않는 회원입니다')
            
    def delete_member(self):
        id = input('>> id : ')
        if id == MemberManager.ADMIN_ID:
            print('관리자 계정은 삭제할 수 없습니다')
            return            
        if self.ms.remove_member_info(id):
            print(f'{id} 계정이 삭제되었습니다.')
        else:
            print('존재하지 않는 회원입니다')

    def start_member_menu(self):
        print('회원메뉴')

    def show_welcome(self):
        print('='*50)
        title = 'Member Manager'
        print(f'{title:^50}')
        print('='*50)

    def say_goodbye(self):
        print('서비스를 종료합니다')

    def print_menu(self, menu_list):
        for i in range(1, len(menu_list)):
            print(f'{i}.{menu_list[i]}')
        print(f'0. {menu_list[0]}')
        print('-'*40)

    def select_menu(self, menu_list):
        self.print_menu(menu_list)
        try:
            menu = int(input('메뉴선택 : '))
            return menu
        except ValueError:
            return -1

if __name__ == '__main__':
    app = MemberManager()
    app.main()
