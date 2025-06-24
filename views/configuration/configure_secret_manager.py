import flet as ft
from handlers.configurations.configure_secret_manager import sm_config


class ConfigurationSecretManagerView:
    def __init__(self, state):
        self.state = state

    def render(self):
        title_row = ft.Row(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(f"STEP 1: {self.state.current_view_title}", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
            ]
        )

        secret_host_text_field = ft.TextField(expand=True, label="Host", border_radius=5, bgcolor=ft.Colors.SURFACE)
        secret_port_text_field = ft.TextField(expand=True, label="Port", border_radius=5, bgcolor=ft.Colors.SURFACE)
        secret_role_id_text_field = ft.TextField(expand=True, label="Role ID", border_radius=5, bgcolor=ft.Colors.SURFACE)
        secret_secret_id_text_field = ft.TextField(expand=True, label="Secret ID", password=True, can_reveal_password=True, border_radius=5, bgcolor=ft.Colors.SURFACE)
        secret_info_text = ft.Text("", style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD)
        self.state.secret_info_text = secret_info_text

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
                        secret_host_text_field,
                        secret_port_text_field,
                        secret_role_id_text_field,
                        secret_secret_id_text_field,
                        ft.Row([
                            ft.Container(expand=True),
                            ft.OutlinedButton(
                                text="Save and Continue",
                                icon=ft.Icons.SAVE_OUTLINED,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREEN_50,
                                        ft.ControlState.DEFAULT: ft.Colors.SURFACE
                                    }
                                ),
                                on_click=lambda e: sm_config(self.state, secret_host_text_field.value, secret_port_text_field.value, secret_role_id_text_field.value, secret_secret_id_text_field.value, "Step1", e),
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
                        secret_info_text
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