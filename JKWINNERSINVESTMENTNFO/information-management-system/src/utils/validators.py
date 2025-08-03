def is_valid_username(username):
    if not isinstance(username, str):
        return False
    if len(username) < 3 or len(username) > 20:
        return False
    if not username.isalnum():
        return False
    return True

def is_valid_password(password):
    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    return True

def is_valid_member_name(name):
    if not isinstance(name, str):
        return False
    if len(name) < 1 or len(name) > 50:
        return False
    return True

def is_valid_division_name(name):
    if not isinstance(name, str):
        return False
    if len(name) < 1 or len(name) > 100:
        return False
    return True