class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self, username, password):
        return self.user_service.create_user(username, password)

    def get_user(self, user_id):
        return self.user_service.get_user(user_id)

    def delete_user(self, user_id):
        return self.user_service.delete_user(user_id)