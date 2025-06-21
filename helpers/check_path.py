import os


def check_path(path):
    try:
        return os.path.exists(path)
    except Exception as e:
        print(e)
        return False
