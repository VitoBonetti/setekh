import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class State:
    def __init__(self):
        self.app_name = "Setekh"
        self.app_version = "0.0.1"
        self.current_view_title = "Dashboard"
        self.project_root = project_root
        self.is_config = False
        self.config_state = None
        self.current_role = None
        self.session_id = None
        self.session_user_uuid = None
