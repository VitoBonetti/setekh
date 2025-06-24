from handlers.configurations.deploy_db import deploy_db


def buttons_map(state, button, e):
    print(f"BUTTON MAPS PRESS: {button}")
    if button == "deploydb":
        deploy_db(state)