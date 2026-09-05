import asyncio

import flet as ft
from database.db import get_scanned_chapter, save_scanned_chapter
from services.claude_ocr import extract_text_from_images


def setup_ebooks_view(page: ft.Page):
    """Return the Setup E-Books scan/review form as a single page."""
    selected_files = ft.Text("No images selected", color=ft.Colors.GREY_600, size=12)
    selected_image_files = []

    content_field = ft.TextField(
        label="Chapter Content",
        multiline=True,
        expand=True,
        min_lines=1,
        max_lines=None,
        text_size=13,
        value="",
    )

    def go_back(e):
        page.appbar = None
        page.drawer = None
        page.navigate("/home")

    async def load_existing_content(e=None):
        # Fetch and display saved content when class/subject/chapter are all selected.
        if class_dropdown.value and subject_dropdown.value and chapter_dropdown.value:
            record = await asyncio.to_thread(
                get_scanned_chapter,
                class_dropdown.value,
                subject_dropdown.value,
                chapter_dropdown.value,
            )
            content_field.value = record["content"] if record else ""
            page.update()

    # Compact styling so each dropdown label fits on one line inside a single row.
    dropdown_text_style = ft.TextStyle(size=13)
    dropdown_label_style = ft.TextStyle(size=12)
    dropdown_height = 44
    dropdown_padding = ft.Padding(left=6, top=4, right=2, bottom=4)

    def compact_label(text):
        # no_wrap keeps the caption on one line instead of breaking mid-word.
        return ft.Text(text, size=12, no_wrap=True)

    def dropdown_arrow():
        return ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18)

    class_dropdown = ft.Dropdown(
        label=compact_label("Class"),
        options=[ft.DropdownOption(text=roman) for roman in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]],
        expand=3,
        trailing_icon=dropdown_arrow(),
        selected_trailing_icon=dropdown_arrow(),
        dense=True,
        height=dropdown_height,
        content_padding=dropdown_padding,
        text_style=dropdown_text_style,
        label_style=dropdown_label_style,
        on_select=load_existing_content,
    )
    subject_dropdown = ft.Dropdown(
        label=compact_label("Subject"),
        options=[ft.DropdownOption(text=subject) for subject in ["Science", "English"]],
        expand=4,
        trailing_icon=dropdown_arrow(),
        selected_trailing_icon=dropdown_arrow(),
        dense=True,
        height=dropdown_height,
        content_padding=dropdown_padding,
        text_style=dropdown_text_style,
        label_style=dropdown_label_style,
        on_select=load_existing_content,
    )
    chapter_dropdown = ft.Dropdown(
        label=compact_label("Chapter"),
        options=[ft.DropdownOption(text=str(chapter)) for chapter in range(1, 51)],
        expand=4,
        trailing_icon=dropdown_arrow(),
        selected_trailing_icon=dropdown_arrow(),
        dense=True,
        height=dropdown_height,
        content_padding=dropdown_padding,
        text_style=dropdown_text_style,
        label_style=dropdown_label_style,
        on_select=load_existing_content,
    )

    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    async def choose_images(e):
        nonlocal selected_image_files
        files = await file_picker.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.IMAGE,
            with_data=True,
        )
        selected_image_files = files
        if files:
            selected_files.value = f"{len(files)} image(s) selected: " + ", ".join(
                file.name for file in files
            )
        else:
            selected_files.value = "No images selected"
        page.update()

    async def scan_chapters(e):
        if not class_dropdown.value or not subject_dropdown.value or not chapter_dropdown.value:
            page.show_dialog(ft.SnackBar(content=ft.Text("Select class, subject, and chapter."), bgcolor=ft.Colors.RED_600))
            return
        if not selected_image_files:
            page.show_dialog(ft.SnackBar(content=ft.Text("Attach at least one image."), bgcolor=ft.Colors.RED_600))
            return

        page.show_dialog(ft.SnackBar(content=ft.Text("Scanning images. This may take a moment."), bgcolor=ft.Colors.BLUE_700))
        try:
            content = await asyncio.to_thread(extract_text_from_images, selected_image_files)
        except Exception as exc:
            page.show_dialog(ft.SnackBar(content=ft.Text(f"Scan failed: {exc}"), bgcolor=ft.Colors.RED_600))
            return

        content_field.value = content
        page.update()

    async def submit_content(e):
        if not class_dropdown.value or not subject_dropdown.value or not chapter_dropdown.value:
            page.show_dialog(ft.SnackBar(content=ft.Text("Select class, subject, and chapter."), bgcolor=ft.Colors.RED_600))
            return
        content = (content_field.value or "").strip()
        if not content:
            page.show_dialog(ft.SnackBar(content=ft.Text("Add chapter content before submitting."), bgcolor=ft.Colors.RED_600))
            return

        page.show_dialog(ft.SnackBar(content=ft.Text("Saving chapter content..."), bgcolor=ft.Colors.BLUE_700))
        username = page.session.store.get("current_user") or ""
        result = await asyncio.to_thread(
            save_scanned_chapter,
            class_dropdown.value,
            subject_dropdown.value,
            chapter_dropdown.value,
            content,
            username,
        )
        if result["success"]:
            page.show_dialog(ft.SnackBar(content=ft.Text("Chapter content saved."), bgcolor=ft.Colors.GREEN_700))
            page.navigate("/home")
        else:
            page.show_dialog(ft.SnackBar(content=ft.Text(result["error"]), bgcolor=ft.Colors.RED_600))

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=go_back,
        ),
        title=ft.Text("Setup E-Books", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor="#3949AB",
    )
    page.drawer = None

    field_row_height = 34

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Scan E-Books pages", size=24, weight=ft.FontWeight.BOLD, color="#1a237e"),
                ft.Text("Choose the class, subject, chapter, and images to scan.", color=ft.Colors.GREY_600),
                ft.Row(
                    controls=[class_dropdown, subject_dropdown, chapter_dropdown],
                    spacing=8,
                ),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ATTACH_FILE, size=16),
                                    ft.Text("Attach Images", size=13),
                                ],
                                tight=True,
                                spacing=6,
                            ),
                            on_click=choose_images,
                            height=field_row_height,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(left=12, top=0, right=12, bottom=0),
                            ),
                        ),
                        ft.ElevatedButton(
                            content=ft.Text("SCAN", size=13),
                            on_click=scan_chapters,
                            style=ft.ButtonStyle(
                                bgcolor={"": "#3949AB"},
                                color={"": ft.Colors.WHITE},
                                padding=ft.Padding(left=20, top=0, right=20, bottom=0),
                            ),
                            height=field_row_height,
                        ),
                    ],
                    spacing=12,
                ),
                selected_files,
                ft.Container(content=content_field, expand=True),
                ft.ElevatedButton(
                    content="SUBMIT",
                    on_click=submit_content,
                    style=ft.ButtonStyle(bgcolor={"": "#3949AB"}, color={"": ft.Colors.WHITE}),
                    height=48,
                    width=float("inf"),
                ),
            ],
            spacing=12,
            expand=True,
        ),
        padding=24,
        expand=True,
        bgcolor=ft.Colors.GREY_50,
    )
