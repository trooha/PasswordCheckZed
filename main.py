import flet as ft
import re

def main(page: ft.Page):
    page.title = "Password checking"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    page.window.width = 380
    page.window.height = 680
    page.window.resizable = False

    icon_header = ft.Icon(ft.Icons.LOCK_OUTLINED, size=80, color="blue")
    title_text = ft.Text("Check security", weight=ft.FontWeight.BOLD, size=16)

    password_input = ft.TextField(
        label="your password",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        width=300
    )

    progress_bar = ft.ProgressBar(value=0, width=300, color="green", bgcolor="surface")
    result_text = ft.Text("input password", weight=ft.FontWeight.BOLD, size=16)
    feedback_text = ft.Text("", size=14, color="onSurfaceVariant")

    def check_password(e):
        password = e.control.value

        if not password:
            progress_bar.value = 0
            result_text.value = "input password"
            result_text.color = "white"
            feedback_text.value = ""
            page.update()
            return

        score = 0
        feedback = []

        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("• Сделайте пароль длиннее (хотя бы 8 символов)")

        if re.search(r"[a-zа-я]", password):
            score += 1
        else:
            feedback.append("• Добавьте строчные буквы")

        if re.search(r"[A-ZА-Я]", password):
            score += 1
        else:
            feedback.append("• Добавьте заглавные буквы")

        if re.search(r"\d", password):
            score += 1
        else:
            feedback.append("• Добавьте цифры")

        if re.search(r"[_@$!%*?&#.,;:+\-]", password):
            score += 1
        else:
            feedback.append("• Добавьте спецсимволы (@, #, $, % и т.д.)")

        progress_bar.value = score / 6

        if score <= 2:
            result_text.value = "weak password"
            result_text.color = "red"
            progress_bar.color = "red"
        elif score <= 4:
            result_text.value = "normal password"
            result_text.color = "orange"
            progress_bar.color = "orange"
        else:
            result_text.value = "good password"
            result_text.color = "green"
            progress_bar.color = "green"

        feedback_text.value = "\n".join(feedback) if score < 6 else "Отличный пароль!"
        page.update()

    password_input.on_change = check_password

    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    icon_header,
                    title_text,
                    ft.Divider(height=20, color="transparent"),
                    password_input,
                    progress_bar,
                    result_text,
                    ft.Divider(height=10, color="transparent"),
                    feedback_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor="surfaceVariant",
        ),
        width=340,
        elevation=5
    )

    page.add(card)

ft.run(main)
