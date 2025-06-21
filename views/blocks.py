import flet as ft


class BlocksView:
    def __init__(self, state):
        self.state = state

    def render(self):
        return ft.Container(
            expand=True,
            padding=5,
            bgcolor=ft.Colors.BLUE_50,
            content=ft.Column(
                [
                    ft.Text(self.state.current_view_title),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )
