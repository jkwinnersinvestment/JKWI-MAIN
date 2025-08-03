class MemberController:
    def __init__(self, member_service):
        self.member_service = member_service

    def create_member(self, member_data):
        return self.member_service.create_member(member_data)

    def get_member(self, member_id):
        return self.member_service.get_member(member_id)

    def update_member(self, member_id, member_data):
        return self.member_service.update_member(member_id, member_data)

    def delete_member(self, member_id):
        return self.member_service.delete_member(member_id)

    def list_members(self):
        return self.member_service.list_members()