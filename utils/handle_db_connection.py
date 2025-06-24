import pymysql
from handlers.configurations.sm_handler import retrieve_secret


def connect_to_db(state):
    db_credentials = retrieve_secret(state, "database")
    if db_credentials:
        state.session_db = db_credentials
        host = db_credentials["host"]
        port = db_credentials["port"]
        user = db_credentials["user"]
        password = db_credentials["password"]
        dbname = db_credentials["db"]
    else:
        return None

    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=dbname)
        state.session_db = conn
        return conn
    except pymysql.MySQLError as err:
        print(err)
        return None
    except Exception as e:
        print(e)
        return None


