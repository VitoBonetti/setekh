import flet as ft
from handlers.authentication.auth_flow import logout


class Template:
    def __init__(self, page: ft.Page, state, content_view: ft.Control, selected_index: int):
        self.page = page
        self.state = state
        self.content_view = content_view
        self.selected_index = selected_index

        self.check_update_icon = ft.Icon(name=ft.Icons.VERIFIED_OUTLINED, tooltip="Up to date", color=ft.Colors.GREEN,
                                         size=20)
        state.check_update_icon = self.check_update_icon
        self.info_progress = ft.ProgressRing(color=ft.Colors.ORANGE, width=12,  height=12, stroke_width=2,
                                             tooltip="In Progress", visible=False)
        state.info_progress = self.info_progress
        self.account_icon = ft.Icon(name=ft.Icons.ACCOUNT_CIRCLE_OUTLINED, tooltip="Account", color=ft.Colors.BLUE,
                                    size=20)
        state.account_icon = self.account_icon
        self.logout_icon_button = ft.IconButton(icon=ft.Icons.LOGOUT_OUTLINED, icon_size=20,  icon_color=ft.Colors.GREEN, tooltip="Logout", on_click=lambda e: logout(self.state, e))
        state.logout_icon_button = self.logout_icon_button

    def render(self):
        def on_nav_change(e):
            self.page.go(f"/{e.control.selected_index + 1}")

        # Navigation Rail
        nav_rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.NONE,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icon(name=ft.Icons.DASHBOARD, tooltip="Dashboard", color=ft.Colors.BLUE), selected_icon=ft.Icon(name=ft.Icons.DASHBOARD_OUTLINED, tooltip="Dashboard", color=ft.Colors.GREEN), label="Dashboard"),
                ft.NavigationRailDestination(icon=ft.Icon(name=ft.Icons.ACCOUNT_TREE, tooltip="Blocks", color=ft.Colors.BLUE), selected_icon=ft.Icon(name=ft.Icons.ACCOUNT_TREE_OUTLINED, tooltip="Blocks", color=ft.Colors.GREEN), label="Blocks"),
                ft.NavigationRailDestination(icon=ft.Icon(name=ft.Icons.DIAMOND, tooltip="Assets", color=ft.Colors.BLUE), selected_icon=ft.Icon(name=ft.Icons.DIAMOND_OUTLINED, tooltip="Assets", color=ft.Colors.GREEN), label="Assets"),
                ft.NavigationRailDestination(icon=ft.Icon(name=ft.Icons.ASSIGNMENT, tooltip="Assessments", color=ft.Colors.BLUE), selected_icon=ft.Icon(name=ft.Icons.ASSIGNMENT_OUTLINED, tooltip="Assessments", color=ft.Colors.GREEN), label="Assessments"),
                ft.NavigationRailDestination(icon=ft.Icon(name=ft.Icons.BUG_REPORT, tooltip="Vulnerabilities", color=ft.Colors.BLUE), selected_icon=ft.Icon(name=ft.Icons.BUG_REPORT_OUTLINED, tooltip="Vulnerabilities", color=ft.Colors.GREEN), label="Vulnerabilities"),
            ],
            on_change=on_nav_change,
        )

        layout = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(width=80, content=nav_rail),
                ft.VerticalDivider(width=1, color=ft.Colors.BLUE),
                ft.Container(
                    expand=True,
                    padding=5,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(self.state.current_view_title, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, expand=True),
                            self.info_progress,
                            self.check_update_icon,
                            self.account_icon,
                            self.logout_icon_button
                        ]),
                        ft.Divider(),
                        self.content_view
                    ])
                )
            ]
        )

        return ft.Column(
            expand=True,
            controls=[
                layout,
                self.page.snack_bar  # Ensure the snackbar is always rendered
            ]
        )
