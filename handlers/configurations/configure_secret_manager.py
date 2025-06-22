import json
import os
from time import sleep


def sm_config(state, host, port, secret, step, e):
    if not host or not port or not secret or not step:
        state.secret_info_text.value = "One or more required parameters are missing."
        state.page.update()
        print("One or more required parameters are missing.")

    port = int(port)
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
    full_host = f"http://{host}:{port}"
    try:
        config_json = {"host": full_host, "secret": secret, "step": step}
        with open(config_file_path, 'w') as config_file:
            json.dump(config_json, config_file, indent=4)

        state.secret_info_text.value = "One or more required parameters are missing."
        state.page.update()
        sleep(1)
        state.page.go("/101")
    except Exception as err:
        print(err)
        state.secret_info_text.value = err.__str__()
        state.page.update()
        return
