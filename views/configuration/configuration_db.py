import flet as ft
from handlers.configurations.configure_db import db_config


class ConfigurationDBView:
    def __init__(self, state):
        self.state = state

    def render(self):

        title_row = ft.Row(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(f"STEP 2 - {self.state.current_view_title}", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
            ]
        )
        host_text_field = ft.TextField(expand=True, label="Host", border_radius=5, bgcolor=ft.Colors.SURFACE)
        port_text_field = ft.TextField(expand=True, label="Port", border_radius=5, bgcolor=ft.Colors.SURFACE)
        user_text_field = ft.TextField(expand=True, label="User", border_radius=5, bgcolor=ft.Colors.SURFACE)
        password_text_field = ft.TextField(expand=True, label="Password", password=True, can_reveal_password=True, border_radius=5, bgcolor=ft.Colors.SURFACE)
        database_text_field = ft.TextField(expand=True, label="Database", border_radius=5, bgcolor=ft.Colors.SURFACE)

        conf_info_progress = ft.ProgressRing(color=ft.Colors.ORANGE, width=25, height=25, stroke_width=2, tooltip="In Progress", visible=False)
        self.state.conf_info_progress = conf_info_progress
        conf_info_text = ft.Text("", style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD)
        self.state.conf_info_text = conf_info_text

        config_layout = ft.Container(
            expand=True,
            padding=10,
            bgcolor=ft.Colors.SURFACE,
            alignment=ft.alignment.center,
            content=ft.Container(
                width=400,
                padding=10,
                border_radius=5,
                bgcolor=ft.Colors.SURFACE,
                content=ft.Column(
                    controls=[
                        host_text_field,
                        port_text_field,
                        user_text_field,
                        password_text_field,
                        database_text_field,
                        ft.Row([
                            ft.Container(expand=True),
                            ft.OutlinedButton(
                                text="Save",
                                icon=ft.Icons.SAVE_OUTLINED,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREEN_50,
                                        ft.ControlState.DEFAULT: ft.Colors.SURFACE
                                    }
                                ),
                                on_click=lambda e: db_config(self.state, host_text_field.value, port_text_field.value, user_text_field.value, password_text_field.value, database_text_field.value, "1", e)
                            ),
                            ft.OutlinedButton(
                                text="Clear",
                                icon=ft.Icons.CLEAR,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.RED_50,
                                        ft.ControlState.DEFAULT: ft.Colors.SURFACE
                                    }
                                )
                            )
                        ]),
                        ft.Row(
                            controls=[
                                conf_info_progress,
                                conf_info_text
                            ],
                            spacing=10
                        )
                    ]
                )
            )
        )

        return ft.Container(
            expand=True,
            padding=5,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Column(
                [
                    title_row,
                    ft.Divider(color=ft.Colors.ORANGE),
                    config_layout
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )
