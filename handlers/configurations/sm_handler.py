import json
import os
import hvac

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
secret_path = "setekh/"


def sm_handler_connection(state):
    if not os.path.exists(config_file_path):
        print("Vault config file not found")
        state.conf_info_text.value = "Vault config file not found"
        state.page.update()

    with open(config_file_path, "r") as f:
        vault_conf = json.load(f)

    vault_url = vault_conf.get("host")
    vault_token = vault_conf.get("secret")

    try:
        client = hvac.Client(url=vault_url, token=vault_token)
        if not client.is_authenticated():
            state.conf_info_text.value = "Vault authentication failed"
            state.page.update()

        return client, secret_path
    except Exception as e:
        print(f"Error authenticating with Vault API: {e}")
        state.conf_info_text.value = "Error authenticating with Vault API"
        state.page.update()
        return None


def retrieve_secret(state, secret_type):
    try:
        client, _ = sm_handler_connection(state)  # ignore saved secret_path from config
        read_response = client.secrets.kv.v2.read_secret_version(
            path=f"setekh/{secret_type}",
            mount_point="secret"
        )
        secret_data = read_response["data"]["data"]
        return secret_data

    except Exception as e:
        print(f"Error reading secret '{secret_type}': {e}")
        state.conf_info_text.value = f"Error retrieving {secret_type} credentials"
        state.page.update()
        return None
