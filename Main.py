import flet as ft
import json
import random
import time


def SaveToFile(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def LoadFromFile(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.theme=ft.Theme(color_scheme_seed=ft.colors.GREY_800)

    filename = open("questions").read().splitlines()[1]

    Rewards = ["Pen", "KitKat", "Mechanical Pencil", "Munch"]

    colors = [ft.colors.RED, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.GREEN, ft.colors.DEEP_ORANGE,
              ft.colors.DEEP_PURPLE]

    #PageAlignment
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    normal_border = ft.BorderSide(0, ft.colors.with_opacity(1, ft.colors.WHITE))
    hovered_border = ft.BorderSide(4, ft.colors.WHITE)

    normal_title_style = ft.TextStyle(size=15, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            section.border_style = (
                hovered_border if idx == e.section_index else normal_border
            )
        chart.update()

    #Design for Icons on the Chart
    def create_badges(images, size):
        badges = []
        for img_url in images:
            badge = ft.Container(
                ft.Image(src=img_url),
                width=size,
                height=size,
                border=ft.border.all(2, ft.colors.BLACK),
                border_radius=size / 2,
                bgcolor=ft.colors.WHITE,
            )
            badges.append(badge)
        return badges

    data = LoadFromFile(filename)

    n = len(data["choices"])

    img = ft.Image(src="Logo/Logo.png")

    Upperbar = ft.AppBar(
        leading=img,
        leading_width=320,
        title=ft.Text("Little Star Hr. Sec. School\n\t\t\t           Survey", size=40,
                      weight=ft.FontWeight.BOLD,color=ft.colors.BLACK),
        center_title=True,
        bgcolor=ft.colors.GREY_400,
        toolbar_opacity=1,
        toolbar_height=130,
        elevation=9,
        shadow_color=ft.colors.WHITE,
        actions=[ft.PopupMenuButton(icon_color=ft.colors.BLACK,
            items=[
                ft.PopupMenuItem(text="Teacher Incharge:"),
                ft.PopupMenuItem(text="\t  Sir Vihutuo"),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Students:"),
                ft.PopupMenuItem(text="\t  Abhishek"),
                ft.PopupMenuItem(text="\t  AkumLong"),
                ft.PopupMenuItem(text="\t  Tekamoli"),
                ft.PopupMenuItem(text="\t  Imdan"),
                ft.PopupMenuItem(text="\t  KumKum"),
                ft.PopupMenuItem(text="\t  RishiLong")
            ]
        )]
    )
    Bottombar = ft.BottomAppBar(
        elevation=10,
        bgcolor=ft.colors.GREY_600,
        height=50
    )
    # Users_Choices

    radio_controls = []

    for i in range(n):
        radio_controls.append(ft.Radio(value=str(i + 1), label=data["choices"][i][0]))

    radios = ft.Column(controls=radio_controls, alignment=ft.MainAxisAlignment.CENTER, height=None)
    radio_group = ft.RadioGroup(content=radios)

    reward_text = ft.Text("", size=25)  # Reward

    # fn for what the submit button will do
    def submit(e):
        # Update user_choice data
        selected_choice = int(radio_group.value) - 1
        data["choices"][selected_choice][1] += 1
        SaveToFile(filename, data)

        # Reward
        user_reward = random.choice(Rewards)
        reward_text.value = "Your Reward :\t  "
        time.sleep(0.1)
        reward_text.value += str(user_reward)

        chart.sections = []

        chart.sections = []

        for i in range(n):
            badge = create_badges([data["choices"][i][2]], 50)  # Using the icon specific to the section
            chart.sections.append(
                ft.PieChartSection(
                    value=data["choices"][i][1],
                    color=colors[i],
                    radius=180,
                    border_side=normal_border,
                    title=data["choices"][i][1],
                    title_style=normal_title_style,
                    badge=badge[0] if badge else None,
                    badge_position=0.98
                )
            )

        # Live Updates the rewards and pie chart data whenever submit is clicked
        page.update()

    submit_btn = ft.ElevatedButton(text="Submit", on_click=submit)
    # Representing Data in the form of pie chart

    chart_sections = []

    for i in range(n):
        badge = create_badges([data["choices"][i][2]], 50)  # Using the icon specific to the section
        chart_sections.append(
            ft.PieChartSection(
                value=data["choices"][i][1],
                color=colors[i],
                radius=180,
                border_side=normal_border,
                badge=badge[0] if badge else None,
                badge_position=0.98,
                title=data["choices"][i][1],
                title_style=normal_title_style,
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
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT
    )

    column_chart = ft.Column(controls=[chart_container], alignment=ft.MainAxisAlignment.END, )  #height=500)
    parent = ft.Container(
        content=column_chart,
        height=75,
        width=1750,
        alignment=ft.alignment.center
    )

    row_all = ft.Row(controls=[radio_group, parent], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(Upperbar)
    page.add(ft.Text(data["question"], size=38))
    page.add(row_all)
    page.add(ft.Text("\n"))
    page.add(submit_btn)
    page.add(ft.Text("\n\n\n"))
    page.add(reward_text, )
    #page.add(parent)

    page.add(Bottombar)


ft.app(target=main)
