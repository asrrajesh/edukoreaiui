import asyncio
import flet as ft
from services.api_client import get_classes, get_chapters, get_subjects

# (key, label) — label is the text shown to the user in the dropdown
QUESTION_TYPES = [
    ("mcq", "Choose the correct answer"),
    ("short", "Answer the following questions (Short)"),
    ("long", "Answer the following questions (Long)"),
]


class QuestionRow:
    """One repeater row: question type, count, marks and the computed row total."""

    def __init__(self, on_type_change, on_remove, on_recalc):
        self._on_type_change = on_type_change
        self._on_remove = on_remove
        self._on_recalc = on_recalc

        self.type_dropdown = ft.Dropdown(
            label="Question Type",
            options=[],
            width=260,
            on_select=lambda e: self._on_type_change(),
        )
        self.count_field = ft.TextField(
            label="Question Count",
            width=140,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self._on_recalc(),
        )
        self.marks_field = ft.TextField(
            label="Marks Per Question",
            width=160,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self._on_recalc(),
        )
        self.total_text = ft.Text("0", size=15, weight=ft.FontWeight.BOLD, color="#1a237e")
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            tooltip="Remove row",
            on_click=lambda e: self._on_remove(self),
        )

        self.row_control = ft.Container(
            content=ft.Row(
                controls=[
                    self.type_dropdown,
                    self.count_field,
                    self.marks_field,
                    ft.Column(
                        controls=[
                            ft.Text("Row Total", size=11, color=ft.Colors.GREY_600),
                            self.total_text,
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    self.delete_button,
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=True,
            ),
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=10,
        )

    def refresh_total(self):
        self.total_text.value = self._compute_total_display()

    def _compute_total_display(self) -> str:
        try:
            count = int(self.count_field.value)
            marks = float(self.marks_field.value)
            if count <= 0 or marks <= 0:
                return "0"
            return f"{count * marks:g}"
        except (TypeError, ValueError):
            return "0"

    def validate(self) -> str | None:
        if not self.type_dropdown.value:
            return "Select a question type for every row."
        try:
            count = int(self.count_field.value)
            if count <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return "Question count must be a positive whole number."
        try:
            marks = float(self.marks_field.value)
            if marks <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return "Marks per question must be a positive number."
        return None

    def to_dict(self) -> dict:
        count = int(self.count_field.value)
        marks = float(self.marks_field.value)
        return {
            "questionType": self.type_dropdown.value,
            "questionCount": count,
            "marksPerQuestion": marks,
            "rowTotalMarks": count * marks,
        }


def generate_questions_view(page: ft.Page):
    """Return the Generate Questions screen matching the Scan E-Books layout/style."""

    def go_back(e):
        page.appbar = None
        page.navigate("/home")

    def show_snack(msg: str, color=ft.Colors.RED_600):
        page.show_dialog(ft.SnackBar(content=ft.Text(msg), bgcolor=color))

    # ── Cascading selectors (Class / Subject / Chapter) ─────────────────
    class SelectorState:
        def __init__(self, label, on_change=None):
            self.label = label
            self.options: list[str] = []
            self.value = None
            self._on_change = on_change
            self.chips = ft.Row(spacing=6, wrap=True, scroll=ft.ScrollMode.HIDDEN, expand=True)
            self.empty_message = ft.Text("", size=12, color=ft.Colors.GREY_500, italic=True, visible=False)
            self.field = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[ft.Text(label, size=12, weight=ft.FontWeight.BOLD)], height=18),
                        self.chips,
                        self.empty_message,
                    ],
                    spacing=4,
                ),
                border=ft.Border.all(1, ft.Colors.GREY_700),
                border_radius=6,
                padding=ft.Padding(left=8, top=5, right=8, bottom=6),
            )

        def set_options(self, options: list[str], empty_text: str = ""):
            self.options = options
            self.value = None
            self.empty_message.value = empty_text
            self.empty_message.visible = not options and bool(empty_text)
            self.refresh()

        def select(self, option):
            self.value = option
            self.refresh()
            if self._on_change:
                page.run_task(self._on_change)

        def refresh(self):
            self.chips.controls = [
                ft.Container(
                    content=ft.Text(
                        option,
                        size=12,
                        color=ft.Colors.WHITE if option == self.value else ft.Colors.GREY_900,
                    ),
                    bgcolor="#3949AB" if option == self.value else ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.GREY_500),
                    border_radius=14,
                    padding=ft.Padding(left=10, top=4, right=10, bottom=4),
                    on_click=lambda e, selected=option: self.select(selected),
                )
                for option in self.options
            ]

    async def on_class_selected():
        subject_selector.set_options([])
        chapter_selector.set_options([])
        update_rows_visibility()
        if class_selector.value:
            subjects = await asyncio.to_thread(get_subjects, class_selector.value)
            subject_selector.set_options(
                subjects, empty_text="No subjects found for this class. Scan e-books first."
            )
        page.update()

    async def on_subject_selected():
        chapter_selector.set_options([])
        update_rows_visibility()
        if class_selector.value and subject_selector.value:
            chapters = await asyncio.to_thread(get_chapters, class_selector.value, subject_selector.value)
            chapter_selector.set_options(
                chapters, empty_text="No chapters found for this subject. Scan e-books first."
            )
        page.update()

    async def on_chapter_selected():
        update_rows_visibility()
        page.update()

    class_selector = SelectorState("Class", on_change=on_class_selected)
    subject_selector = SelectorState("Subject", on_change=on_subject_selected)
    chapter_selector = SelectorState("Chapter", on_change=on_chapter_selected)

    # ── Dynamic question rows ────────────────────────────────────────────
    rows: list[QuestionRow] = []
    rows_column = ft.Column(spacing=10)
    ready_message = ft.Text(
        "Select class, subject, and chapter to configure questions.",
        color=ft.Colors.GREY_600,
        size=13,
    )
    add_row_button = ft.OutlinedButton(
        content=ft.Row(
            controls=[ft.Icon(ft.Icons.ADD, size=16), ft.Text("Add Row", size=13)],
            tight=True,
            spacing=6,
        ),
        on_click=lambda e: add_row(),
    )
    rows_section = ft.Column(
        controls=[
            ft.Text("Question Configuration", size=16, weight=ft.FontWeight.BOLD, color="#1a237e"),
            rows_column,
            add_row_button,
        ],
        spacing=12,
        visible=False,
    )

    def update_rows_visibility():
        ready = bool(class_selector.value and subject_selector.value and chapter_selector.value)
        rows_section.visible = ready
        ready_message.visible = not ready

    def used_types(exclude_row: QuestionRow | None = None) -> set:
        return {row.type_dropdown.value for row in rows if row is not exclude_row and row.type_dropdown.value}

    def refresh_dropdown_options():
        for row in rows:
            taken = used_types(exclude_row=row)
            row.type_dropdown.options = [
                ft.DropdownOption(key=key, text=text, disabled=key in taken) for key, text in QUESTION_TYPES
            ]

    def render_rows(update_page: bool = True):
        rows_column.controls = [row.row_control for row in rows]
        refresh_dropdown_options()
        add_row_button.disabled = len(rows) >= len(QUESTION_TYPES)
        for row in rows:
            row.delete_button.visible = len(rows) > 1
        if update_page:
            page.update()

    def recalc_row(row: QuestionRow):
        row.refresh_total()
        page.update()

    def add_row():
        if len(rows) >= len(QUESTION_TYPES):
            return
        row = QuestionRow(
            on_type_change=lambda: (refresh_dropdown_options(), page.update()),
            on_remove=remove_row,
            on_recalc=lambda: None,
        )
        row._on_recalc = lambda r=row: recalc_row(r)
        rows.append(row)
        render_rows()

    def remove_row(row: QuestionRow):
        if len(rows) <= 1:
            return
        rows.remove(row)
        render_rows()

    def generate_questions(e):
        if not (class_selector.value and subject_selector.value and chapter_selector.value):
            show_snack("Select class, subject, and chapter.")
            return
        if not rows:
            show_snack("Add at least one question row.")
            return
        for row in rows:
            error = row.validate()
            if error:
                show_snack(error)
                return

        payload = {
            "className": class_selector.value,
            "subject": subject_selector.value,
            "chapter": chapter_selector.value,
            "questionRows": [row.to_dict() for row in rows],
        }
        print(f"Generate Questions submitted: {payload}")
        show_snack("Question configuration submitted successfully.", color=ft.Colors.GREEN_700)

    add_row()

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=go_back,
        ),
        title=ft.Text("Generate Questions", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor="#3949AB",
    )
    page.drawer = None

    form_layout = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=16,
        controls=[
            ft.Text("Generate Questions", size=24, weight=ft.FontWeight.BOLD, color="#1a237e"),
            ft.Text(
                "Choose the class, subject, and chapter to configure the question paper.",
                color=ft.Colors.GREY_600,
                size=14,
            ),
            class_selector.field,
            subject_selector.field,
            chapter_selector.field,
            ready_message,
            rows_section,
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text("GENERATE QUESTIONS", weight=ft.FontWeight.BOLD),
                    color=ft.Colors.WHITE,
                    bgcolor="#3949AB",
                    height=46,
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=23)),
                    on_click=generate_questions,
                ),
                width=page.width - 40,
                padding=ft.Padding(left=0, top=10, right=0, bottom=20),
            ),
        ],
    )

    async def load_classes():
        classes = await asyncio.to_thread(get_classes)
        class_selector.set_options(
            classes, empty_text="No class data found. Scan e-books first to add data."
        )
        page.update()

    page.run_task(load_classes)

    return ft.Container(
        content=form_layout,
        padding=ft.Padding(left=20, top=20, right=20, bottom=20),
        expand=True,
    )
