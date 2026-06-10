from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Member.member_manager import MemberManager
from Book.book import Book
from Book.book_dao import BookDAO
from Book.book_service import BookService
from Cart.cart_dao import CartDAO
from Cart.cart_service import CartService
from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery_service import DeliveryService
from Order.order_dao import OrderDAO
from Order.order_service import OrderService

class ConsoleOnlineBookStore:
    start_menu = ['종료','로그인','회원가입','도서조회'] # 시작 메뉴

    # 사용자 메뉴
    member_menu = ['로그아웃','도서조회','장바구니','주문내역조회','내정보'] # 회원 메뉴
    book_menu = ['돌아가기','도서상세정보','장바구니담기'] # 도서 메뉴
    cart_menu = ['돌아가기','책삭제','주문하기'] # 장바구니 메뉴
    order_menu = ['돌아가기','상세조회','주문취소'] # 주문내역 메뉴
    order_detail_menu = ['돌아가기','배송조회'] # 상세조회 메뉴
    my_info_menu = ['돌아가기','내정보조회','비밀번호수정','회원탈퇴'] # 내정보 메뉴

    # 관리자 메뉴
    admin_menu = ['로그아웃','도서관리','회원관리','주문목록조회','배송상태변경'] # 관리자 메뉴
    book_manager_menu = ['돌아가기','도서목록','도서추가','도서수정','도서삭제'] # 도서관리 메뉴
    member_manager_menu = ['돌아가기','회원목록','회원정보조회','회원삭제'] # 회원관리 메뉴

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.mmg = MemberManager(self.msv)
        self.bsv = BookService(BookDAO())
        self.csv = CartService(CartDAO(), self.bsv)
        self.dsv = DeliveryService(DeliveryDAO())
        self.osv = OrderService(OrderDAO(), self.csv, self.dsv)
        self.sample_books()

    def main(self):
        self.show_welcome()
        while True:
            run_start_menu = self.run_start_menu()
            if run_start_menu == False:
                break
        self.say_goodbye()

    def sample_books(self):
        self.bsv.add_book('축구의 이해', '정원재', 10000, 5)
        self.bsv.add_book('농구의 정석', '전민수', 20000, 3)
        self.bsv.add_book('야구의 모든 것', '김철수', 15000, 2)

# start_menu ==================================================================

    def show_welcome(self):
        print("================ Jae's Online Book Store ================")

    def say_goodbye(self):
        print('============ 이용해주셔서 감사합니다 ============')
        print()

    def select_menu(self, menu_list):
        print()
        print('====================== MENU ======================')
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]} | ', end=' ')
        print(f'0. {menu_list[0]}')
        print('==================================================')
        print()
        try:
            menu = int(input('>>메뉴 선택 : '))
            print()
            if not (0 <= menu <= len(menu_list)-1):
                raise Exception('ERROR : 잘못된 입력입니다')
            return menu
        except ValueError:
            print('ERROR : 숫자를 입력해주세요')
            return -1
        except Exception as e:
            print(e)
            return -1

    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.start_menu)
            if menu == 0:
                return False
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()
            elif menu == 3:
                self.run_book_menu()

    def menu_login(self):
        id = input('아이디: ')
        password = input('비밀번호: ')
        print()
        if self.msv.login(id, password):
            if self.msv.current_user == MemberService.ADMIN_ID:
                print('관리자 전용 페이지')
                self.run_admin_menu()
            else:
                print('로그인되었습니다')
                self.run_member_menu()
        else:
            print('ERROR : 아이디 또는 비밀번호가 잘못되었습니다')

    def menu_join(self):
        id = input('생성할 아이디: ')
        password = input('사용할 비밀번호: ')
        name = input('이름: ')
        phone = input('전화번호: ')
        email = input('이메일: ')
        print()
        member = Member(id, password, name, phone, email)
        if self.msv.join(member) == True:
            print(f'{name}님 회원가입 되었습니다')
        else:
            print('ERROR : 이미 가입된 회원입니다')

# member_menu ==================================================================

    def run_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.member_menu)
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                return
            elif menu == 1:
                self.run_book_menu()
            elif menu == 2:
                self.run_cart_menu()
            elif menu == 3:
                self.run_order_menu()
            elif menu == 4:
                self.run_my_info_menu()

# book_menu ==================================================================

    def run_book_menu(self):
        self.menu_list_books()
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.book_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_book_detail()
                self.menu_list_books()
            elif menu == 2:
                self.menu_add_cart()

    def menu_list_books(self):
        books = self.bsv.get_all_books()
        if books:
            for book in books:
                print(book.get_list_info())
        else:
            print('등록된 도서가 없습니다')

    def menu_book_detail(self):
        bookId = input('책번호: ')
        print()
        book = self.bsv.get_book_detail(bookId)
        if book:
            print(book)
        else:
            print('ERROR : 존재하지 않는 도서입니다')

    def menu_add_cart(self):
        if not self.msv.current_user:
            print('ERROR : 로그인 후 이용해주세요')
            return
        bookId = input('장바구니에 담을 책번호: ')
        print()
        if self.csv.add_item(self.msv.current_user, bookId) == True:
            print('장바구니에 담겼습니다')
            self.menu_list_books()
        else:
            print('ERROR : 존재하지 않는 도서입니다')
            self.menu_list_books()

# cart_menu ==================================================================

    def run_cart_menu(self):
        while True:
            self.menu_view_cart()
            menu = self.select_menu(ConsoleOnlineBookStore.cart_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_remove_cart_item()
            elif menu == 2:
                self.menu_order_cart()

    def menu_view_cart(self):
        cart = self.csv.view_cart(self.msv.current_user)
        if cart:
            print(cart)
        else:
            print('장바구니가 비어있습니다')

    def menu_remove_cart_item(self):
        bookId = input('삭제할 책번호: ')
        print()
        if self.csv.remove_item(self.msv.current_user, bookId) == True:
            print('선택한 책이 장바구니에서 삭제되었습니다')
        else:
            print('ERROR : 장바구니에 없는 책번호입니다')

    def menu_order_cart(self):
        address = self.osv.get_member_address(self.msv.current_user)
        if address:
            print(f'기존 배송주소로 주문합니다: {address}')
        else:
            address = input('배송주소: ')
        print()
        if self.osv.order_cart(self.msv.current_user, address) == True:
            print('주문되었습니다')
        else:
            print('ERROR : 장바구니가 비어있습니다')

# order_menu ==================================================================

    def run_order_menu(self):
        self.menu_list_my_orders()
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.order_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_order_detail()
            elif menu == 2:
                self.menu_cancel_order()

    def menu_list_my_orders(self):
        orders = self.osv.get_member_orders(self.msv.current_user)

        if orders:
            for order in orders:
                print(order)

                delivery = self.dsv.view_delivery_by_order(order.get_orderId())

                if delivery:
                    print(f'배송상태 : {delivery.get_status()}')

                print()
        else:
            print('주문내역이 없습니다')

    def menu_order_detail(self):
        orderId = input('주문번호: ')
        print()
        order = self.osv.get_order_detail(orderId)
        if order:
            print(order)
            self.run_order_detail_menu(orderId)
        else:
            print('ERROR : 존재하지 않는 주문입니다')

    def run_order_detail_menu(self, orderId):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.order_detail_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_view_delivery(orderId)

    def menu_view_delivery(self, orderId):
        deliveries = self.dsv.view_member_deliveries(self.msv.current_user)
        if deliveries:
            for delivery in deliveries:
                if delivery.get_orderId() == orderId:
                    print(delivery)
                    return
        print('배송정보가 없습니다')

    def menu_cancel_order(self):
        orderId = input('취소할 주문번호: ')
        print()
        if self.osv.cancel_order(orderId) == True:
            print('주문이 취소되었습니다')
        else:
            print('ERROR : 존재하지 않는 주문입니다')

# my_info_menu ==================================================================

    def run_my_info_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.my_info_menu)
            if menu == 0:
                print('회원메뉴로 돌아갑니다')
                return
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_update_password()
            elif menu == 3:
                self.menu_delete_membership()
                return

    def menu_view_myinfo(self):
        myinfo = self.msv.view_member_info(self.msv.current_user)
        print(myinfo)

    def menu_update_password(self):
        id = input('아이디: ')
        org_password = input('현재 비밀번호: ')
        new_password = input('새 비밀번호: ')
        print()
        if self.msv.update_member_password(id, org_password, new_password) == True:
            print('비밀번호가 바뀌었습니다')
        else:
            print('ERROR : 아이디나 비밀번호가 일치하지 않습니다')

    def menu_delete_membership(self):
        id = input('아이디: ')
        print()
        if id != self.msv.current_user:
            print('ERROR : 로그인된 아이디와 일치하지 않습니다')
            return
        if self.msv.remove_member(id) == True:
            self.msv.logout()
            print('계정이 삭제되었습니다')
        else:
            print('ERROR : 아이디가 일치하지 않습니다')

