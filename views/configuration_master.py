import flet as ft
from handlers.configurations.create_master import register_master, verify_code


class MasterUserRegistration:
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

        email_text_field = ft.TextField(expand=True, label="Email", border_radius=5, bgcolor=ft.Colors.SURFACE)
        password1_text_field = ft.TextField(expand=True, label="Password", password=True, can_reveal_password=True,
                                            border_radius=5, bgcolor=ft.Colors.SURFACE)
        password2_text_field = ft.TextField(expand=True, label="Repeat Password", password=True,
                                            can_reveal_password=True, border_radius=5, bgcolor=ft.Colors.SURFACE)

        step2_info_progress = ft.ProgressRing(color=ft.Colors.ORANGE, width=25, height=25, stroke_width=2,
                                             tooltip="In Progress", visible=False)

        self.state.step2_info_progress = step2_info_progress

        step2_info_text = ft.Text("", style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD)
        self.state.step2_info_text = step2_info_text

        qr_code_image_control = ft.Image(
            src="",
            width=200,
            height=200,
            visible=False
        )
        self.state.qr_code_image_control = qr_code_image_control

        verify_code_text_field = ft.TextField(expand=True, label="Verify Code", border_radius=5, bgcolor=ft.Colors.SURFACE, visible=False)
        self.state.verify_code_text_field = verify_code_text_field
        verify_code_button = ft.OutlinedButton(
            text="Verify Code",
            icon=ft.Icons.BEENHERE_OUTLINED,
            icon_color=ft.Colors.GREEN,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_50,
                    ft.ControlState.DEFAULT: ft.Colors.SURFACE
                }
            ),
            on_click=lambda e: verify_code(self.state, e)
        )
        self.state.verify_code_button = verify_code_button
        create_user_layout = ft.Container(
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
                        email_text_field,
                        password1_text_field,
                        password2_text_field,
                        ft.Row([
                            ft.Container(expand=True),
                            ft.OutlinedButton(
                                text="Save",
                                icon=ft.Icons.INPUT_OUTLINED,
                                icon_color=ft.Colors.GREEN,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.GREEN_50,
                                        ft.ControlState.DEFAULT: ft.Colors.SURFACE
                                    }
                                ),
                                on_click=lambda e: register_master(email_text_field.value, password1_text_field.value, password2_text_field.value, self.state, e)
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
                                step2_info_progress,
                                step2_info_text
                            ],
                            spacing=10
                        ),
                        qr_code_image_control,
                        ft.Row(
                            controls=[
                                verify_code_text_field,
                                verify_code_button
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
                    create_user_layout
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )