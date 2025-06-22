import flet as ft
from decorators.roles_decorator import require_role


class ConfigurationFirstLoginView:
    def __init__(self, state):
        self.state = state
        state.current_role = self.state.current_role

    @require_role("Master")
    def render(self):
        manage_database_text = ft.Text("Manage database", theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD)
        create_database_button = ft.OutlinedButton(
            text="Create database",
            icon=ft.Icons.DATASET_OUTLINED,
            icon_color=ft.Colors.GREEN,
            visible=True,
            expand=True,
            width=float("inf"),
            style = ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.GREEN_50
                }
            )
        )
        delete_database_button = ft.OutlinedButton(
            text="Delete database",
            icon=ft.Icons.DELETE_FOREVER_OUTLINED,
            icon_color=ft.Colors.RED,
            visible=True,
            expand=True,
            width=float("inf"),
            style = ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.RED_100,
                    ft.ControlState.DEFAULT: ft.Colors.RED_50
                }
            )
        )

        manage_database_layout = ft.Container(
            expand=True,
            padding=10,
            bgcolor=ft.Colors.SURFACE,
            alignment=ft.alignment.center,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.ORANGE_400),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        [
                            ft.Icon(name=ft.Icons.DATASET_LINKED_OUTLINED, color=ft.Colors.BLUE),
                            manage_database_text
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.Container(create_database_button, expand=True),
                    ft.Container(delete_database_button, expand=True)
                ],
                spacing=10,
            )
        )


        build_layout = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=5,
            controls=[
                ft.Container(
                    expand=1,
                    bgcolor=ft.Colors.SURFACE,
                    content=manage_database_layout
                ),
                ft.Container(
                    expand=1,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Text("TEST")
                )
            ]

        )

        return ft.Container(
            expand=True,
            padding=5,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Column(
                [
                    build_layout
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )