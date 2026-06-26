from Member.member_entity import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from LP.lp_dao import LPDAO
from LP.lp_service import LPService
from LP.lp_entity import LP
from Wishlist.wishlist_dao import WishlistDAO
from Wishlist.wishlist_service import WishlistService
from Order.order_dao import OrderDAO
from Order.order_service import OrderService
from Order.order_entity import Order


class ConsoleOnlineLPStore:
    start_menu = ['종료', '로그인', '회원가입', '상품조회']

    # 회원 메뉴
    member_menu = ['로그아웃', '상품조회', '위시리스트', '주문내역조회', '내상품', '내정보']
    lp_menu = ['돌아가기', 'LP상세정보', '위시리스트 추가', '구매하기']
    wishlist_menu = ['돌아가기', '위시리스트 삭제', 'LP상세정보', '구매하기']
    order_menu = ['돌아가기', '상세조회']
    order_detail_menu = ['돌아가기', '배송조회', '주문취소요청']
    my_lp_menu = ['돌아가기', 'LP등록', '상품수정', '상품삭제']
    lp_edit_menu = ['돌아가기', '판매상품수정', '판매완료상품수정']
    sold_edit_menu = ['돌아가기', '배송준비중', '배송중', '배송완료', '취소요청']
    cancel_request_menu = ['돌아가기', '승인', '거부']
    my_info_menu = ['돌아가기', '내정보수정', '회원탈퇴']

    # 관리자 메뉴
    admin_menu = ['로그아웃', '상품관리', '회원관리', '주문목록조회']
    lp_manager_menu = ['돌아가기', '상품삭제']
    member_manager_menu = ['돌아가기', '회원목록조회', '회원정보조회', '회원탈퇴']
    order_list_menu = ['돌아가기', '회원별주문조회']
    member_order_menu = ['돌아가기', '주문상세']
    admin_order_detail_menu = ['돌아가기', '배송조회']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.lsv = LPService(LPDAO(), self.msv)
        self.wsv = WishlistService(WishlistDAO(), self.lsv)
        self.osv = OrderService(OrderDAO(), self.wsv, self.lsv, self.msv)
        self.sample_data()

    def main(self):
        self.show_welcome()
        while True:
            if self.run_start_menu() is False:
                break
        self.say_goodbye()

    def show_welcome(self):
        print("============== Jae's Online LP Used Trade Store ==============")
        print()
        print('관리자 계정: admin / 1234')
        print('샘플 회원: seller / 1111, buyer / 1111')
        print()

    def say_goodbye(self):
        print('============ 이용해주셔서 감사합니다 ============')

    def sample_data(self):
        members = self.msv.list_members()
        if not members:
            self.msv.join(Member('seller', '1111', '정원재', '010-1111-1111', 'jack0815@gmail.com', '서울특별시 성동구 응봉동'))
            self.msv.join(Member('buyer', '1111', '김이서', '010-2222-2222', 'Kim0701@gmail.com', '경기도 성남시 분당구 서현동'))

        if not self.lsv.get_all_lps():
            self.lsv.register_lp('Kind Of Blue', 'Miles Davis', 38000, '재즈 명반 중고 LP입니다. 커버 모서리에 약간 사용감이 있습니다.', 3000, 'seller')
            self.lsv.register_lp('Abbey Road', 'The Beatles', 45000, '재생 확인 완료. 음반 상태 양호합니다.', 3500, 'seller')
            self.lsv.register_lp('The Dark Side Of The Moon', 'Pink Floyd', 52000, '소장용으로 보관한 중고 LP입니다.', 4000, 'seller')

    def select_menu(self, menu_list, title='MENU'):
        print('====================== ' + title + ' ======================')
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]}', end=' | ')
        print(f'0. {menu_list[0]}')
        print()
        try:
            menu = int(input('>> 메뉴 선택 : '))
            print()
            if not (0 <= menu <= len(menu_list) - 1):
                print('ERROR : 없는 메뉴입니다')
                print()
                return -1
            return menu
        except ValueError:
            print('\nERROR : 숫자를 입력해주세요')
            print()
            return -1

    def input_int(self, message, allow_zero=True):
        try:
            value = int(input(message))
            if not allow_zero and value <= 0:
                print('ERROR : 1 이상의 숫자를 입력해주세요')
                print()
                return None
            if value < 0:
                print('ERROR : 0 이상의 숫자를 입력해주세요')
                print()
                return None
            return value
        except ValueError:
            print('ERROR : 숫자를 입력해주세요')
            return None

    def pause(self):
        input('\n계속하려면 Enter를 누르세요...')
        print()

    def is_member_login(self):
        return self.msv.current_member is not None and not self.msv.is_admin()

    # start_menu ==============================================================

    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineLPStore.start_menu, '시작 Menu')
            if menu == 0:
                return False
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()
            elif menu == 3:
                self.run_lp_menu()

    def menu_login(self):
        memberId = input('아이디 : ')
        password = input('비밀번호 : ')
        print()
        if self.msv.login(memberId, password):
            if self.msv.is_admin():
                print('관리자 전용 페이지입니다')
                print()
                self.run_admin_menu()
            else:
                member = self.msv.view_member_info(memberId)
                print(f'{member.get_name()}님 로그인되었습니다')
                print()
                self.run_member_menu()
        else:
            print('ERROR : 아이디 또는 비밀번호가 잘못되었습니다')
            print()

    def menu_join(self):
        memberId = input('생성할 아이디 : ')
        password = input('사용할 비밀번호 : ')
        name = input('이름 : ')
        phone = input('전화번호 : ')
        email = input('이메일 : ')
        address = input('주소 : ')
        print()
        member = Member(memberId, password, name, phone, email, address)
        result = self.msv.join(member)
        if result is True:
            print(f'{name}님 회원가입 되었습니다')
            print()
        elif result == 'ID_DUPLICATED' or result == 'PHONE_DUPLICATED' or result == 'ADMIN_ID_ERROR':
            print('ERROR : 이미 존재하는 회원입니다')
            print()
        else:
            print('ERROR : 회원가입에 실패했습니다')
            print()

    # member_menu =============================================================

    def run_member_menu(self):
        while self.msv.current_member:
            menu = self.select_menu(ConsoleOnlineLPStore.member_menu, '회원 Menu')
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                print()
                return
            elif menu == 1:
                self.run_lp_menu()
            elif menu == 2:
                self.run_wishlist_menu()
            elif menu == 3:
                self.run_order_menu()
            elif menu == 4:
                self.run_my_lp_menu()
            elif menu == 5:
                self.run_my_info_menu()

    # lp_menu =================================================================

    def run_lp_menu(self):
        while True:
            self.menu_list_lps()
            menu = self.select_menu(ConsoleOnlineLPStore.lp_menu, '상품조회 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_lp_detail()
            elif menu == 2:
                self.menu_add_wishlist()
            elif menu == 3:
                self.menu_buy_lp()

    def menu_list_lps(self):
        print('---------------- 전체 LP 목록 ----------------')
        print()
        lps = self.lsv.get_all_lps()
        if not lps:
            print('등록된 LP가 없습니다')
            print()
            return
        for lp in lps:
            print(lp.get_list_info())
            print()

    def menu_lp_detail(self):
        lpId = input('상세조회할 LP번호 : ')
        print()
        lp = self.lsv.get_lp_detail(lpId)
        if not lp:
            print('ERROR : 존재하지 않는 LP입니다')
            return
        seller = self.msv.view_member_info(lp.get_sellerId())
        seller_name = seller.get_name() if seller else lp.get_sellerId()
        print('---------------- LP 상세정보 ----------------')
        print()
        print(lp.get_detail_info(seller_name))
        print()

    def menu_add_wishlist(self):
        if not self.is_member_login():
            print('ERROR : 로그인 후 이용 가능합니다')
            print()
            return
        lpId = input('위시리스트에 추가할 LP번호 : ')
        print()
        result = self.wsv.add_item(self.msv.current_member, lpId)
        if result is True:
            print('위시리스트에 추가되었습니다')
            print()
        elif result == 'DUPLICATED':
            print('ERROR : 이미 위시리스트에 등록된 LP입니다')
            print()
        elif result == 'SELF_ITEM_ERROR':
            print('ERROR : 본인이 등록한 LP는 위시리스트에 담을 수 없습니다')
            print()
        elif result == 'SOLD_ERROR':
            print('ERROR : 판매완료된 LP는 위시리스트에 담을 수 없습니다')
            print()
        else:
            print('ERROR : 존재하지 않는 LP입니다')
            print()

    def menu_buy_lp(self):
        if not self.is_member_login():
            print('ERROR : 로그인 후 이용 가능합니다')
            print()
            return
        lpId = input('구매할 LP번호 : ')
        print()
        lp = self.lsv.get_lp_detail(lpId)
        if not lp:
            print('ERROR : 존재하지 않는 LP입니다')
            print()
            return
        print('---------------- 구매 LP 정보 ----------------')
        print()
        seller = self.msv.view_member_info(lp.get_sellerId())
        print(lp.get_detail_info(seller.get_name() if seller else None))
        confirm = input('구매하시겠습니까? (Y/N) : ').strip().upper()
        print()
        if confirm != 'Y':
            print('구매를 취소했습니다')
            return

        member = self.msv.view_member_info(self.msv.current_member)
        default_address = member.get_address()
        address = default_address
        if default_address:
            change = input(f'기본 배송주소 [{default_address}]를 사용하시겠습니까? (Y/N) : ').strip().upper()
            print()
            if change == 'N':
                address = input('배송주소 : ')
                print()
        else:
            address = input('배송주소 : ')
            print()

        result = self.osv.place_order(self.msv.current_member, lpId, address)
        if result is True:
            print('구매가 완료되었습니다')
            print()
        elif result == 'SELF_ITEM_ERROR':
            print('ERROR : 본인이 등록한 LP는 구매할 수 없습니다')
            print()
        elif result == 'SOLD_ERROR':
            print('ERROR : 판매완료된 LP입니다')
            print()
        elif result == 'ADDRESS_ERROR':
            print('ERROR : 배송주소가 필요합니다')
            print()
        else:
            print('ERROR : 구매에 실패했습니다')
            print()

    # wishlist_menu ===========================================================

    def run_wishlist_menu(self):
        while True:
            self.menu_view_wishlist()
            menu = self.select_menu(ConsoleOnlineLPStore.wishlist_menu, '위시리스트 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_remove_wishlist_item()
            elif menu == 2:
                self.menu_lp_detail()
            elif menu == 3:
                self.menu_buy_lp()

    def menu_view_wishlist(self):
        print('---------------- 위시리스트 ----------------')
        print()
        lp_list = self.wsv.view_wishlist(self.msv.current_member)
        if not lp_list:
            print('위시리스트가 비어있습니다')
            print()
            return
        for lp in lp_list:
            print(lp.get_list_info())
            print()

    def menu_remove_wishlist_item(self):
        lpId = input('삭제할 LP번호 : ')
        print()
        result = self.wsv.remove_item(self.msv.current_member, lpId)
        if result is True:
            print('위시리스트에서 삭제되었습니다')
            print()
        else:
            print('ERROR : 위시리스트에 없는 LP입니다')
            print()

    # order_menu ============================================================== 

    def run_order_menu(self):
        while True:
            self.menu_list_my_orders()
            menu = self.select_menu(ConsoleOnlineLPStore.order_menu, '주문내역 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.run_order_detail_menu()

    def menu_list_my_orders(self):
        print('---------------- 내 주문내역 ----------------')
        print()
        orders = self.osv.get_orders_by_member(self.msv.current_member)
        if not orders:
            print('주문내역이 없습니다')
            print()
            return
        for order in orders:
            lp = self.lsv.get_lp_detail(order.get_lpId())
            print(order.get_list_info(lp=lp))
            print()

    def run_order_detail_menu(self):
        orderId = input('상세조회할 주문번호 : ')
        print()
        order = self.osv.get_order_detail(orderId)
        if not order or order.get_memberId() != self.msv.current_member:
            print('ERROR : 조회할 수 없는 주문입니다')
            print()
            return
        while True:
            self.print_order_detail(orderId)
            menu = self.select_menu(ConsoleOnlineLPStore.order_detail_menu, '상세조회 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_view_delivery(orderId)
            elif menu == 2:
                self.menu_request_cancel(orderId)
                return

    def print_order_detail(self, orderId):
        order = self.osv.get_order_detail(orderId)
        lp = self.lsv.get_lp_detail(order.get_lpId()) if order else None
        seller = self.msv.view_member_info(lp.get_sellerId()) if lp else None
        print('---------------- 주문 상세 ----------------')
        print()
        if order:
            print(order.get_detail_info(lp=lp, seller=seller))
            print()
        else:
            print('ERROR : 주문이 없습니다')
            print()

    def menu_view_delivery(self, orderId):
        order = self.osv.get_order_detail(orderId)
        if not order:
            print('ERROR : 주문이 없습니다')
            print()
            return
        print('---------------- 배송조회 ----------------')
        print()
        print(f'주문번호 : {order.get_orderId()}')
        print(f'배송주소 : {order.get_address()}')
        print(f'배송상태 : {order.get_status()}')
        print(f'송장번호 : {order.get_trackingNo() if order.get_trackingNo() else "-"}')
        print()

    def menu_request_cancel(self, orderId):
        confirm = input('판매자에게 주문취소를 요청하시겠습니까? (Y/N) : ').strip().upper()
        print()
        if confirm != 'Y':
            print('주문취소 요청을 취소했습니다')
            print()
            return
        result = self.osv.request_cancel(orderId, self.msv.current_member)
        if result is True:
            print('주문취소가 요청되었습니다')
            print()
        elif result == 'STATUS_ERROR':
            print('ERROR : 배송완료 또는 취소된 주문은 취소 요청할 수 없습니다')
            print()
        else:
            print('ERROR : 주문취소 요청에 실패했습니다')
            print()

    # my_lp_menu ============================================================== 

    def run_my_lp_menu(self):
        while True:
            self.menu_list_my_lps()
            menu = self.select_menu(ConsoleOnlineLPStore.my_lp_menu, '내상품 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_register_lp()
            elif menu == 2:
                self.run_lp_edit_menu()
            elif menu == 3:
                self.menu_remove_my_lp()

    def menu_list_my_lps(self):
        print('---------------- 내상품 목록 ----------------')
        print()
        lps = self.lsv.get_my_lps(self.msv.current_member)
        if not lps:
            print('등록한 LP가 없습니다')
            print()
            return
        for lp in lps:
            order = self.osv.get_order_by_lp(lp.get_lpId())
            order_status = order.get_status() if order else '-'
            print(lp.get_my_list_info(order_status))
            print()

    def menu_register_lp(self):
        print('---------------- LP 등록 ----------------')
        print()
        title = input('앨범명 : ')
        artist = input('아티스트 : ')
        description = input('내용 : ')
        price = self.input_int('가격 : ', allow_zero=False)
        if price is None:
            return
        deliveryprice = self.input_int('배송가격 : ')
        print()
        if deliveryprice is None:
            return
        result = self.lsv.register_lp(title, artist, price, description, deliveryprice, self.msv.current_member)
        if result is True:
            print('LP가 등록되었습니다')
            print()
        else:
            print()
            print('ERROR : LP 등록에 실패했습니다')
            print()

    def run_lp_edit_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineLPStore.lp_edit_menu, '상품수정 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_edit_sale_lp()
            elif menu == 2:
                self.run_sold_edit_menu()

    def menu_edit_sale_lp(self):
        lps = self.lsv.get_my_lps(self.msv.current_member)
        sale_lps = [lp for lp in lps if lp.get_status() == LP.STATUS_ON_SALE] if lps else []
        if not sale_lps:
            print('수정 가능한 판매중 LP가 없습니다')
            print()
            return
        print('---------------- 판매중 LP ----------------')
        print()
        for lp in sale_lps:
            print(lp.get_list_info())
        print()
        lpId = input('수정할 LP번호 : ')
        print()
        lp = self.lsv.get_lp_detail(lpId)
        if not lp:
            print('ERROR : 존재하지 않는 LP입니다')
            print()
            return
        print('변경하지 않을 항목은 Enter만 입력하세요')
        print()
        title = input(f'앨범명 [{lp.get_title()}] : ') or lp.get_title()
        artist = input(f'아티스트 [{lp.get_artist()}] : ') or lp.get_artist()
        description = input(f'내용 [{lp.get_description()}] : ') or lp.get_description()
        price_text = input(f'가격 [{lp.get_price()}] : ')
        delivery_text = input(f'배송가격 [{lp.get_deliveryprice()}] : ')
        print()
        try:
            price = int(price_text) if price_text else lp.get_price()
            deliveryprice = int(delivery_text) if delivery_text else lp.get_deliveryprice()
        except ValueError:
            print('ERROR : 가격은 숫자로 입력해주세요')
            print()
            return
        result = self.lsv.edit_lp(lpId, title, artist, description, price, deliveryprice, self.msv.current_member)
        if result is True:
            print('LP 정보가 수정되었습니다')
            print()
        elif result == 'AUTH_ERROR':
            print('ERROR : 본인이 등록한 LP만 수정할 수 있습니다')
            print()
        elif result == 'SOLD_ERROR':
            print('ERROR : 판매완료된 LP는 판매상품수정에서 수정할 수 없습니다')
            print()
        else:
            print('ERROR : LP 수정에 실패했습니다')
            print()

    def run_sold_edit_menu(self):
        orders = self.osv.get_seller_orders(self.msv.current_member)
        sold_orders = []
        if orders:
            for order in orders:
                lp = self.lsv.get_lp_detail(order.get_lpId())
                if lp and lp.get_status() == LP.STATUS_SOLD:
                    sold_orders.append(order)
        if not sold_orders:
            print('판매완료된 LP 주문이 없습니다')
            print()
            return

        print('---------------- 판매완료 LP 주문 ----------------')
        print()
        for order in sold_orders:
            lp = self.lsv.get_lp_detail(order.get_lpId())
            buyer = self.msv.view_member_info(order.get_memberId())
            print(order.get_list_info(lp=lp, buyer=buyer))
            print()

        orderId = input('배송/취소 상태를 수정할 주문번호 : ')
        print()
        order = self.osv.get_order_detail(orderId)
        if not order:
            print('ERROR : 존재하지 않는 주문입니다')
            print()
            return
        lp = self.lsv.get_lp_detail(order.get_lpId())
        if not lp or lp.get_sellerId() != self.msv.current_member:
            print('ERROR : 본인이 판매한 LP 주문만 수정할 수 있습니다')
            print()
            return

        while True:
            self.print_order_detail_for_seller(orderId)
            menu = self.select_menu(ConsoleOnlineLPStore.sold_edit_menu, '판매완료수정 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_change_delivery_status(orderId, Order.STATUS_PREPARING)
            elif menu == 2:
                trackingNo = input('송장번호 : ')
                self.menu_change_delivery_status(orderId, Order.STATUS_SHIPPING, trackingNo)
            elif menu == 3:
                self.menu_change_delivery_status(orderId, Order.STATUS_DELIVERED)
            elif menu == 4:
                self.run_cancel_request_menu(orderId)
                return

    def print_order_detail_for_seller(self, orderId):
        order = self.osv.get_order_detail(orderId)
        lp = self.lsv.get_lp_detail(order.get_lpId()) if order else None
        buyer = self.msv.view_member_info(order.get_memberId()) if order else None
        print('---------------- 판매 주문 상세 ----------------')
        print()
        if order:
            print(order.get_detail_info(lp=lp, seller=buyer))
            print(f'구매자명 : {buyer.get_name() if buyer else "-"}')
            print()
        else:
            print('ERROR : 주문이 없습니다')
            print()

    def menu_change_delivery_status(self, orderId, status, trackingNo=None):
        result = self.osv.change_delivery_status(orderId, self.msv.current_member, status, trackingNo)
        if result is True:
            print(f'배송상태가 [{status}]로 변경되었습니다')
            print()
        elif result == 'TRACKING_ERROR':
            print('ERROR : 배송중 상태는 송장번호가 필요합니다')
            print()
        elif result == 'CANCEL_REQUEST_ERROR':
            print('ERROR : 취소요청 주문은 승인/거부 처리를 먼저 해주세요')
            print()
        elif result == 'CANCELLED_ERROR':
            print('ERROR : 이미 취소된 주문입니다')
            print()
        else:
            print('ERROR : 배송상태 수정에 실패했습니다')
            print()

    def run_cancel_request_menu(self, orderId):
        order = self.osv.get_order_detail(orderId)
        if not order or order.get_status() != Order.STATUS_CANCEL_REQUEST:
            print('ERROR : 취소요청 상태인 주문만 처리할 수 있습니다')
            print()
            return
        while True:
            menu = self.select_menu(ConsoleOnlineLPStore.cancel_request_menu, '취소요청 Menu')
            if menu == 0:
                return
            elif menu == 1:
                result = self.osv.approve_cancel(orderId, self.msv.current_member)
                print('주문취소 요청을 승인했습니다' if result is True else 'ERROR : 승인에 실패했습니다')
                print()
                return
            elif menu == 2:
                result = self.osv.reject_cancel(orderId, self.msv.current_member)
                print('주문취소 요청을 거부했습니다' if result is True else 'ERROR : 거부에 실패했습니다')
                print()
                return

    def menu_remove_my_lp(self):
        lpId = input('삭제할 LP번호 : ')
        print()
        result = self.lsv.remove_lp(lpId, self.msv.current_member)
        if result is True:
            self.wsv.remove_lp_from_all(lpId)
            print('LP가 삭제되었습니다')
            print()
        elif result == 'SOLD_ERROR':
            print('ERROR : 판매완료된 LP는 삭제할 수 없습니다')
            print()
        elif result == 'AUTH_ERROR':
            print('ERROR : 본인이 등록한 LP만 삭제할 수 있습니다')
            print()
        else:
            print('ERROR : 존재하지 않는 LP입니다')
            print()

    # my_info_menu ============================================================

    def run_my_info_menu(self):
        while self.msv.current_member:
            self.menu_view_myinfo()
            menu = self.select_menu(ConsoleOnlineLPStore.my_info_menu, '내정보 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_update_myinfo()
            elif menu == 2:
                self.menu_delete_membership()
                if self.msv.current_member is None:
                    return

    def menu_view_myinfo(self):
        print('---------------- 내정보 ----------------')
        print()
        member = self.msv.view_member_info(self.msv.current_member)
        print(member if member else '회원정보가 없습니다')
        print()

    def menu_update_myinfo(self):
        old = self.msv.view_member_info(self.msv.current_member)
        print('변경하지 않을 항목은 Enter만 입력하세요')
        print()
        name = input(f'이름 [{old.get_name()}] : ') or old.get_name()
        phone = input(f'전화번호 [{old.get_phone()}] : ') or old.get_phone()
        email = input(f'이메일 [{old.get_email()}] : ') or old.get_email()
        address = input(f'주소 [{old.get_address()}] : ') or old.get_address()
        print()

        change_pw = input('비밀번호도 변경하시겠습니까? (Y/N) : ').strip().upper()
        print()
        if change_pw == 'Y':
            org_pw = input('현재 비밀번호 : ')
            new_pw = input('새 비밀번호 : ')
            print()
            pw_result = self.msv.update_password(self.msv.current_member, org_pw, new_pw)
            if pw_result == 'PASSWORD_ERROR':
                print('ERROR : 현재 비밀번호가 일치하지 않습니다')
                print()
                return
            elif pw_result is not True:
                print('ERROR : 비밀번호 수정에 실패했습니다')
                print()
                return

        member = Member(self.msv.current_member, old.get_password(), name, phone, email, address)
        result = self.msv.update_member_info(self.msv.current_member, member)
        if result is True:
            print('회원정보가 수정되었습니다')
            print()
        elif result == 'PHONE_DUPLICATED':
            print('ERROR : 이미 가입된 전화번호입니다')
            print()
        else:
            print('ERROR : 회원정보 수정에 실패했습니다')
            print()

    def menu_delete_membership(self):
        password = input('회원탈퇴를 위해 비밀번호를 입력하세요 : ')
        confirm = input('정말 탈퇴하시겠습니까? (Y/N) : ').strip().upper()
        print()
        if confirm != 'Y':
            print('회원탈퇴를 취소했습니다')
            print()
            return
        result = self.msv.remove_member(self.msv.current_member, password)
        if result is True:
            print('회원탈퇴가 완료되었습니다')
            print()
        elif result == 'PASSWORD_ERROR':
            print('ERROR : 비밀번호가 일치하지 않습니다')
            print()
        else:
            print('ERROR : 회원탈퇴에 실패했습니다')
            print()

    # admin_menu ============================================================== 

    def run_admin_menu(self):
        while self.msv.current_member:
            menu = self.select_menu(ConsoleOnlineLPStore.admin_menu, '관리자 Menu')
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다')
                print()
                return
            elif menu == 1:
                self.run_lp_manager_menu()
            elif menu == 2:
                self.run_member_manager_menu()
            elif menu == 3:
                self.run_order_list_menu()

    def run_lp_manager_menu(self):
        while True:
            self.menu_list_lps()
            menu = self.select_menu(ConsoleOnlineLPStore.lp_manager_menu, '상품관리 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_admin_remove_lp()

    def menu_admin_remove_lp(self):
        lpId = input('삭제할 LP번호 : ')
        print()
        result = self.lsv.remove_lp(lpId, self.msv.current_member, by_admin=True)
        if result is True:
            self.wsv.remove_lp_from_all(lpId)
            print('LP가 삭제되었습니다')
            print()
        elif result == 'SOLD_ERROR':
            print('ERROR : 판매완료된 LP는 삭제할 수 없습니다')
            print()
        else:
            print('ERROR : 존재하지 않는 LP입니다')
            print()

    def run_member_manager_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineLPStore.member_manager_menu, '회원관리 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_admin_remove_member()

    def menu_list_members(self):
        print('---------------- 회원목록 ----------------')
        print()
        members = self.msv.list_members()
        if not members:
            print('가입된 회원이 없습니다')
            print()
            return
        for member in members:
            print(member.get_list_info())
            print()

    def menu_view_member_info(self):
        memberId = input('조회할 회원 아이디 : ')
        print()
        member = self.msv.view_member_info(memberId)
        if member and not member.isAdmin():
            print('---------------- 회원정보 ----------------')
            print()
            print(member)
            print()
        else:
            print('ERROR : 조회할 수 없는 회원입니다')
            print()

    def menu_admin_remove_member(self):
        memberId = input('탈퇴 처리할 회원 아이디 : ')
        print()
        result = self.msv.remove_member(memberId, by_admin=True)
        if result is True:
            print('회원탈퇴 처리되었습니다')
            print()
        elif result == 'ADMIN_DELETE_ERROR':
            print('ERROR : 관리자 계정은 탈퇴할 수 없습니다')
            print()
        else:
            print('ERROR : 존재하지 않는 회원입니다')
            print()

    def run_order_list_menu(self):
        while True:
            self.menu_list_all_orders()
            menu = self.select_menu(ConsoleOnlineLPStore.order_list_menu, '주문목록 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.run_member_order_menu()

    def menu_list_all_orders(self):
        print('---------------- 전체 주문목록 ----------------')
        print()
        orders = self.osv.get_all_orders()
        if not orders:
            print('주문내역이 없습니다')
            print()
            return
        for order in orders:
            lp = self.lsv.get_lp_detail(order.get_lpId())
            seller = self.msv.view_member_info(lp.get_sellerId()) if lp else None
            buyer = self.msv.view_member_info(order.get_memberId())
            print(order.get_list_info(lp=lp, seller=seller, buyer=buyer))
        print()

    def run_member_order_menu(self):
        memberId = input('주문을 조회할 회원 아이디 : ')
        print()
        orders = self.osv.get_orders_by_member(memberId)
        if not orders:
            print('해당 회원의 주문내역이 없습니다')
            print()
            return
        while True:
            print('---------------- 회원별 주문 ----------------')
            print()
            for order in orders:
                lp = self.lsv.get_lp_detail(order.get_lpId())
                print(order.get_list_info(lp=lp))
            print()
            menu = self.select_menu(ConsoleOnlineLPStore.member_order_menu, '회원별주문 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.run_admin_order_detail_menu(memberId)

    def run_admin_order_detail_menu(self, memberId):
        orderId = input('상세조회할 주문번호 : ')
        print()
        order = self.osv.get_order_detail(orderId)
        if not order or order.get_memberId() != memberId:
            print('ERROR : 조회할 수 없는 주문입니다')
            print()
            return
        while True:
            self.print_order_detail(orderId)
            menu = self.select_menu(ConsoleOnlineLPStore.admin_order_detail_menu, '주문상세 Menu')
            if menu == 0:
                return
            elif menu == 1:
                self.menu_view_delivery(orderId)


if __name__ == '__main__':
    app = ConsoleOnlineLPStore()
    app.main()
