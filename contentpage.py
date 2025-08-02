import flet as ft
import os

cntr = ft.MainAxisAlignment.CENTER

class ContentPage(ft.View):
    def __init__(self, master):

        self.master = master
        self.colon = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        # colon width
        self.cw = 200
        self.bw = 25 

        self.initialize_content()
        self.container = ft.Container(content=self.colon, expand=True, margin=ft.margin.symmetric(horizontal=40))
        super().__init__(controls=[self.container], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)

    def initialize_content(self):
        self.colon.controls = []

        cols = [
                ft.DataColumn(ft.Text("Note", expand=True)),
                ft.DataColumn(ft.Text("Key", expand=True)),
                ft.DataColumn(ft.Text("Value", expand=True)),
                ft.DataColumn(ft.Text("Show", expand=True)),
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
                         ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=1: self.edit_callback(g,n)),
                         ])
                         ),
                     ft.DataCell(
                         ft.Row([
                         ft.TextField(value="Vaal {i}", disabled=True, password=True, expand=True),
                         ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=2: self.edit_callback(g,n)),
                         ])
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.PREVIEW, on_click=lambda _, g=i: self.show_callback(g), expand=True)
                         )]
            dtrow = ft.DataRow(cells=cells)
            setattr(self, f'row_group{i}', dtrow)


            rows.append(dtrow)
            setattr(self, f'cell_{i}0_editing', False)
            setattr(self, f'cell_{i}1_editing', False)
            setattr(self, f'cell_{i}2_editing', False)

        self.dt = ft.Row([ft.DataTable(columns=cols, rows=rows, expand=True)], alignment=ft.MainAxisAlignment.CENTER)
        self.colon.controls.append(self.dt)
        self.master.update()

    def show_callback(self, g:int):
        i = g
        row_group = getattr(self, f'row_group{i}')

        key_control = row_group.cells[1].content.controls[0]
        key_control.password = not key_control.password

        value_control = row_group.cells[2].content.controls[0]
        value_control.password = not value_control.password

        self.master.update()

    def edit_callback(self, g:int, n:int):
        i = g
        row_group = getattr(self, f'row_group{i}')
        row_cells = row_group.cells
        is_editing = getattr(self, f'cell_{i}{n}_editing')

        new_row_control = row_cells[n].content.controls[0]
        if is_editing:
            new_row_control.disabled = True
            row_cells[n].content.controls[0] = new_row_control

            row_edit_control = row_cells[n].content.controls[1]
            row_edit_control.icon = ft.Icons.EDIT
            row_cells[n].content.controls[1] = row_edit_control
        else:
            new_row_control.disabled = False
            row_cells[n].content.controls[0] = new_row_control

            row_edit_control = row_cells[n].content.controls[1] 
            row_edit_control.icon = ft.Icons.CLOSE
            row_cells[n].content.controls[1] = row_edit_control

        row_group.cells = row_cells
        setattr(self, f'cell_{i}{n}_editing', not is_editing)
        setattr(self, f'row_group{i}', row_group)
        self.master.update()


class MainWindow:
    def __init__(self,page):
        self.page = page
        self.page.title = "Content Page"
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change

        dlg = ft.AlertDialog(modal=True,title=ft.Text("Info"), content=ft.Text("To encrypt data in the app, you need to register before you can start storing it.\n This app does not communicate with the internet, everything is stored locally. Content is encrypted and decrypted using your master password, master password is not stored as plain text.\n\nData is stored\n\nOn Linux:\n'~/.config/password_wallet'\n\nOn macOS:\n'/Users/<username>/Library/Application Support/password_wallet'\n\nOn Windows:\n'C:\\Users\\<username>\\AppData\\Local\\duzdunya\\password_wallet'\n\nAuthor: Ali Çine"), actions=[ft.TextButton("Ok",on_click=lambda _: self.master.close(dlg))])
        self.apb= ft.AppBar(
                title=ft.Text("Password Wallet"),
                center_title=False,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                        ft.PopupMenuItem(text="Info", icon=ft.Icons.INFO, on_click=lambda _: self.page.open(dlg)),
                            ft.PopupMenuItem(text="Quit", icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click=lambda _: self.page.window.destroy()),
                            ]
                        ),
                    ],
                )

        self.page.update()
        self.page.go("/")

        
    def route_change(self, route):
        self.page.views.clear()

        if self.page.route == '/':
            contentpage = ContentPage(self.page)
            self.page.views.append(contentpage)

        self.page.update()



ft.app(MainWindow)
