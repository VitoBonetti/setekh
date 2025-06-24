import flet as ft
from utils.handle_db_connection import connect_to_db
from handlers.dashboard.buttons_map import buttons_map
from queries.queries import SELECT_INITIAL_CONFIG_TABLE, COUNT_USER_ROLES, COUNT_USER_BLOCKS


def check_and_return_settings_state(state, dict, value):
    if dict[value]:
        cell_check = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            expand=True,
            controls=[
                ft.Icon(name=ft.Icons.CHECK_OUTLINED, color=ft.Colors.GREEN, size=18),
                ft.IconButton(
                    tooltip="Edit",
                    icon_size=18,
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color=ft.Colors.BLUE,
                    visible=True,
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.HOVERED: ft.Colors.BLUE_100,
                            ft.ControlState.DEFAULT: ft.Colors.BLUE_50
                        }
                    )
                )
            ]
        )
    else:
        cell_check = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            expand=True,
            controls=[
                ft.Icon(name=ft.Icons.CANCEL_OUTLINED, color=ft.Colors.RED, size=18),
                ft.IconButton(
                    tooltip="Deploy",
                    icon_size=18,
                    icon=ft.Icons.COMMIT_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    visible=True,
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                            ft.ControlState.DEFAULT: ft.Colors.GREEN_50
                        }
                    ),
                    on_click=lambda e: buttons_map(state, value, e)
                )
            ]

        )


    return cell_check


def configuration_status(state, info):
    title_config_status = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Configuration Status", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,  weight=ft.FontWeight.BOLD)
        ]
    )

    config_main_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("Secret Server", italic=True, weight=ft.FontWeight.BOLD),
                        check_and_return_settings_state(state, info, "secret"),
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("SQL Server", italic=True, weight=ft.FontWeight.BOLD),
                        check_and_return_settings_state(state, info, "initialdb"),
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("SMTP Server", italic=True, weight=ft.FontWeight.BOLD),
                        check_and_return_settings_state(state, info, "email"),
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("Master User", italic=True, weight=ft.FontWeight.BOLD),
                        check_and_return_settings_state(state, info, "masteruser"),
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("Deploy DB", italic=True, weight=ft.FontWeight.BOLD),
                        check_and_return_settings_state(state, info, "deploydb"),
                    ]
                )
            ),
        ]
    )

    return ft.Column(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            title_config_status,
            ft.Divider(color=ft.Colors.ORANGE),
            config_main_row
        ]
    )


def total_user_per_role(state, info):
    if info:
        row_list = []
        for role_name, role_count in info:
            row_list.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(role_name)),
                        ft.DataCell(ft.Text(str(role_count)))
                    ]
                )
            )

        title_total_user_per_role = ft.Text("Users per role", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                               weight=ft.FontWeight.BOLD)
        table_total_user_per_role = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Role", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("User", weight=ft.FontWeight.BOLD))
            ],
            rows=row_list,
        )

        second_col = ft.Container(
            border=ft.border.all(1, ft.Colors.ORANGE),
            border_radius=15,
            padding=10,
            content=ft.Column(
                spacing=5,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    title_total_user_per_role,
                    ft.Divider(color=ft.Colors.ORANGE),
                    table_total_user_per_role
                ]
            )
        )
        return second_col
    else:
        print("Nothing")
        return None


def total_user_per_block(state, info):
    if info:
        row_list = []
        for blocks_name, user_count in info:
            row_list.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(blocks_name)),
                        ft.DataCell(ft.Text(str(user_count)))
                    ]
                )
            )

        title_total_user_per_block = ft.Text("Users per Blocks", theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                               weight=ft.FontWeight.BOLD)
        table_total_user_per_block = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Block", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("User", weight=ft.FontWeight.BOLD))
            ],
            rows=row_list,
        )

        third_col = ft.Container(
            border=ft.border.all(1, ft.Colors.ORANGE),
            border_radius=15,
            padding=10,
            content=ft.Column(
                spacing=5,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    title_total_user_per_block,
                    ft.Divider(color=ft.Colors.ORANGE),
                    table_total_user_per_block
                ]
            )
        )
        return third_col
    else:
        print("Nothing")
        return None


def generate_master_dashboard(state):
    config_info = None
    try:
        if not state.session_db:
            print("NO conn yet")
            conn = connect_to_db(state)
            state.session_db = conn
        else:
            print("FOUND conn")
            conn = state.session_db
        cursor = conn.cursor()
        cursor.execute(SELECT_INITIAL_CONFIG_TABLE)
        column_names = [description[0] for description in cursor.description]
        config_info_tuple  = cursor.fetchone()

        cursor.execute(COUNT_USER_ROLES)
        user_per_role_info = cursor.fetchall()
        second_col = total_user_per_role(state, user_per_role_info)

        cursor.execute(COUNT_USER_BLOCKS)
        user_per_block_info = cursor.fetchall()
        third_col = total_user_per_block(state, user_per_block_info)

        if config_info_tuple:
            config_info = dict(zip(column_names, config_info_tuple))
        else:
            config_info = {}

        config_row = configuration_status(state, config_info)

    except Exception as e:
        print(f"Generate Master dashboard DB connection ERROR: {e}")

    # == NAVIGATION FUNCTION ==

    title_nav_func = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Navigation Functions", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD)
        ]
    )

    nav_func = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.OutlinedButton(
                            text="Add User",
                            icon=ft.Icons.PERSON_ADD_OUTLINED,
                            icon_color=ft.Colors.ORANGE,
                            visible=True,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                                    ft.ControlState.DEFAULT: ft.Colors.ORANGE_50
                                }
                            )
                        )
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.OutlinedButton(
                            text="Add Block",
                            icon=ft.Icons.ACCOUNT_TREE_OUTLINED,
                            icon_color=ft.Colors.ORANGE,
                            visible=True,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                                    ft.ControlState.DEFAULT: ft.Colors.ORANGE_50
                                }
                            )
                        )
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.OutlinedButton(
                            text="Add Asset",
                            icon=ft.Icons.DIAMOND_OUTLINED,
                            icon_color=ft.Colors.ORANGE,
                            visible=True,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                                    ft.ControlState.DEFAULT: ft.Colors.ORANGE_50
                                }
                            )
                        )
                    ]
                )
            ),
            ft.Container(
                expand=1,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.OutlinedButton(
                            text="Add Assessments",
                            icon=ft.Icons.ASSIGNMENT_OUTLINED,
                            icon_color=ft.Colors.ORANGE,
                            visible=True,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                                    ft.ControlState.DEFAULT: ft.Colors.ORANGE_50
                                }
                            )
                        )
                    ]
                )
            )
        ]
    )

    nav_row = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            title_nav_func,
            ft.Divider(color=ft.Colors.ORANGE),
            nav_func
        ]
    )

    # == NAVIGATION FUNCTION END ==

    first_col = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                expand=1,
                border=ft.border.all(1, ft.Colors.ORANGE),
                border_radius=15,
                padding=10,
                content=nav_row
            ),
            ft.Container(
                expand=1,
                border=ft.border.all(1, ft.Colors.ORANGE),
                border_radius=15,
                padding=10,
                content=config_row
            )
        ]
    )

    return ft.Column(
       [
           ft.Container(
               bgcolor=ft.Colors.YELLOW_50,
               expand=True,
               padding=5,
               content=ft.Column(
                   [
                       first_col
                   ],
                   alignment=ft.MainAxisAlignment.START,
                   scroll=ft.ScrollMode.AUTO,
                   expand=True,
               )
           ),
           ft.Row(
               alignment=ft.MainAxisAlignment.START,
               vertical_alignment=ft.CrossAxisAlignment.START,
               controls=[
                   ft.Container(
                       bgcolor=ft.Colors.CYAN_50,
                       expand=1,
                       padding=5,
                       content=ft.Column(
                           [
                               second_col
                           ],
                           alignment=ft.MainAxisAlignment.START,
                           scroll=ft.ScrollMode.AUTO,
                           expand=True,
                       )
                   ),
                   ft.Container(
                       bgcolor=ft.Colors.INDIGO_50,
                       expand=1,
                       padding=5,
                       content=ft.Column(
                           [
                               third_col
                           ],
                           alignment=ft.MainAxisAlignment.START,
                           scroll=ft.ScrollMode.AUTO,
                           expand=True,
                       )
                   )
               ]
           )
       ],
       alignment=ft.MainAxisAlignment.START
   )

