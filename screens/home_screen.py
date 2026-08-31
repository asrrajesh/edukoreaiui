import flet as ft


def home_view(page: ft.Page):
    """Return the home view controls."""

    current_user = page.session.store.get("current_user") or ""

    async def close_drawer(e=None):
        await page.close_drawer()

    async def go_question_bank(e):
        await close_drawer()
        page.navigate("/question_bank")

    def do_logout(e):
        page.session.store.remove("current_user")
        page.navigate("/login")

    async def drawer_logout(e):
        await close_drawer()
        do_logout(e)

    async def open_drawer(e):
        await page.show_drawer()

    # ── Navigation Drawer ─────────────────────────────────────────────
    drawer_header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.SCHOOL, size=48, color=ft.Colors.WHITE),
                ft.Text(
                    "MySchool",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    current_user,
                    size=12,
                    color=ft.Colors.with_opacity(0.80, ft.Colors.WHITE),
                ),
            ],
            spacing=4,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#3949AB", "#5C6BC0"],
        ),
        padding=ft.Padding(left=20, top=40, bottom=24, right=20),
        width=float("inf"),
    )

    page.drawer = ft.NavigationDrawer(
        controls=[
            drawer_header,
            ft.Divider(height=1),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HELP_OUTLINE, color="#3949AB"),
                title=ft.Text("Question Bank"),
                on_click=go_question_bank,
            ),
            ft.Divider(height=1),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400),
                title=ft.Text("Logout"),
                on_click=drawer_logout,
            ),
        ],
    )

    # ── AppBar ────────────────────────────────────────────────────────
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color=ft.Colors.WHITE,
            on_click=open_drawer,
        ),
        title=ft.Text("MySchool", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor="#3949AB",
        actions=[
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
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
                    ft.Icon(ft.Icons.WAVING_HAND, size=64, color="#3949AB"),
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
                        color=ft.Colors.GREY_600,
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
        bgcolor=ft.Colors.GREY_50,
    )
