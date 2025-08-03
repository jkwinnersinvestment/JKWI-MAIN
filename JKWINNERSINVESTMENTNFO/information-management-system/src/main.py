# main.py

from database.connection import connect_to_database
from controllers.user_controller import UserController
from controllers.member_controller import MemberController
from controllers.division_controller import DivisionController

def main():
    # Initialize database connection
    connect_to_database()

    # Initialize controllers
    user_controller = UserController()
    member_controller = MemberController()
    division_controller = DivisionController()

    # Start the main application loop
    while True:
        print("Welcome to the Information Management System")
        print("1. User Management")
        print("2. Member Management")
        print("3. Division Management")
        print("4. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            user_controller.handle_user_requests()
        elif choice == '2':
            member_controller.handle_member_requests()
        elif choice == '3':
            division_controller.handle_division_requests()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()