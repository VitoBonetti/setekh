import flet as ft
from handlers.configurations.configure_smtp import configure_smtp


class ConfigurationEmailView:
    def __init__(self, state):
        self.state = state

    def render(self):

        title_row = ft.Row(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(f"STEP 4 - {self.state.current_view_title}", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
            ]
        )

        smtp_text_field = ft.TextField(expand=True, label="SMTP IP Address", border_radius=5, bgcolor=ft.Colors.SURFACE)
        smtp_port_text_field = ft.TextField(expand=True, label="Port", border_radius=5, bgcolor=ft.Colors.SURFACE)
        smtp_user_text_field = ft.TextField(expand=True, label="User", border_radius=5, bgcolor=ft.Colors.SURFACE)
        smtp_password_text_field = ft.TextField(expand=True, label="Password", password=True, can_reveal_password=True, border_radius=5, bgcolor=ft.Colors.SURFACE)

        smtp_info_text = ft.Text("", style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD)
        self.state.smtp_info_text = smtp_info_text

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
                        smtp_text_field,
                        smtp_port_text_field,
                        smtp_user_text_field,
                        smtp_password_text_field,
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
                                on_click=lambda e: configure_smtp(self.state, smtp_text_field.value, smtp_port_text_field.value, smtp_user_text_field.value, smtp_password_text_field.value, "Done", e)
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
                                smtp_info_text
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