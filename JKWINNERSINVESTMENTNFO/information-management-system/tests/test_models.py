import unittest
from src.models.user import User
from src.models.member import Member
from src.models.division import Division

class TestModels(unittest.TestCase):

    def test_user_creation(self):
        user = User(id=1, username='testuser', password='securepassword')
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'testuser')
        self.assertIsNotNone(user.password)

    def test_member_creation(self):
        member = Member(id=1, name='John Doe', membership_status='active')
        self.assertEqual(member.id, 1)
        self.assertEqual(member.name, 'John Doe')
        self.assertEqual(member.membership_status, 'active')

    def test_division_creation(self):
        division = Division(id=1, name='Finance', description='Handles financial operations')
        self.assertEqual(division.id, 1)
        self.assertEqual(division.name, 'Finance')
        self.assertEqual(division.description, 'Handles financial operations')

if __name__ == '__main__':
    unittest.main()