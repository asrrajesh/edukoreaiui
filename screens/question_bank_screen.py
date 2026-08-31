import flet as ft


def question_bank_view(page: ft.Page):
    """Return the question bank view controls."""

    def go_back(e):
        page.appbar = None
        page.drawer = None
        page.navigate("/home")

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=go_back,
        ),
        title=ft.Text("Question Bank", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor="#3949AB",
    )
    page.drawer = None

    return ft.Column(
        controls=[
            ft.Container(expand=True),
            ft.Column(
                controls=[
                    ft.Icon(ft.Icons.HELP_OUTLINE, size=80, color="#3949AB"),
                    ft.Text(
                        "Question Bank",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1a237e",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Coming Soon!",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "This section is under construction.\nStay tuned for exciting content.",
                        size=14,
                        color=ft.Colors.GREY_500,
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
