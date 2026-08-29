import flet as ft
from database.db import register_user


def signup_view(page: ft.Page):
    """Return the signup view controls."""
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
        helper_text="Minimum 8 characters",
        height=56,
        expand=True,
    )
    confirm_field = ft.TextField(
        label="Confirm Password",
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

    def do_signup(e):
        username = username_field.value.strip()
        password = password_field.value
        confirm = confirm_field.value

        if not username:
            show_snack("Please enter your email or mobile number.")
            return
        if not password:
            show_snack("Please enter a password.")
            return
        if password != confirm:
            show_snack("Passwords do not match.")
            return

        result = register_user(username, password)
        if result["success"]:
            show_snack("Account created! Please sign in.", color=ft.colors.GREEN_700)
            username_field.value = ""
            password_field.value = ""
            confirm_field.value = ""
            page.go("/login")
        else:
            show_snack(result["error"])

    def go_back(e):
        username_field.value = ""
        password_field.value = ""
        confirm_field.value = ""
        page.go("/login")

    # ── UI ───────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_color=ft.colors.WHITE,
                            on_click=go_back,
                        ),
                    ],
                ),
                ft.Text(
                    "Create Account",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                ),
                ft.Text(
                    "Join MySchool today",
                    size=14,
                    color=ft.colors.with_opacity(0.88, ft.colors.WHITE),
                ),
            ],
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#3949AB", "#5C6BC0"],
        ),
        padding=ft.padding.only(top=40, bottom=36, left=16, right=24),
        width=float("inf"),
    )

    card_content = ft.Container(
        content=ft.Column(
            controls=[
                username_field,
                ft.Container(height=4),
                password_field,
                ft.Container(height=4),
                confirm_field,
                ft.Container(height=12),
                ft.ElevatedButton(
                    text="CREATE ACCOUNT",
                    on_click=do_signup,
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
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Text("Already have an account?", size=13, color=ft.colors.GREY_600),
                        ft.TextButton(
                            "Sign In",
                            on_click=go_back,
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
