import flet as ft
import os
import json
from src.state import State
from handlers.authentication.auth_flow import is_session_valid
from helpers.check_path import check_path
from views.template import Template
from views.configuration_db import ConfigurationDBView
from views.configuration_master import MasterUserRegistration
from views.assets import AssetsView
from views.blocks import BlocksView
from views.dashboard import DashboardView
from views.assessments import AssessmentsView
from views.vulnerabilities import VulnerabilitiesView
from views.login import LoginView



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

    # one inner‐view instance per route
    state.view_instances = {}
    # one rendered inner‐view control per route
    state.view_contents = {}

    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))

    # *** ONLY ONE TemplatePage FOR ALL ROUTES ***
    # we’ll swap out its content_view + selected_index on each nav
    tpl = Template(page, state, content_view=None, selected_index=0)
    state.template_page = tpl

    # map of routes → (title, view class)
    route_map = {
        "/":  ("Configuration", ConfigurationDBView),
        "/1": ("Dashboard", DashboardView),
        "/2": ("Blocks", BlocksView),
        "/3": ("Assets", AssetsView),
        "/4": ("Assessments", AssessmentsView),
        "/5": ("Vulnerability", VulnerabilitiesView),
        "/100": ("Registration Master User", MasterUserRegistration),
        "/200": ("Login", LoginView),
    }

    def route_change(e):
        # figure out route key
        if not check_path(config_file_path):
            # no config.json → always show config view
            route = "/"
        else:
            with open(config_file_path, "r") as f:
                conf_data = json.load(f)
                if conf_data["step"] == "1":
                    page.go("/100")
                elif conf_data["step"] == "Done":
                    if is_session_valid(state):
                        # config exists
                        if page.route == "/":
                            # user is on "/" → immediately switch to dashboard
                            page.go("/1")
                            return
                    else:
                        page.go("/200")
            route = page.route

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
        if route in ["/", "/100", "/200"]:  # Skip template is if not logged user
            page.views.append(
                ft.View(
                    route=route,
                    controls=[content]
                )
            )
        else:
            # 3) update our single TemplatePage
            tpl.selected_index = (int(route[1:]) - 1) if len(route) > 1 else 0
            tpl.content_view = content
            page.views.append(
                ft.View(
                    route=route,
                    controls=[tpl.render()]
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route or ("/1" if check_path(config_file_path) else "/"))


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, host="127.0.0.1", port=8500)
