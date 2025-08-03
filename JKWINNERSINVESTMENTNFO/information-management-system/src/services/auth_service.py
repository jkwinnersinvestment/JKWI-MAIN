class AuthService:
    def __init__(self):
        self.users = {}  # This will hold user data in a dictionary for demonstration purposes

    def login(self, username, password):
        """Authenticate a user with username and password."""
        user = self.users.get(username)
        if user and user['password'] == password:
            return {"message": "Login successful", "user": user}
        return {"message": "Invalid username or password"}

    def logout(self, username):
        """Log out a user."""
        if username in self.users:
            return {"message": f"{username} logged out successfully"}
        return {"message": "User not found"}

    def register(self, username, password):
        """Register a new user."""
        if username in self.users:
            return {"message": "Username already exists"}
        self.users[username] = {"username": username, "password": password}
        return {"message": "User registered successfully"}