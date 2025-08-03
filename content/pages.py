from typing import NoReturn
from sec.auth import login_check, register_check
from sec.encryption import get_hashed_password, encrypt_the_content, decrypt_the_content, get_user_key
from user.data import add_new_user, save_content
from conf.settings import USER_DATA
from PIL import Image
import flet as ft

CNTR = ft.MainAxisAlignment.CENTER
CX_CENTER = ft.CrossAxisAlignment.CENTER
##############################
# Alert and AppBar
##############################

class WarningAlert(ft.AlertDialog):
    def __init__(self, master, text, title="Alert"):
        self.master = master
        
        super().__init__(modal=True, content=ft.Text(text, size=20), actions=[ft.TextButton("Ok", on_click= lambda _: self.master.page.close(self))])

class CustomAppBar(ft.AppBar):
    def __init__(self, title, master, *args, **kwargs):
        self.master = master

        dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Info"),
                content=ft.Text("To encrypt data in the app, you need to register before you can start storing it.\nThis app does not communicate with the internet, everything is stored locally. Content is encrypted and decrypted using your master password, master password is not stored as plain text.\n\nData located:\n\nOn Linux:\n'~/.config/password_wallet'\n\nOn macOS:\n'/Users/<username>/Library/Application Support/password_wallet'\n\nOn Windows:\n'C:\\Users\\<username>\\AppData\\Local\\duzdunya\\password_wallet'\n\nAuthor: Ali Çine"),
                actions=[ft.TextButton("Ok",on_click=lambda _: self.master.page.close(dlg))]
                )

        actions = []
        if title == "Login":
            actions.append(ft.ElevatedButton(text="Info", icon=ft.Icons.INFO, on_click=lambda _: self.master.page.open(dlg)),)

        actions.append(
                ft.PopupMenuButton(items=[
                                        ft.PopupMenuItem(text="Print", icon=ft.Icons.INFO),
                                        ft.PopupMenuItem(text="Quit", icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click=lambda _: self.master.page.window.destroy()),
                                        ])
                )

        super().__init__(title=ft.Text(title),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        actions=actions,
                         *args, **kwargs)


##############################
# Pages
##############################
class WelcomePage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master

        column = ft.Column([
                ft.Text("Hello!,\n\nWelcome to my Application for savig passwords safely.\n\nFirst you need to register with your master password. !!!Dont forget your master password!!! If you forget it, then you cannot reach your data!\n\nAfter you logged in, you can add your data with input fields.\n - Add 'note' to remember the use area of key and value. 'note' area must be unique.\n - 'key' area is mostly email or phone number, 'value' area is password.\n - All 'name', 'key' and 'values' are encrypted.\n\nAuthor: Ali Çine"), 
            ft.ElevatedButton(text="Okay",on_click=lambda _: self.master.page.go('/login') )
            ], alignment=CNTR)

        super().__init__(content=column, *args, **kwargs)

class LoginPage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master

        self.header = ft.Text("Welcome!", size=20)
        self.username_entry = ft.TextField(label="Username", width=300)
        self.password_entry = ft.TextField(label="Password", password=True, can_reveal_password=True,width=300)
        self.login_button= ft.ElevatedButton(text="Login", on_click=lambda _:self.login_callback() ,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300)
        self.register_button = ft.ElevatedButton(text="Register", on_click=lambda _:self.register_callback(),style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300)

        self.colon = ft.Column([
            self.header,
            self.username_entry,
            self.password_entry,
            self.login_button,
            self.register_button
            ], alignment=CNTR, horizontal_alignment=CX_CENTER)

        self.appbar = CustomAppBar(title="Login", master=self.master)

        self.container = ft.Container(content=self.colon, alignment=ft.alignment.center, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, padding=30)

        self.v_row = ft.ResponsiveRow([ ft.Column([ self.container ],col={"xs":12, "md":6}) ], alignment=CNTR)
        super().__init__(controls=[self.v_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, appbar=self.appbar)

    def login_callback(self) -> NoReturn:
        username_val = self.username_entry.value
        password_val = self.password_entry.value
        if login_check(username_val, password_val, self.master.datajson, self.master):
            userkey = get_user_key(password_val)
            self.master.username = username_val
            self.master.userkey = userkey

            usercontent = self.master.datajson[username_val]["content"]
            self.master.decrypted_content = decrypt_the_content(usercontent, userkey)
            self.master.page.go("/")
            self.master.show_alert("You are logged in!")

    def register_callback(self) -> NoReturn:
       self.master.page.go("/register")

class RegisterPage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.masterpage = master.page

        self.signup = ft.Text("Sign Up", size=20)
        self.name_entry = ft.TextField(label="Name", width=300)
        self.username_entry = ft.TextField(label="Username", width=300)
        self.password_entry = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
        self.password_two_entry = ft.TextField(label="Password (again)", width=300, password=True, can_reveal_password=True)
        self.submit = ft.ElevatedButton("Submit", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300, on_click= lambda _: self.register_callback())
        self.back = ft.IconButton(on_click=lambda _: self.master.page.go("/login"), icon=ft.Icons.KEYBOARD_RETURN)

        self.colon = ft.Column([
            self.signup,
            self.name_entry,
            self.username_entry,
            self.password_entry,
            self.password_two_entry,
            self.submit,
            self.back
            ], alignment=CNTR, horizontal_alignment=CX_CENTER)

        self.appbar = CustomAppBar(title="Register", master=self.master)

        self.container = ft.Container(content=self.colon, alignment=ft.alignment.center, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, padding=30, )

        self.v_row = ft.ResponsiveRow([ ft.Column([ self.container ],col={"xs":12, "md":6}) ], alignment=CNTR)
        super().__init__(controls=[self.v_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, appbar=self.appbar)


    def register_callback(self):
        if register_check(self.name_entry.value, self.username_entry.value, self.password_entry.value, self.password_two_entry.value, self.master.datajson, self.master):
            psswd = self.password_entry.value
            add_new_user(username=self.username_entry.value,name=self.name_entry.value, password_hashed=get_hashed_password(psswd), password_raw=psswd)
            self.master.reload_data()
            self.master.page.go("/login")
            self.master.show_alert("You are registered!")


class ContentPage(ft.View):
    def __init__(self, master):
        self.master = master
        self.colon = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        self.appbar = CustomAppBar(title="Content", master=self.master)

        self.initialize_content()
        self.container = ft.Container(content=self.colon, expand=True, margin=ft.margin.symmetric(horizontal=40))
        super().__init__(controls=[self.container], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS, appbar=self.appbar)

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

        self.dt = ft.DataTable(columns=cols, rows=rows, expand=True)
        self.colon.controls.append(ft.Row([self.dt], alignment=ft.MainAxisAlignment.CENTER))
        self.master.page.update()

    def show_callback(self, g:int):
        i = g
        row_group = getattr(self, f'row_group{i}')

        key_control = row_group.cells[1].content.controls[0]
        key_control.password = not key_control.password

        value_control = row_group.cells[2].content.controls[0]
        value_control.password = not value_control.password

        self.master.page.update()

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
        self.master.page.update()

    def get_serialized_content(self) -> dict:
        serialized = {}
        values = ["note","key","value"]
        for datarow in self.dt.rows:
            # note, key and value cells
            note_value = datarow.cells[0].content.controls[0].value 
            key_value = datarow.cells[1].content.controls[0].value 
            value_value = datarow.cells[2].content.controls[0].value
            serialized[note_value]= {"key":key_value, "value":value_value}

        print(serialized)

