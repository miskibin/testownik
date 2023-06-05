import flet as ft
from model import Model, TestCase

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650

ITERATION = 0


class App(ft.UserControl):
    def __init__(self, model: Model = Model(), question: TestCase = None):
        super().__init__()
        self.model = model
        self.question = question
        if question is None:
            self.question: TestCase = next(self.model.question_generator)

    @property
    def main_container(self):
        self.checkboxes = [
            ft.Checkbox(fill_color="blue600") for answer in self.question.answers
        ]
        self.question_text = ft.Text(self.question.question, size=25)
        return ft.Container(
            ft.Column(
                [
                    self.question_text,
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    *[
                                        ft.Row(
                                            [
                                                checkbox,
                                                ft.Text(
                                                    answer,
                                                    size=20,
                                                    width=WINDOW_WIDTH // 1.4,
                                                ),
                                            ],
                                            alignment="start",
                                        )
                                        for checkbox, answer in zip(
                                            self.checkboxes, self.question.answers
                                        )
                                    ],
                                ],
                                # height=WINDOW_HEIGHT // 1.6,
                                alignment="start",
                            ),
                            ft.Container(
                                # bgcolor="blue",
                                content=ft.IconButton(
                                    icon=ft.icons.CHECK_ROUNDED,
                                    icon_color="blue600",
                                    icon_size=100,
                                    on_click=self.submit,
                                ),
                                # alignment=ft.alignment.bottom_right,
                                expand=True,
                                height=WINDOW_HEIGHT // 1.9,
                                width=WINDOW_WIDTH // 4,
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                alignment="center",
            ),
            height=WINDOW_HEIGHT // 1.4,
            border_radius=20,
            # bgcolor="green",
            padding=20,
            margin=5,
        )

    @property
    def footer(self):
        return ft.Container(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Current question", size=20),
                            ft.Text(
                                f"{self.question._tried} / {self.question._correct_anwsered}",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                            ),
                        ],
                        horizontal_alignment="center",
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"Questions in quiz",
                                size=20,
                            ),
                            ft.Text(
                                f"{len(self.model.questions)}",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                            ),
                        ],
                        horizontal_alignment="center",
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"Total attempts",
                                size=20,
                            ),
                            ft.Text(
                                f"{ITERATION}",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                            ),
                        ],
                        horizontal_alignment="center",
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"mastered ({self.model.mastered_questions}/{len(self.model.questions)})",
                                size=20,
                            ),
                            ft.ProgressBar(
                                value=self.model.mastered_questions
                                / len(self.model.questions),
                                bgcolor="red600",
                                color="green",
                                width=WINDOW_WIDTH // 7,
                            ),
                        ],
                        horizontal_alignment="center",
                    ),
                ],
                alignment="spaceAround",
                vertical_alignment="start",
            ),
            margin=5,
            padding=20,
            bgcolor="blue600",
            border_radius=25,
        )

    def submit(self, e):
        global ITERATION
        ITERATION += 1
        aws = [int(b.value) for b in self.checkboxes]
        if sum(aws) == 1:
            idx = aws.index(1)
            self.question._tried += 1
        else:
            print("Please select only one answer")
            return
        print(f"Correct answer: {self.question.correct_answer}, your answer: {idx}")
        if idx == self.question.correct_answer:
            e.page.dialog = self.correct_dialog
            self.question._correct_anwsered += 1

        else:
            e.page.dialog = self.wrong_dialog

        self.page.dialog.open = True
        e.page.update()

    def go_forward(self, e):
        self.page.dialog.open = False
        e.page.update()
        self.update_all(e)

    def close_dialog(self, e):
        self.page.dialog.open = False
        e.page.update()

    @property
    def correct_dialog(self):
        col = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.CHECK,
                    icon_size=60,
                    disabled=True,
                    icon_color="green",
                ),
                ft.Text("Correct!", size=40),
                ft.IconButton(
                    icon=ft.icons.ARROW_RIGHT_ALT,
                    icon_size=90,
                    on_click=self.go_forward,
                    icon_color="blue600",
                ),
            ],
            alignment="center",
            vertical_alignment="center",
        )
        return ft.AlertDialog(
            # title=ft.Text("Please confirm"),
            title=col,
        )

    def choose_number_of_questions(self, e):
        self.model = Model(int(self.number_of_questions_field.value))
        self.page.dialog.open = False

        e.page.update()
        self.update_all(e)

    @property
    def number_of_questions_dialog(self):
        self.number_of_questions_field = ft.TextField(
            value=len(self.model.questions),
            helper_text="number of questions",
            # on_click=self.choose_number_of_questions,
        )
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("How many questions do you want to have?"),
            actions=[
                self.number_of_questions_field,
                ft.OutlinedButton("OK", on_click=self.choose_number_of_questions),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    @property
    def wrong_dialog(self):
        col = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_size=60,
                    disabled=True,
                    icon_color="red",
                ),
                ft.Column(
                    [
                        ft.Text("WRONG!", size=40),
                        ft.Text(
                            f"correct: {self.question.answers[self.question.correct_answer]}",
                            size=15,
                        ),
                    ]
                ),
                ft.IconButton(
                    icon=ft.icons.LOOP,
                    on_click=self.close_dialog,
                    icon_size=80,
                    icon_color="blue600",
                ),
            ],
            alignment="center",
        )
        return ft.AlertDialog(
            # title=ft.Text("Please confirm"),
            title=col,
        )

    @property
    def end_dialog(self):
        col = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.PIN_END,
                    icon_size=60,
                    disabled=True,
                    icon_color="blue600",
                ),
                ft.Text("You have finished quiz! ", size=40),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_size=60,
                    icon_color="red",
                ),
            ],
            alignment="center",
        )
        return ft.AlertDialog(
            # title=ft.Text("Please confirm"),
            title=col,
        )

    def on_keyboard_event(self, event: ft.KeyboardEvent):
        if event.key == "Enter" and (
            not event.page.dialog or event.page.dialog.open is False
        ):
            self.submit(event)
        elif event.key == "Enter":
            self.go_forward(event)
        elif str(event.key).isdigit() and int(event.key) <= len(self.question.answers):
            self.checkboxes[int(event.key) - 1].value = not self.checkboxes[
                int(event.key) - 1
            ].value
            self.checkboxes[int(event.key) - 1].update()
        event.page.update()

    def update_all(self, event):
        page = event.page
        # check if there is next question
        try:
            self.question = next(self.model.question_generator)
        except StopIteration:
            page.dialog = self.end_dialog
            page.dialog.open = True
            page.update()
            return
        page.controls.pop()
        page.controls.append(App(self.model, self.question))
        page.update()

    def build(self):
        view = ft.Column(
            [
                self.main_container,
                self.footer,
            ],
            alignment="spaceBetween",
            horizontal_alignment="center",
        )
        return view


def main(page: ft.Page):
    global NUMBER_OF_QUESTIONS
    page.padding = 10
    # page.scroll = "auto"
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT
    page.window_min_height = WINDOW_HEIGHT
    page.window_min_width = WINDOW_WIDTH
    page.title = "testownik"
    model = Model()
    app = App(model)
    page.add(app)
    page.dialog = app.number_of_questions_dialog
    page.dialog.open = True
    page.update()


if __name__ == "__main__":
    # number_of_questions  ile pytan ma byc w sumie w quizie
    # pytania sie usuwaja w miare jak ich sie nauczy
    ft.app(
        target=main,
    )
