from typing import NoReturn, Union
from sec.auth import login_check, register_check
from sec.encryption import get_hashed_password, encrypt_the_content, decrypt_the_content, get_user_key
from user.data import add_new_user, save_content
from conf.settings import USER_DATA
from lang.texts import Local
from PIL import Image
import flet as ft

l = Local("en")

CNTR = ft.MainAxisAlignment.CENTER
CX_CENTER = ft.CrossAxisAlignment.CENTER
##############################
# Alert and AppBar
##############################

class WarningAlert(ft.AlertDialog):
    def __init__(self, master, text, title="Alert"):
        self.master = master

        super().__init__(modal=True, content=ft.Text(text, size=20), actions=[ft.TextButton(l.ok, on_click= lambda _: self.master.page.close(self))])

class CustomAppBar(ft.AppBar):
    def __init__(self, title, master: "MainWindow", used_in:Union["View", None]=None, *args, **kwargs):
        self.master:"MainWindow" = master
        self.used_in:"View" = used_in
        self.title = title

        dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(l.info),
                content=ft.Text(l.info_content),
                actions=[ft.TextButton(l.ok, on_click=lambda _: self.master.page.close(dlg))]
                )

        actions = []
        if title == "Password Wallet | Login":
            actions.append(ft.TextButton(text=l.info, icon=ft.Icons.INFO, on_click=lambda _: self.master.page.open(dlg), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), expand=True))

        elif title == "Password Wallet | Data":
            actions.append(ft.TextButton(text=l.save, icon=ft.Icons.SAVE_SHARP, on_click=lambda _: self.used_in.save_callback()))
            actions.append(ft.TextButton(text=l.reload, icon=ft.Icons.CACHED, on_click=lambda _: self.used_in.reload_callback()))
            actions.append(ft.TextButton(text=l.print, icon=ft.Icons.INFO, on_click=lambda _: print(self.used_in.get_serialized_content()) ))
            actions.append(ft.TextButton(text=l.check_equal, icon=ft.Icons.INFO, on_click=lambda _: self.used_in.is_there_change() ))

        actions.append(
                ft.PopupMenuButton(items=[
                    ft.PopupMenuItem(text=l.quit ,icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click=lambda _: self.quit_callback()),
                    ])
                )

        super().__init__(title=ft.Text(title),
                         bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                         actions=actions,
                         *args, **kwargs)

    def quit_callback(self):
        if self.title == "Password Wallet | Data":
            if self.used_in.is_there_change():
                alert = ft.AlertDialog(modal=True,title=l.unsaved, content=ft.Text(l.unsaved_content), actions_padding=30, actions=[
                ft.TextButton(l.save, icon=ft.Icons.SAVE_SHARP, on_click= lambda _: self.exit_save_callback(alert)),
                ft.TextButton(l.exit_without_save, icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click= lambda _: self.master.page.window.destroy()),
                ft.TextButton(l.cancel,style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
             ])
                self.master.page.open(alert)
            else:
                alert = ft.AlertDialog(modal=True, title=l.exit, content=ft.Text(l.exit_sure,size=20), actions=[
                ft.TextButton(l.ok, on_click= lambda _: self.master.page.window.destroy()),
                ft.TextButton(l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
                ])
                self.master.page.open(alert)

        else:
            alert = ft.AlertDialog(modal=True, title=l.exit, content=ft.Text(l.exit_sure,size=20), actions=[
                ft.TextButton(l.ok, on_click= lambda _: self.master.page.window.destroy()),
                ft.TextButton(l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
                ])
            self.master.page.open(alert)



    def exit_save_callback(self, alert):
        self.master.page.close(alert)
        self.used_in.save_callback()


##############################
# Pages
##############################
class WelcomePage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master

        column = ft.Column([
            ft.Markdown(l.welcome,
                        selectable=True,
                        ),
            ft.ElevatedButton(text=l.ok, on_click=lambda _: self.okay_callback())
            ], alignment=CNTR, horizontal_alignment=CX_CENTER)

        self.container = ft.Container(column, padding=50, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, alignment=ft.alignment.center)
        self.v_row = ft.ResponsiveRow([ ft.Column([ self.container ],col={"xs":12, "md":6}) ], alignment=CNTR)

        super().__init__(controls=[self.v_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, *args, **kwargs)

    def okay_callback(self):
        self.master.page.go('/login')

class LoginPage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master

        self.header = ft.Text("Welcome!", size=20)
        self.username_entry = ft.TextField(label=l.username, width=300)
        self.password_entry = ft.TextField(label=l.password, password=True, can_reveal_password=True,width=300)
        self.login_button= ft.ElevatedButton(text=l.login, on_click=lambda _:self.login_callback() ,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300)
        self.register_button = ft.ElevatedButton(text=l.register, on_click=lambda _:self.register_callback(),style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300)

        self.colon = ft.Column([
            self.header,
            self.username_entry,
            self.password_entry,
            self.login_button,
            self.register_button
            ], alignment=CNTR, horizontal_alignment=CX_CENTER)

        self.appbar = CustomAppBar(title="Password Wallet | Login", master=self.master)

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
            self.master.show_snackbar(l.logged_in)

    def register_callback(self) -> NoReturn:
        self.master.page.go("/register")

class RegisterPage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.masterpage = master.page

        self.signup = ft.Text("Sign Up", size=20)
        self.name_entry = ft.TextField(label=l.name, width=300)
        self.username_entry = ft.TextField(label=l.username, width=300)
        self.password_entry = ft.TextField(label=l.password, width=300, password=True, can_reveal_password=True)
        self.password_two_entry = ft.TextField(label=l.password_again, width=300, password=True, can_reveal_password=True)
        self.submit = ft.ElevatedButton(l.submit, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300, on_click= lambda _: self.register_callback())
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

        self.appbar = CustomAppBar(title="Password Wallet | Register", master=self.master)

        self.container = ft.Container(content=self.colon, alignment=ft.alignment.center, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, padding=30, )

        self.v_row = ft.ResponsiveRow([ ft.Column([ self.container ],col={"xs":12, "md":6}) ], alignment=CNTR)
        super().__init__(controls=[self.v_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, appbar=self.appbar)


    def register_callback(self):
        if register_check(self.name_entry.value, self.username_entry.value, self.password_entry.value, self.password_two_entry.value, self.master.datajson, self.master):
            psswd = self.password_entry.value
            add_new_user(username=self.username_entry.value,name=self.name_entry.value, password_hashed=get_hashed_password(psswd), password_raw=psswd)
            self.master.reload_data()
            self.master.page.go("/login")
            self.master.show_alert(l.registered)


class ContentPage(ft.View):
    def __init__(self, master):
        self.master = master
        self.colon = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        self.appbar = CustomAppBar(title="Password Wallet | Data", master=self.master, used_in=self)
        self.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[
            ft.Text(l.new_entry),
            ft.TextField(label=l.note),
            ft.TextField(label=l.key),
            ft.TextField(label=l.value),
            ft.TextButton(l.add,icon=ft.Icons.ADD, on_click=lambda _: self.add_callback())
            ]))

        self.initialize_content()
        self.container = ft.Container(content=self.colon, expand=True, margin=ft.margin.symmetric(horizontal=40))
        super().__init__(controls=[self.container], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS, appbar=self.appbar, bottom_appbar=self.bottom_appbar)

    def initialize_content(self):
        self.colon.controls = []

        cols = [
                ft.DataColumn(ft.Text(l.note, expand=True)),
                ft.DataColumn(ft.Text(l.key, expand=True)),
                ft.DataColumn(ft.Text(l.value, expand=True)),
                ft.DataColumn(ft.Text(l.show, expand=True)),
                ft.DataColumn(ft.Text(l.delete, expand=True))
                ]
        rows = []
        decrypted_content = self.master.decrypted_content
        for i, note in enumerate(decrypted_content):
            cells = [ 
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f"{note}",  disabled=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT,on_click=lambda _, g=i, n=0: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{decrypted_content[note]["key"]}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=1: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{decrypted_content[note]["value"]}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=2: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.PREVIEW, on_click=lambda _, g=i: self.show_callback(g), expand=True)
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.DELETE, style=ft.ButtonStyle(color=ft.Colors.RED), on_click=lambda _, g=i: self.delete_callback(g), expand=True)
                         )
                     ]
            dtrow = ft.DataRow(cells=cells)
            rows.append(dtrow)

            setattr(self, f'row_group{i}', dtrow)
            setattr(self, f'cell_{i}0_editing', False)
            setattr(self, f'cell_{i}1_editing', False)
            setattr(self, f'cell_{i}2_editing', False)

        self.dt = ft.DataTable(columns=cols, rows=rows, expand=True, border=ft.border.all(0))
        self.colon.controls.append(ft.Row([self.dt], alignment=ft.MainAxisAlignment.CENTER))
        self.master.page.update()

    def save_callback(self):
        master = self.master
        if self.is_there_change(): 
            encrypted_content = encrypt_the_content(self.get_serialized_content(), master.userkey)
            try:
                save_content(USER_DATA, master.username, encrypted_content)
            except Exception as e:
                raise e
            else:
                self.master.show_snackbar(l.saved)
                self.master.reload_data()
        else:
            self.master.show_snackbar(l.no_changes)

    def reload_callback(self):
        master = self.master
        if self.is_there_change():
            master.show_snackbar(l.save_before_reload)
        else:
            master.reload_data()
            self.initialize_content()
            master.show_snackbar(l.reloaded)

    def add_callback(self):
        controls = self.bottom_appbar.content.controls
        note_val = controls[1].value
        key_val = controls[2].value
        value_val = controls[3].value

        if len(note_val) == 0:
            self.master.show_snackbar("Please add something to Note Area")
            return
        elif len(key_val) == 0:
            self.master.show_snackbar("Please add something to Key Area")
            return
        elif len(value_val) == 0:
            self.master.show_snackbar("Please add something to Value Area")
            return
        else:
            try:
                self.get_serialized_content()[note_val]
            except:
                pass
            else:
                self.master.show_snackbar("Note Area must be unique")
                return

        i = len(self.dt.rows) + 1
        cells = [ 
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f"{note_val}",  disabled=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT,on_click=lambda _, g=i, n=0: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{key_val}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=1: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{value_val}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=2: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.PREVIEW, on_click=lambda _, g=i: self.show_callback(g), expand=True)
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.DELETE, style=ft.ButtonStyle(color=ft.Colors.RED), on_click=lambda _, g=i: self.delete_callback(g), expand=True)
                         )
                     ]
        dtrow = ft.DataRow(cells=cells)
        setattr(self, f'row_group{i}', dtrow)
        setattr(self, f'cell_{i}0_editing', False)
        setattr(self, f'cell_{i}1_editing', False)
        setattr(self, f'cell_{i}2_editing', False)
        #self.master.decrypted_content[note_val] = {"key":key_val, "value":value_val}
        self.dt.rows.append(dtrow)
        self.master.show_snackbar(l.added)

        controls[1].value = ""
        controls[2].value = ""
        controls[3].value = ""
        self.master.page.update()

    # needs editing
    def delete_callback(self, g:int):
        pass

    def show_callback(self, g:int):
        i = g
        row_group = getattr(self, f'row_group{i}')

        key_control = row_group.cells[1].content.controls[0]
        key_control.password = not key_control.password

        value_control = row_group.cells[2].content.controls[0]
        value_control.password = not value_control.password

        self.master.page.update()
    
    # done
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
        for datarow in self.dt.rows:
            # note, key and value cells
            note_value = datarow.cells[0].content.controls[0].value 
            key_value = datarow.cells[1].content.controls[0].value 
            value_value = datarow.cells[2].content.controls[0].value
            serialized[note_value]= {"key":key_value, "value":value_value}

        return serialized

    # done
    def is_there_change(self) -> bool:
        decrypted: dict = self.master.decrypted_content
        serialized: dict = self.get_serialized_content()
        # if hash of twos are not equal, there is a change
        return decrypted != serialized
