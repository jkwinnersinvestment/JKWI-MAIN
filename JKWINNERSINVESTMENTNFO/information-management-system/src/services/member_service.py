class MemberService:
    def __init__(self):
        self.members = []

    def create_member(self, name, membership_status):
        member_id = len(self.members) + 1
        member = {
            'id': member_id,
            'name': name,
            'membership_status': membership_status
        }
        self.members.append(member)
        return member

    def get_member(self, member_id):
        for member in self.members:
            if member['id'] == member_id:
                return member
        return None

    def update_member(self, member_id, name=None, membership_status=None):
        member = self.get_member(member_id)
        if member:
            if name is not None:
                member['name'] = name
            if membership_status is not None:
                member['membership_status'] = membership_status
            return member
        return None

    def delete_member(self, member_id):
        member = self.get_member(member_id)
        if member:
            self.members.remove(member)
            return True
        return False

    def list_members(self):
        return self.members.copy()