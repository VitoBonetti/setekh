import bcrypt


def hash_password(password):
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return hashed
    except Exception as e:
        print(e)
        return False


def compare_password(password1, password2):
    return password1 == password2
