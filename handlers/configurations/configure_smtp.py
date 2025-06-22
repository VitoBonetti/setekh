import json
from time import sleep
import os
from helpers.check_smtp import check_smtp
from handlers.configurations.sm_handler import sm_handler_connection
from utils.handle_db_connection import connect_to_db
from queries.queries import SELECT_CONFIG_UUID, UPDATE_INITIAL_CONFIG


def configure_smtp(state, smtp, port, email, password, step, e):
    if not smtp or not port or not email or not password:
        state.smtp_info_text.value = "One or more required parameters are missing."
        state.page.update()
        print("One or more required parameters are missing.")
        return

    if not check_smtp(smtp, port, email, password):
        state.smtp_info_text.value = "It was not possible to connect to the SMTP server."
        state.page.update()
        return

    port = int(port)

    try:
        client, secret_path = sm_handler_connection(state)
        client.secrets.kv.v2.create_or_update_secret(
            path=f"{secret_path}/smtp",
            secret={
                "server": smtp,
                "port": port,
                "email": email,
                "password": password,
            },
            mount_point="secret"
        )
        state.smtp_info_text.value = "Connection Established."
        state.smtp_info_text.update()

        config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
        with open(config_file_path) as config_file:
            json_config = json.load(config_file)

        json_config["step"] = step

        with open(config_file_path, "w") as f:
            json.dump(json_config, f, indent=4)
        sleep(1)

        conn = connect_to_db(state)
        cursor = conn.cursor()
        cursor.execute(SELECT_CONFIG_UUID)
        row = cursor.fetchone()
        uuid = row[0]

        cursor.execute(UPDATE_INITIAL_CONFIG, (uuid))
        conn.commit()
        cursor.close()
        conn.close()

        state.smtp_info_text.value = "All set up. Redirect to login"
        state.page.update()
        sleep(3)
        state.page.go("/104")
    except Exception as e:
        print(e)
        state.smtp_info_text.value = str(e)
        state.page.update()
        return




