import re

def validate_email(email):
    """
    Validates the email format.
    Returns True if valid, False otherwise.
    """
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def validate_phone_number(phone):
    """
    Validates the phone number format.
    Accepts numbers with optional + and country code.
    Returns True if valid, False otherwise.
    """
    phone_regex = r'^\+?\d{7,15}$'
    return re.match(phone_regex, phone) is not None
