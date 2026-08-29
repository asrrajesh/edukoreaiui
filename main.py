import flet as ft
from screens.login_screen import login_view
from screens.signup_screen import signup_view
from screens.forgot_password_screen import forgot_password_view
from screens.home_screen import home_view
from screens.question_bank_screen import question_bank_view
from config.config import (
    APP_TITLE,
    THEME_COLOR,
    BACKGROUND_COLOR,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_RESIZABLE,
)


def main(page: ft.Page):
    page.title = APP_TITLE
    page.theme = ft.Theme(color_scheme_seed=THEME_COLOR)
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = WINDOW_RESIZABLE

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.appbar = None
        page.drawer = None

        route = e.route

        if route == "/login" or route == "/":
            page.views.append(
                ft.View(
                    "/login",
                    controls=[login_view(page)],
                    padding=0,
                    bgcolor=ft.colors.WHITE,
                )
            )
        elif route == "/signup":
            page.views.append(
                ft.View(
                    "/signup",
                    controls=[signup_view(page)],
                    padding=0,
                    bgcolor=ft.colors.WHITE,
                )
            )
        elif route == "/forgot_password":
            page.views.append(
                ft.View(
                    "/forgot_password",
                    controls=[forgot_password_view(page)],
                    padding=0,
                    bgcolor=ft.colors.WHITE,
                )
            )
        elif route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    controls=[home_view(page)],
                    padding=0,
                    appbar=page.appbar,
                    drawer=page.drawer,
                    bgcolor=ft.colors.GREY_50,
                )
            )
        elif route == "/question_bank":
            page.views.append(
                ft.View(
                    "/question_bank",
                    controls=[question_bank_view(page)],
                    padding=ft.padding.symmetric(horizontal=24, vertical=16),
                    appbar=page.appbar,
                    bgcolor=ft.colors.GREY_50,
                )
            )

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main)
