class Member:
    def __init__(self, member_id, name, membership_status):
        self.member_id = member_id
        self.name = name
        self.membership_status = membership_status

    def activate_membership(self):
        self.membership_status = 'Active'

    def deactivate_membership(self):
        self.membership_status = 'Inactive'

    def __str__(self):
        return f'Member(ID: {self.member_id}, Name: {self.name}, Status: {self.membership_status})'