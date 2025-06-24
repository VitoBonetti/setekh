import flet as ft
from handlers.dashboard.loading_test import testing_data
from handlers.dashboard.master_dashboard import generate_master_dashboard


class DashboardView:
    def __init__(self, state):
        self.state = state
        self.testing_data = testing_data(self.state)
        self.current_role = self.state.current_role

    def render(self):
        if self.current_role == "Master":
           dashboard = generate_master_dashboard(self.state)

        else:
            dashboard = ft.Container(
            expand=True,
            padding=5,
            content=ft.Column(
                [
                    ft.Text(self.state.current_view_title),
                    ft.Text(self.state.current_role),
                    ft.Column(
                        controls=self.testing_data
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        )

        return dashboard
