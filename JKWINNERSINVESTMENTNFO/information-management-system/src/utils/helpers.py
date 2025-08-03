def format_date(date_string):
    from datetime import datetime
    """Convert a date string to a standardized format."""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    except ValueError:
        return None

def generate_unique_id(existing_ids):
    """Generate a unique ID not present in the existing IDs."""
    import uuid
    new_id = str(uuid.uuid4())
    while new_id in existing_ids:
        new_id = str(uuid.uuid4())
    return new_id

def calculate_age(birthdate):
    from datetime import datetime
    """Calculate age based on the birthdate."""
    today = datetime.today()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def sanitize_input(input_string):
    """Remove any potentially harmful characters from input."""
    import re
    return re.sub(r'[^\w\s]', '', input_string)