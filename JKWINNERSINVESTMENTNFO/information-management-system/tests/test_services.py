import unittest
from src.services.member_service import MemberService

class TestMemberService(unittest.TestCase):

    def setUp(self):
        self.member_service = MemberService()

    def test_create_member(self):
        # Test creating a member
        member_data = {'name': 'John Doe', 'status': 'active'}
        member = self.member_service.create_member(member_data)
        self.assertIsNotNone(member)
        self.assertEqual(member.name, 'John Doe')
        self.assertEqual(member.status, 'active')

    def test_get_member(self):
        # Test retrieving a member
        member_data = {'name': 'Jane Doe', 'status': 'active'}
        member = self.member_service.create_member(member_data)
        retrieved_member = self.member_service.get_member(member.id)
        self.assertEqual(retrieved_member.name, 'Jane Doe')

    def test_update_member(self):
        # Test updating a member
        member_data = {'name': 'John Smith', 'status': 'inactive'}
        member = self.member_service.create_member(member_data)
        updated_member = self.member_service.update_member(member.id, {'status': 'active'})
        self.assertEqual(updated_member.status, 'active')

    def test_delete_member(self):
        # Test deleting a member
        member_data = {'name': 'Mark Twain', 'status': 'active'}
        member = self.member_service.create_member(member_data)
        result = self.member_service.delete_member(member.id)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()