import json
import os
from time import sleep


def sm_config(state, host, port, role_id, secret_id, step, e):
    if not host or not port or not role_id or not secret_id or not step:
        state.secret_info_text.value = "One or more required parameters are missing."
        state.page.update()
        print("One or more required parameters are missing.")

    port = int(port)
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.conf'))
    full_host = f"http://{host}:{port}"
    try:
        config_json = {"host": full_host, "role_id": role_id, "secret_id": secret_id, "step": step}
        with open(config_file_path, 'w') as config_file:
            json.dump(config_json, config_file, indent=4)

        sleep(1)
        state.page.go("/101")
    except Exception as err:
        print(err)
        state.secret_info_text.value = err.__str__()
        state.page.update()
        return
