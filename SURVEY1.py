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
    page.theme_mode = ft.ThemeMode.DARK

    filename = open("questions").read().splitlines()[-1]
    Rewards = ["Pen", "KitKat", "Pencil", "Munch"]

    colors = [ft.colors.RED, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.GREEN]

    #PageAlignment
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    normal_border = ft.BorderSide(0, ft.colors.with_opacity(0, ft.colors.BLACK))
    hovered_border = ft.BorderSide(4, ft.colors.WHITE)

    normal_title_style = ft.TextStyle(size=15, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            section.border_style = (
                hovered_border if idx == e.section_index else normal_border
            )
        chart.update()

    #Design for Icons on the Chart
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

    n = len(data["choices"])

    img = ft.Image(src="Logo/Logo.png")

    Upperbar = ft.AppBar(
        leading=img,
        leading_width=320,
        title=ft.Text("Little Star Hr. Sec. School\n\t\t\t           Survey", size=40, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.colors.GREY_600,
        toolbar_opacity=1,
        toolbar_height=110,
        elevation=7,
        shadow_color=ft.colors.WHITE,
        actions=[ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Tekamoli")
            ]
        )]
    )
    Bottombar= ft.BottomAppBar(
        elevation=10,
        shadow_color=ft.colors.WHITE,
        height=60
    )
    # Users_Choices

    radio_controls = []

    for i in range(n):
        radio_controls.append(ft.Radio(value=str(i + 1), label=data["choices"][i][0]))

    radios = ft.Column(controls=radio_controls, alignment=ft.alignment.top_left)

    radio_group = ft.RadioGroup(content=radios)

    reward_text = ft.Text("",size=20)  # Reward

    # fn for what the submit button will do
    def submit(e):
        # Update user_choice data
        selected_choice = int(radio_group.value) - 1
        data["choices"][selected_choice][1] += 1
        SaveToFile(filename, data)

        # Reward
        user_reward = random.choice(Rewards)
        reward_text.value = f"Your reward: {user_reward}"

        chart.sections = []
        for i in range(n):
            chart.sections.append(
                ft.PieChartSection(
                    value=data["choices"][i][1],
                    color=colors[i],
                    radius=150,
                    border_side=normal_border,
                    title=data["choices"][i][1],
                    title_style=normal_title_style
                )
            )

        # Live Updates the rewards and pie chart data whenever submit is clicked
        page.update()

    submit_btn = ft.ElevatedButton(text="Submit", on_click=submit)
    # Representing Data in the form of pie chart
    chart_sections = []

    for i in range(n):
        chart_sections.append(
            ft.PieChartSection(
                value=data["choices"][i][1],
                color=colors[i],
                radius=120,
                border_side=normal_border,
                title=data["choices"][i][1],
                title_style=normal_title_style
            )
        )

    chart = ft.PieChart(
        sections=chart_sections,
        sections_space=0,
        center_space_radius=0,
        on_chart_event=on_chart_event,
        expand=True
    )
    chart_container = ft.Container(
        content=chart,
        alignment=ft.alignment.top_right,
        height=200,
        width=1000)
    parent= ft.Container(
        content=chart_container,
        alignment=ft.alignment.top_right
    )
    row_all=ft.Row(controls=[radio_group,parent],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    page.add(Upperbar)
    page.add(ft.Text("\n"))
    page.add((ft.Text(data["question"], size=38)))
    #page.add(radio_group)
    page.add(row_all)

    page.add(submit_btn)
    page.add(reward_text,)
    #page.add(parent)

    page.add(Bottombar)
ft.app(target=main)