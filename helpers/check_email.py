from email_validator import validate_email, EmailNotValidError


def check_email(email):
    if not email:
        return False

    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        print(e)
        return False
