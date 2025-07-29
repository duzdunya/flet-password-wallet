import flet as ft
import os

cntr = ft.MainAxisAlignment.CENTER

class ValueInput(ft.Container):
    def __init__(self, master):
        pass

class ContentPage(ft.View):
    def __init__(self, master):

        self.master = master
        self.colon = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        # colon width
        self.cw = 200
        self.bw = 25 

        self.initialize_content()
        self.container = ft.Container(content=self.colon)
        appbar = ft.AppBar(
                title=ft.Text("Password Wallet"),
                center_title=False,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Quit", icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click=lambda _: self.page.window.destroy()),
                            ]
                        ),
                    ],
                )
        super().__init__(controls=[self.container], horizontal_alignment=ft.alignment.center, vertical_alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS, appbar=appbar)

    def initialize_content(self):
        self.colon.controls = []

        cols = [
                ft.DataColumn(ft.Text("Note", expand=True)),
                ft.DataColumn(ft.Text("Key", expand=True)),
                ft.DataColumn(ft.Text("Value", expand=True)),
                ft.DataColumn(ft.Text("Show")),
                ]
        rows = []
        for i in range(0,100):
            cells = [ 
                     ft.DataCell(
                         ft.Row([
                         ft.TextField(value=f"My note {i}",  disabled=True, expand=True),
                         ft.IconButton(icon=ft.Icons.EDIT,on_click=lambda _, g=i, n=0: self.edit_callback(g,n)),
                         ])
                         ),
                     ft.DataCell(
                         ft.Row([
                         ft.TextField(value=f'Keey {i}j', disabled=True, password=True, expand=True),
                         ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=2: self.edit_callback(g,n)),
                         ])
                         ),
                     ft.DataCell(
                         ft.Row([
                         ft.TextField(value="Vaal {i}", disabled=True, password=True, expand=True),
                         ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=4: self.edit_callback(g,n)),
                         ])
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.PREVIEW, on_click=lambda _, g=i: self.show_callback(g), expand=True)
                         )]
            dtrow = ft.DataRow(cells=cells)

            rows.append(dtrow)

            setattr(self, f'row_group{i}_0_editing', False)
            setattr(self, f'row_group{i}_2_editing', False)
            setattr(self, f'row_group{i}_4_editing', False)

        self.dt = ft.DataTable(columns=cols, rows=rows, expand=True)
        self.colon.controls.append(self.dt)
        self.master.update()

    def show_callback(self, g:int):
        i = g
        row_group = getattr(self, f'row_group{i}')

        key_control = row_group.controls[2]
        key_control.password = not key_control.password

        value_control = row_group.controls[4]
        value_control.password = not value_control.password

        self.master.update()

    def edit_callback(self, g:int, n:int):
        i = g
        row_group = getattr(self, f'row_group{i}')
        row_controls = row_group.controls
        is_editing = getattr(self, f'row_group{i}_{n}_editing')

        if is_editing:
            new_row_control = row_controls[n]
            new_row_control.disabled = True
            row_controls[n] = new_row_control

            row_edit_control = row_controls[n+1]
            row_edit_control.icon = ft.Icons.EDIT
            row_controls[n+1] = row_edit_control
        else:

            new_row_control = row_controls[n]
            new_row_control.disabled = False
            row_controls[n] = new_row_control

            row_edit_control = row_controls[n+1]
            row_edit_control.icon = ft.Icons.CLOSE
            row_controls[n+1] = row_edit_control

        row_group.controls = row_controls
        setattr(self, f'row_group{i}_{n}_editing', not is_editing)
        setattr(self, f'row_group{i}', row_group)
        self.master.update()


class MainWindow:
    def __init__(self,page):
        self.page = page
        self.page.title = "Content Page"
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change
        self.page.go("/")

    def route_change(self, route):
        self.page.views.clear()

        if self.page.route == '/':
            contentpage = ContentPage(self.page)
            self.page.views.append(contentpage)

        self.page.update()



ft.app(MainWindow)
