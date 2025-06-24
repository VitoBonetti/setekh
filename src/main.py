import flet as ft
import os
import json
from src.state import State
from handlers.authentication.auth_flow import is_session_valid
from helpers.check_path import check_path
from views.template import Template
from views.configuration.configuration_db import ConfigurationDBView
from views.configuration.configuration_master import MasterUserRegistration
from views.configuration.configuration_first_login import ConfigurationFirstLoginView
from views.configuration.configure_secret_manager import ConfigurationSecretManagerView
from views.configuration.configuration_email import ConfigurationEmailView
from views.assets import AssetsView
from views.blocks import BlocksView
from views.dashboard import DashboardView
from views.assessments import AssessmentsView
from views.vulnerabilities import VulnerabilitiesView
from views.login import LoginView
from views.unauthorized import UnauthorizedView



def main(page: ft.Page):
    state = State()
    page.title = f"{state.app_name} v.{state.app_version}"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.window_resizable = True
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)
    state.page = page
    page.state = state

    # get cookie if any
    state.session_id = state.page.client_storage.get("session_id")
    state.session_user_uuid = state.page.client_storage.get("user_uuid")

    # one inner‐view instance per route
    state.view_instances = {}
    # one rendered inner‐view control per route
    state.view_contents = {}

    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.conf'))

    # *** ONLY ONE TemplatePage FOR ALL ROUTES ***
    # we’ll swap out its content_view + selected_index on each nav
    tpl = Template(page, state, content_view=None, selected_index=0)
    state.template_page = tpl

    # map of routes → (title, view class)
    route_map = {
        "/": ("Dashboard", DashboardView),
        "/1": ("Blocks", BlocksView),
        "/2": ("Assets", AssetsView),
        "/3": ("Assessments", AssessmentsView),
        "/4": ("Vulnerability", VulnerabilitiesView),
        "/5": ("Settings", ConfigurationFirstLoginView),
        "/100": ("Configuration Secret Manager", ConfigurationSecretManagerView),
        "/101": ("Configuration DB Server", ConfigurationDBView),
        "/102": ("Registration Master User", MasterUserRegistration),
        "/103": ("Configuration SMTP Server", ConfigurationEmailView),
        "/104": ("Login", LoginView),
        "/401": ("Unauthorized", UnauthorizedView),
    }

    def route_change(e):
        route = page.route  # user-selected route

        title, ViewCls = route_map.get(route, ("Dashboard", DashboardView))
        state.current_view_title = title

        # 1) get-or-create the inner view instance
        if route not in state.view_instances:
            inst = ViewCls(state)
            state.view_instances[route] = inst
            # render once
            state.view_contents[route] = inst.render()
        content = state.view_contents[route]

        # 2) display logic
        page.views.clear()
        if route in ["/100", "/101", "/102", "/103", "/104", "/401"]:  # Skip template is if not logged user
            page.views.append(
                ft.View(
                    route=route,
                    controls=[content]
                )
            )
        else:
            # 3) update our single TemplatePage
            tpl.selected_index = int(route[1:]) if len(route) > 1 else 0
            tpl.content_view = content
            page.views.append(
                ft.View(
                    route=route,
                    controls=[tpl.render()]
                )
            )
        page.update()

    page.on_route_change = route_change

    if not check_path(config_file_path):
        page.go("/100")
    else:
        with open(config_file_path, "r") as f:
            conf_data = json.load(f)
            if conf_data["step"] == "Step1":
                page.go("/101")
            elif conf_data["step"] == "Step2":
                page.go("/102")
            elif conf_data["step"] == "Step3":
                page.go("/103")
            elif is_session_valid(state):
                page.go("/")
            else:
                page.go("/104")


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, host="127.0.0.1", port=8500)
