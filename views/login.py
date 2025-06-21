import flet as ft
from handlers.authentication.auth_flow import login, otp_login


class LoginView:
    def __init__(self, state):
        self.state = state

    def render(self):
        title_row = ft.Row(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(self.state.current_view_title, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
            ]
        )

        email_login_text_field = ft.TextField(expand=True, label="Email", border_radius=5, bgcolor=ft.Colors.SURFACE)
        password_login_text_field = ft.TextField(expand=True, label="Password", password=True, can_reveal_password=True,
                                                 border_radius=5, bgcolor=ft.Colors.SURFACE)
        login_info_text = ft.Text("", style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD)

        self.state.login_info_text = login_info_text
        self.state.email_login_text_field = email_login_text_field
        self.state.password_login_text_field = password_login_text_field

        login_button = ft.OutlinedButton(
            text="Login",
            icon=ft.Icons.LOGIN_OUTLINED,
            icon_color=ft.Colors.GREEN,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_50,
                    ft.ControlState.DEFAULT: ft.Colors.SURFACE
                }
            ),
            on_click=lambda e: login(email_login_text_field.value, password_login_text_field.value, self.state, e)
        )

        verify_code_login_text_field = ft.TextField(expand=True, label="Verify Code", border_radius=5,
                                                    bgcolor=ft.Colors.SURFACE, visible=False)
        verify_code_login_button = ft.OutlinedButton(
            text="Verify Code",
            icon=ft.Icons.BEENHERE_OUTLINED,
            icon_color=ft.Colors.GREEN,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.RED_50,
                    ft.ControlState.DEFAULT: ft.Colors.SURFACE
                }
            ),
            on_click=lambda e: otp_login(verify_code_login_text_field.value, self.state, e)
        )
        self.state.verify_code_login_button = verify_code_login_button
        self.state.verify_code_login_text_field = verify_code_login_text_field

        login_layout = ft.Container(
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
                        email_login_text_field,
                        password_login_text_field,
                        ft.Row([
                            ft.Container(expand=True),
                            login_button
                        ]),
                        ft.Row(
                            controls=[
                                login_info_text
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                verify_code_login_text_field,
                                verify_code_login_button
                            ],
                            spacing=10
                        ),
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
                    login_layout
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )
