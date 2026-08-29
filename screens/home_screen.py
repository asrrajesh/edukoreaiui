import flet as ft


def home_view(page: ft.Page):
    """Return the home view controls."""

    current_user = page.session.get("current_user") or ""

    def close_drawer(e=None):
        page.drawer.open = False
        page.update()

    def go_question_bank(e):
        close_drawer()
        page.go("/question_bank")

    def do_logout(e):
        page.session.remove("current_user")
        page.go("/login")

    def do_exit(e):
        close_drawer()
        page.window.close()

    # ── Navigation Drawer ─────────────────────────────────────────────
    drawer_header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.icons.SCHOOL, size=48, color=ft.colors.WHITE),
                ft.Text(
                    "MySchool",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                ),
                ft.Text(
                    current_user,
                    size=12,
                    color=ft.colors.with_opacity(0.80, ft.colors.WHITE),
                ),
            ],
            spacing=4,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#3949AB", "#5C6BC0"],
        ),
        padding=ft.padding.only(left=20, top=40, bottom=24, right=20),
        width=float("inf"),
    )

    page.drawer = ft.NavigationDrawer(
        controls=[
            drawer_header,
            ft.Divider(height=1),
            ft.ListTile(
                leading=ft.Icon(ft.icons.HELP_OUTLINE, color="#3949AB"),
                title=ft.Text("Question Bank"),
                on_click=go_question_bank,
            ),
            ft.Divider(height=1),
            ft.ListTile(
                leading=ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.RED_400),
                title=ft.Text("Exit"),
                on_click=do_exit,
            ),
        ],
    )

    # ── AppBar ────────────────────────────────────────────────────────
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.MENU,
            icon_color=ft.colors.WHITE,
            on_click=lambda e: setattr(page.drawer, "open", True) or page.update(),
        ),
        title=ft.Text("MySchool", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor="#3949AB",
        actions=[
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                icon_color=ft.colors.WHITE,
                tooltip="Logout",
                on_click=do_logout,
            ),
        ],
    )

    # ── Body ──────────────────────────────────────────────────────────
    body = ft.Column(
        controls=[
            ft.Container(expand=True),
            ft.Column(
                controls=[
                    ft.Icon(ft.icons.WAVING_HAND, size=64, color="#3949AB"),
                    ft.Text(
                        f"Welcome!",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1a237e",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Tap  ☰  to open the menu and navigate.",
                        size=14,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            ft.Container(expand=True),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=body,
        expand=True,
        bgcolor=ft.colors.GREY_50,
    )
