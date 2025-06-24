import flet as ft
from utils.handle_db_connection import connect_to_db


def testing_data(state):
    testing_content = []
    if not state.session_db:
        print("NO conn yet")
        conn = connect_to_db(state)
        state.session_db = conn
    else:
        print("FOUND conn")
        conn = state.session_db
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    row = cursor.fetchone()

    for item in row:
        test = ft.Text(item)
        testing_content.append(test)

    # cursor.close()
    # conn.close()
    return testing_content
