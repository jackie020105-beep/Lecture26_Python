class MemberManager:
    def __init__(self, member_service):
        self.__memberService = member_service

    def list_members(self):
        return self.__memberService.list_members()

    def view_member_info(self, id):
        return self.__memberService.view_member_info(id)

    def remove_member(self, id):
        return self.__memberService.remove_member(id)
