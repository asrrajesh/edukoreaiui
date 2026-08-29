import flet as ft
from database.db import login_user


def login_view(page: ft.Page):
    """Return the login view controls."""

    # ── State ────────────────────────────────────────────────────────
    username_field = ft.TextField(
        label="Email or Mobile Number",
        prefix_icon=ft.icons.PERSON_OUTLINE,
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        height=56,
        expand=True,
    )
    password_field = ft.TextField(
        label="Password",
        prefix_icon=ft.icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        height=56,
        expand=True,
    )

    def show_snack(msg: str, color=ft.colors.RED_600):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg, color=ft.colors.WHITE),
            bgcolor=color,
        )
        page.snack_bar.open = True
        page.update()

    def do_login(e):
        username = username_field.value.strip()
        password = password_field.value
        if not username:
            show_snack("Please enter your email or mobile number.")
            return
        if not password:
            show_snack("Please enter your password.")
            return

        result = login_user(username, password)
        if result["success"]:
            page.session.set("current_user", result["user"]["username"])
            username_field.value = ""
            password_field.value = ""
            page.go("/home")
        else:
            show_snack(result["error"])

    def go_forgot(e):
        page.go("/forgot_password")

    def go_signup(e):
        page.go("/signup")

    # ── UI ───────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.icons.SCHOOL, size=56, color=ft.colors.WHITE),
                ft.Text(
                    "MySchool",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                ),
                ft.Text(
                    "Learn. Grow. Succeed.",
                    size=15,
                    color=ft.colors.with_opacity(0.88, ft.colors.WHITE),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#3949AB", "#5C6BC0"],
        ),
        padding=ft.padding.only(top=52, bottom=36, left=24, right=24),
        width=float("inf"),
    )

    card_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Welcome Back", size=22, weight=ft.FontWeight.BOLD, color="#1a237e"),
                ft.Text("Sign in to continue", size=13, color=ft.colors.GREY_600),
                ft.Container(height=8),
                username_field,
                ft.Container(height=4),
                password_field,
                ft.Container(height=8),
                ft.ElevatedButton(
                    text="LOGIN",
                    on_click=do_login,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#3949AB"},
                        color={"": ft.colors.WHITE},
                        shape={"": ft.RoundedRectangleBorder(radius=12)},
                        elevation={"": 3},
                        text_style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                    ),
                    height=50,
                    width=float("inf"),
                ),
                ft.TextButton(
                    text="Forgot Password?",
                    on_click=go_forgot,
                    style=ft.ButtonStyle(color={"": "#3949AB"}),
                ),
                ft.Row(
                    controls=[
                        ft.Text("Don't have an account?", size=13, color=ft.colors.GREY_600),
                        ft.TextButton(
                            "Sign Up",
                            on_click=go_signup,
                            style=ft.ButtonStyle(color={"": "#3949AB"}),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
            ],
            spacing=10,
        ),
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.only(top_left=32, top_right=32),
        padding=ft.padding.symmetric(horizontal=28, vertical=32),
        expand=True,
    )

    return ft.Column(
        controls=[header, card_content],
        spacing=0,
        expand=True,
    )
