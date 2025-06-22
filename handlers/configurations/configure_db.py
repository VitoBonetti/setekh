import json
from time import sleep
import pymysql
import os
from utils.initial_db_setup import execute_query
from handlers.configurations.sm_handler import sm_handler_connection


def db_config(state, host, port, user, password, db, step, e):
    if not host or not port or not user or not password or not db:
        state.conf_info_text.value = "One or more required parameters are missing."
        state.page.update()
        print("One or more required parameters are missing.")

    state.conf_info_progress.visible = True
    state.conf_info_progress.update()

    port = int(port)


    try:
        print("Try to connect")
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db)
        if conn:
            client, secret_path = sm_handler_connection(state)
            client.secrets.kv.v2.create_or_update_secret(
                path=f"{secret_path}/database",
                secret={
                    "host": host,
                    "port": port,
                    "user": user,
                    "password": password,
                    "db": db,
                },
                mount_point="secret"
            )
            print("Database connection tested")
            state.conf_info_text.value = "Connection successful."
            state.conf_info_text.update()

            config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
            with open(config_file_path) as config_file:
                json_config = json.load(config_file)

            json_config["step"] = "Step2"

            with open(config_file_path, "w") as f:
                json.dump(json_config, f, indent=4)
            sleep(1)

            state.conf_info_text.value = "Connection successful. Setting up database."
            state.conf_info_text.update()
            execute_query(conn)
            state.conf_info_progress.visible = False
            state.conf_info_progress.update()
            state.conf_info_text.value = "Database set up successfully."
            state.conf_info_text.update()
            sleep(1)
            state.page.go("/102")
        else:
            print("Database connection test failed.")
            state.conf_info_text.value = "Connection failed."
            state.conf_info_progress.visible = False
            state.conf_info_text.update()
            state.conf_info_progress.update()
            return
    except pymysql.MySQLError as err:
        print(err)
        state.conf_info_text.value = err.__str__()
        state.conf_info_progress.visible = False
        state.conf_info_text.update()
        state.conf_info_progress.update()
        return
    except Exception as e:
        print(e)
        state.conf_info_text.value = str(e)
        state.conf_info_progress.visible = False
        state.conf_info_text.update()
        state.conf_info_progress.update()
        return