# admin_menu ==================================================================

    def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.admin_menu)
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                return
            elif menu == 1:
                self.run_book_manager_menu()
            elif menu == 2:
                self.run_member_manager_menu()
            elif menu == 3:
                self.menu_list_all_orders()
            elif menu == 4:
                self.menu_change_delivery_status()


# book_manager_menu ==================================================================

    def run_book_manager_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.book_manager_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_list_books()
            elif menu == 2:
                self.menu_add_book()
            elif menu == 3:
                self.menu_edit_book()
            elif menu == 4:
                self.menu_delete_book()

    def menu_add_book(self):
        title = input('제목: ')
        author = input('저자: ')
        price = int(input('가격: '))
        stock = int(input('재고: '))
        print()
        if self.bsv.add_book(title, author, price, stock) == True:
            print('도서가 추가되었습니다')
        else:
            print('ERROR : 도서 추가에 실패했습니다')

    def menu_edit_book(self):
        bookId = input('수정할 책번호: ')
        title = input('제목: ')
        author = input('저자: ')
        price = int(input('가격: '))
        stock = int(input('재고: '))
        print()
        book = Book(bookId, title, author, price, stock)
        if self.bsv.edit_book(bookId, book) == True:
            print('도서가 수정되었습니다')
        else:
            print('ERROR : 존재하지 않는 도서입니다')

    def menu_delete_book(self):
        bookId = input('삭제할 책번호: ')
        print()
        if self.bsv.remove_book(bookId) == True:
            print('도서가 삭제되었습니다')
        else:
            print('ERROR : 존재하지 않는 도서입니다')


# member_manager_menu ==================================================================

    def run_member_manager_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.member_manager_menu)
            if menu == 0:
                return
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_delete_member()

    def menu_list_members(self):
        members = self.mmg.list_members()
        if members:
            for member in members:
                print(member.get_list_info())
        else:
            print('가입된 회원이 없습니다')

    def menu_view_member_info(self):
        id = input('확인할 회원 아이디: ')
        print()
        member = self.mmg.view_member_info(id)
        if member:
            print(member)
        else:
            print('ERROR : 존재하지 않는 회원입니다')

    def menu_delete_member(self):
        id = input('삭제할 회원 아이디: ')
        print()
        if self.mmg.remove_member(id) == True:
            print('회원이 삭제되었습니다')
        else:
            print('ERROR : 존재하지 않는 회원이거나 관리자입니다')

# list_all_orders ==================================================================

    def menu_list_all_orders(self):
        orders = self.osv.get_all_orders()

        if orders:
            for order in orders:
                print(order)

                delivery = self.dsv.view_delivery_by_order(order.get_orderId())

                if delivery:
                    print(f'배송번호 : {delivery.get_deliveryId()}')
                    print(f'배송상태 : {delivery.get_status()}')

                print()
        else:
            print('주문내역이 없습니다')

# change_delivery_status ==================================================================

    def menu_change_delivery_status(self):
        deliveryId = input('배송번호: ')
        status = input('변경할 배송상태: ')
        print()
        if self.dsv.change_status(deliveryId, status) == True:
            print('배송상태가 변경되었습니다')
        else:
            print('ERROR : 존재하지 않는 배송입니다')


if __name__ == '__main__':
    app = ConsoleOnlineBookStore()
    app.main()
