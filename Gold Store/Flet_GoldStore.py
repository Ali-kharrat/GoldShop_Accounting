from database import add_clinet, show, add_products, create_database, create_image
import flet as ft
import requests
import re
from bs4 import BeautifulSoup

create_database()


def getvalue():
    try:
        req = requests.request(url="https://www.tala.ir/webservice/price_live.php?new=1", method="GET")
        soup = BeautifulSoup(req.content, 'html.parser')
        a = soup.find("a", id="gold_18k")
        for i in re.findall('<a href="http://www.tala.ir" id="gold_18k" style="color:#.*" target="_blank">(.*?)</a>',
                            str(a)):
            val = i.replace(',', '')
    except:
        val = ''

    return val


global_data = {
    "weights": "",
    "nowprice": "",
    "right": "",
    "taxs": "",
}


class Task(ft.Column):
    def __init__(self, name, phone_number, serial_number, task_delete):
        super().__init__()
        self.completed = False
        self.name = name
        self.phone_number = phone_number
        self.serial_number = serial_number
        self.task_delete = task_delete
        get_value = getvalue()
        vazn = show(serial_number)
        try:
            a = int(vazn) * int(get_value) * 0.09
        except:
            a = ''

        self.weight_field = ft.TextField(
            label="وزن", rtl=True, width=135, value=vazn, on_change=self.onchange
        )
        self.now_price = ft.TextField(
            label=" قیمت لحظه‌ای", rtl=True, width=135, value=get_value, on_change=self.onchange
        )
        self.rights = ft.TextField(
            label="اجرت", rtl=True, width=135, on_change=self.onchange
        )
        self.tax = ft.TextField(
            label="مالیات", rtl=True, width=135, value=a, on_change=self.onchange
        )

        self.display_view = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(rtl=True,
                       controls=[
                           ft.Text(f"{name}", rtl=True), ft.Text(f"0{phone_number}")
                       ]
                       ),

                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER,
                       controls=[
                           ft.IconButton(
                               ft.icons.DELETE_OUTLINE,
                               tooltip="Delete",
                               on_click=self.delete_clicked,
                           ),
                           self.tax,
                           self.rights,
                           self.now_price,
                           self.weight_field,
                       ],
                       ),
            ],
        )

        self.controls = [self.display_view]

    def delete_clicked(self, e):
        self.task_delete(self)

    def onchange(self, e):
        global global_data
        global_data["weights"] = self.weight_field.value
        global_data["nowprice"] = self.now_price.value
        global_data["right"] = self.rights.value
        global_data["taxs"] = self.tax.value


class TodoApp(ft.Column):

    def __init__(self):
        super().__init__()
        self.Name = ft.TextField(
            label="نام", on_submit=self.add_clicked, expand=True, rtl=True, prefix_icon=ft.icons.PERSON
        )

        self.Phone_number = ft.TextField(
            label="شماره همراه", on_submit=self.add_clicked, expand=True, prefix_text="+98 ",
        )

        self.Serial_Number = ft.TextField(
            label="شماره سریال", on_submit=self.add_clicked, expand=True, prefix_icon=ft.icons.NUMBERS_SHARP
        )

        self.Serial_Number_ADD = ft.TextField(
            label="شماره سریال", on_submit=self.add_clicked, expand=False, prefix_icon=ft.icons.NUMBERS_SHARP
        )
        self.Weight_ADD = ft.TextField(
            label="وزن", on_submit=self.add_clicked, expand=False, prefix_icon=ft.icons.NUMBERS_SHARP
        )
        self.Buy_Price = ft.TextField(
            label="قیمت خرید", on_submit=self.add_clicked, expand=False, prefix_icon=ft.icons.NUMBERS_SHARP
        )

        self.tasks = ft.Column()

        self.add_con = ft.Container(
            width=120,
            content=ft.ResponsiveRow(
                expand=True,
                controls=[
                    self.Serial_Number_ADD, self.Weight_ADD, self.Buy_Price
                ]
            )
        )

        self.dlg_modal = ft.AlertDialog(
            modal=False,
            title=ft.Text("Please confirm"),
            content=self.add_con,
            actions=[
                ft.TextButton("save", on_click=self.save),
                ft.TextButton("No", on_click=lambda e: self.page.close(self.dlg_modal))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="ثبت خرید"),
                  #   ft.Tab(text="خرید های اخیر"),
                  ],
        )

        self.items_left = ft.Text("هیچ محصولی خریداری نشده")

        self.width = 600
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(value="Gold Store", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                ],
            ),
            ft.Row(
                controls=[
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        on_click=self.add_clicked,
                        height=50,
                        width=50,
                        bgcolor="lime"
                    ),
                    self.Serial_Number,
                    self.Phone_number,
                    self.Name,
                ]
            ),

            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.Row(
                                controls=[

                                    ft.OutlinedButton(
                                        text="ثبت خرید", on_click=self.Submit_click,
                                    ),
                                    ft.ElevatedButton(color='black',
                                                      animate_opacity=10,
                                                      bgcolor='lime',
                                                      text="اضافه کردن محصول",
                                                      width=180,
                                                      height=33,
                                                      icon=ft.icons.ADD,
                                                      on_click=lambda e: self.page.open(self.dlg_modal)
                                                      )
                                ]
                            )
                        ],
                    ),
                ],
            ),
        ]

    def save(self, e):
        serial_number = self.Serial_Number_ADD.value
        weight = int(self.Weight_ADD.value)
        buy_price = int(self.Buy_Price.value)
        try:
            add_products(serial_number, weight, buy_price)
        except:
            pass
        print(show(serial_number))
        try:
            self.page.close(self.dlg_modal)
        except:
            pass

    def add_clicked(self, e):
        name = self.Name.value
        number = self.Phone_number.value
        serial = self.Serial_Number.value
        task = Task(self.Name.value, self.Phone_number.value, self.Serial_Number.value, self.task_delete)
        self.tasks.controls.append(task)
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def Submit_click(self, e):

        for task in self.tasks.controls:
            name = self.Name.value
            phone = self.Phone_number.value
            serial = self.Serial_Number.value
            global global_data
            data = global_data
            final = int(data["nowprice"]) * int(data["weights"]) * 0.09 + int(data["right"])
            task.completed = True
            create_image(name, phone, serial, int(data["weights"]), final)
            add_clinet(name, phone, serial, int(data["nowprice"]), int(data["weights"]), final)

        self.update()

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                    (status == "ثبت خرید" and task.completed == False) or (status == "خرید های اخیر" and task.completed)
            )
            print(task.visible, status)
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} محصولات خریداری شده"


def main(page: ft.Page):
    page.title = "Gold Store"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(TodoApp())


ft.app(main)
