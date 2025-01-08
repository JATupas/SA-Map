from datetime import date
import re

def validate_registration_form(data):
    errors = {}

    # Validate Full Name
    if not data.get('full_name') or len(data['full_name'].strip()) < 3:
        errors['full_name'] = "Full Name must be at least 3 characters long."

    # Validate Birthdate
    try:
        birthdate = date.fromisoformat(data.get('birthdate', ''))
        if birthdate >= date.today():
            errors['birthdate'] = "Birthdate must be in the past."
    except ValueError:
        errors['birthdate'] = "Invalid birthdate format."

    # Validate Email Address
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
        errors['email'] = "Invalid email address."

    # Validate PRC License
    if not data.get('prc_license') or not re.match(r'^\d{7}$', data['prc_license']):
        errors['prc_license'] = "PRC License must be a 7-digit number."

    # Validate Profession
    if not data.get('profession'):
        errors['profession'] = "Profession is required."

    return errors
