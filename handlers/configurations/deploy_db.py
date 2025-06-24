import flet as ft
from utils.handle_db_connection import connect_to_db
from queries.queries import CREATE_MAP_USER_BLOCK_ROLE, INSERT_ROLES, SELECT_CONFIG_UUID, UPDATE_INITIAL_CONFIG_BIS
import uuid
from time import sleep

ROLES = ["Manager", "Client", "Guest"]


def deploy_db(state):
    print("Deploying DB")
    try:
        if not state.session_db:
            print("NO conn yet")
            conn = connect_to_db(state)
            state.session_db = conn
        else:
            print("FOUND conn")
            conn = state.session_db

        cursor = conn.cursor()
        for role in ROLES:
            try:
                cursor.execute(INSERT_ROLES, (str(uuid.uuid4()), role))
                conn.commit()
            except Exception as e:
                pass

        try:
            cursor.execute(CREATE_MAP_USER_BLOCK_ROLE)
            conn.commit()
        except Exception as e:
            pass

        cursor.execute(SELECT_CONFIG_UUID)
        row = cursor.fetchone()
        uuid_to_update = row[0]
        cursor.execute(UPDATE_INITIAL_CONFIG_BIS, (uuid_to_update,))
        conn.commit()

        sleep(1)
        state.page.go("/")

    except Exception as e:
        print(f"DEPLOY DB ERROR: {e}")
        pass
        # return False




