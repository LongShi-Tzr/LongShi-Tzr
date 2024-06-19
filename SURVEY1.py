import flet as ft
import json
import random

def SaveToFile(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def LoadFromFile(filename):
    with open(filename, "r") as f:
        return json.load(f)

def main(page: ft.Page):
    filename = "Transport_School.txt"
    Rewards = ["Pen", "Ruler", "Pencil"]

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    normal_border = ft.BorderSide(0, ft.colors.with_opacity(0, ft.colors.BLACK))
    hovered_border = ft.BorderSide(4, ft.colors.WHITE)

    normal_title_style = ft.TextStyle(
        size=16, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            section.border_side = (
                hovered_border if idx == e.section_index else normal_border
            )
        chart.update()

    def badge(icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.WHITE),
            border_radius=size / 2,
            bgcolor=ft.colors.BLACK,
        )

    data = LoadFromFile(filename)

    bar = ft.AppBar(title=ft.Text("SURVEY1", size=40, weight=ft.FontWeight.BOLD),
                    center_title=True,
                    bgcolor=ft.colors.BLUE_ACCENT,
                    toolbar_opacity=1,
                    )

    radios=ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=
    [
        ft.Column(alignment=ft.MainAxisAlignment.CENTER,
                  controls=[
                      ft.Radio(value="1", label=data["choices"][0][0]),
                      ft.Radio(value="2", label=data["choices"][1][0]),
                      ft.Radio(value="3", label=data["choices"][2][0]),
                      ft.Radio(value="4", label=data["choices"][3][0])
                  ]
                  )
    ]
                  )

    radio_group = ft.RadioGroup(content=radios)

    reward_text = ft.Text("")#RewardText

    def submit(e):
        # Update user_choice data
        selected_choice = int(radio_group.value) - 1
        data["choices"][selected_choice][1] += 1
        SaveToFile(filename, data)

        # Reward
        user_reward = random.choice(Rewards)
        reward_text.value = f"Your reward: {user_reward}"

        # Update chart sections
        chart.sections = [
            ft.PieChartSection(
                data["choices"][0][1],
                color=ft.colors.BLUE,
                radius=150,
                border_side=normal_border,
                title=data["choices"][0][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_BUS, 40),
                badge_position=0.98


            ),
            ft.PieChartSection(
                data["choices"][1][1],
                color=ft.colors.YELLOW,
                radius=150,
                border_side=normal_border,
                title=data["choices"][1][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.ELECTRIC_RICKSHAW, 40),
                badge_position=0.98

            ),
            ft.PieChartSection(
                data["choices"][2][1],
                color=ft.colors.RED,
                radius=150,
                border_side=normal_border,
                title=data["choices"][2][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_CAR, 40),
                badge_position=0.98
            ),
            ft.PieChartSection(
                data["choices"][3][1],
                color=ft.colors.GREEN,
                radius=150,
                border_side=normal_border,
                title=data["choices"][3][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_WALK, 40),
                badge_position=0.98
            )
        ]

        page.update()

    submit_btn = ft.ElevatedButton(text="Submit", on_click=submit)

    page.add(bar)
    page.add(ft.Text(data["question"], size=30),radio_group,submit_btn,reward_text)

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                data["choices"][0][1],
                color=ft.colors.BLUE,
                radius=150,
                border_side=normal_border,
                title=data["choices"][0][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_BUS, 40),
                badge_position=0.98
            ),
            ft.PieChartSection(
                data["choices"][1][1],
                color=ft.colors.YELLOW,
                radius=150,
                border_side=normal_border,
                title=data["choices"][1][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.ELECTRIC_RICKSHAW, 40),
                badge_position=0.98
            ),
            ft.PieChartSection(
                data["choices"][2][1],
                color=ft.colors.RED,
                radius=150,
                border_side=normal_border,
                title=data["choices"][2][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_CAR, 40),
                badge_position=0.98

            ),
            ft.PieChartSection(
                data["choices"][3][1],
                color=ft.colors.GREEN,
                radius=150,
                border_side=normal_border,
                title=data["choices"][3][1],
                title_style=normal_title_style,
                badge=badge(ft.icons.DIRECTIONS_WALK, 40),
                badge_position=0.98
            )
        ],
        sections_space=1,
        center_space_radius=0,
        on_chart_event=on_chart_event,
        expand=True
    )

    page.add(chart)

ft.app(target=main,view=ft.AppView.WEB_BROWSER)
