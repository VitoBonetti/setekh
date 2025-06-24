import json
import os
import hvac

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.conf'))
secret_path = "setekh/"


def sm_handler_connection():
    if not os.path.exists(config_file_path):
        print("Vault config file not found")
        return None

    with open(config_file_path, "r") as f:
        vault_conf = json.load(f)

    vault_url = vault_conf.get("host")
    vault_role = vault_conf.get("role_id")
    vault_secret = vault_conf.get("secret_id")

    try:
        client = hvac.Client(url=vault_url)

        # If client.token is accidentally overwritten
        if isinstance(client.token, str):
            print("client.token was overwritten! creating clean client...")
            # recreate a new client, don't try to fix the old one
            client = hvac.Client(url=vault_url)

        # Authenticate with AppRole
        auth_response = client.auth.approle.login(role_id=vault_role, secret_id=vault_secret)

        if not client.is_authenticated():
            raise Exception("Vault authentication failed")

        try:
            token_info = client.lookup_token()

            if token_info["data"].get("renewable", False):
                try:
                    renewed = client.token.renew_self(increment="30m")
                    print(f"Token renewed. TTL: {renewed['auth']['lease_duration']}s")
                except Exception as renew_error:
                    print(f"Token renewal failed: {renew_error}")
                    # Retry full re-auth
                    client = hvac.Client(url=vault_url)
                    auth_response = client.auth.approle.login(role_id=vault_role, secret_id=vault_secret)
                    if not client.is_authenticated():
                        raise Exception("Re-authentication after renewal failed")

        except hvac.exceptions.InvalidRequest as token_error:
            print(f"Token check failed: {token_error}")
            # Retry full auth again
            client = hvac.Client(url=vault_url)
            client.auth.approle.login(role_id=vault_role, secret_id=vault_secret)
            if not client.is_authenticated():
                raise Exception("Re-authentication after token check failed")

        return client, secret_path

    except Exception as e:
        print(f"Error authenticating with Vault API: {e}")
        return None


def retrieve_secret(state, secret_type):
    connection = sm_handler_connection()
    if not connection:
        print("Failed to connect to Vault — no client returned.")
        return None

    client, _ = connection
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path=f"setekh/{secret_type}",
            mount_point="secret"
        )
        return read_response["data"]["data"]

    except Exception as e:
        print(f"Error reading secret '{secret_type}': {e}")
        return None
