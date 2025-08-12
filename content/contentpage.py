import flet as ft

from .alertd import WarningAlert
from .appbar import CustomAppBar
from .abbr import *
from sec.encryption import get_hashed_password, encrypt_the_content, decrypt_the_content
from user.data import save_content
from conf.settings import USER_DATA


class ContentPage(ft.View):
    def __init__(self, master: "MainWindow"):
        self.master = master
        self.l = self.master.l

        self.colon = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        self.appbar = CustomAppBar(title="Password Wallet | Data", master=self.master, used_in=self)
        self.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[
            ft.Text(self.l.new_entry),
            ft.TextField(label=self.l.note),
            ft.TextField(label=self.l.key),
            ft.TextField(label=self.l.value),
            ft.TextButton(self.l.add,icon=ft.Icons.ADD, on_click=lambda _: self.add_callback())
            ]))
        self.container = ft.Container(content=self.colon, expand=True, margin=ft.margin.symmetric(horizontal=40))
        super().__init__(controls=[self.container], horizontal_alignment=CX_CENTER, vertical_alignment=CNTR, scroll=ft.ScrollMode.ALWAYS, appbar=self.appbar, bottom_appbar=self.bottom_appbar)
        self.master.page.update()

        self.initialize_content()



    # mainly used in Appbar
    def __str__(self):
        return "data"

    def initialize_content(self):
        dcryptd = self.master.decrypted_content
        self.colon.controls = []

        cols = [
                ft.DataColumn(ft.Text(self.l.note, expand=True)),
                ft.DataColumn(ft.Text(self.l.key, expand=True)),
                ft.DataColumn(ft.Text(self.l.value, expand=True)),
                ft.DataColumn(ft.Text(self.l.show, expand=True)),
                ft.DataColumn(ft.Text(self.l.delete, expand=True))
                ]

        rows = []

        for i, note in enumerate(dcryptd):
            cells = [ 
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f"{note}",  disabled=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT,on_click=lambda _, g=i, n=0: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{dcryptd[note]["key"]}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=1: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.Row([
                             ft.TextField(value=f'{dcryptd[note]["value"]}', disabled=True, password=True, expand=True),
                             ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _, g=i, n=2: self.edit_callback(g,n)),
                             ])
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.PREVIEW, on_click=lambda _, g=i: self.show_callback(g), expand=True)
                         ),
                     ft.DataCell(
                         ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.RED, on_click=lambda _, g=i: self.delete_callback(g), expand=True)
                         )
                     ]
            dtrow = ft.DataRow(cells=cells)
            rows.append(dtrow)

            setattr(self, f'row_group{i}', dtrow)
            print("setted ", f"row_group{i}")
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
                self.master.show_snackbar(self.l.saved)
                self.master.reload_data()
        else:
            self.master.show_snackbar(self.l.no_changes)

    def reload_callback(self):
        master = self.master
        if self.is_there_change():
            master.show_snackbar(self.l.save_before_reload)
        else:
            master.reload_data()
            self.initialize_content()
            master.show_snackbar(self.l.reloaded)

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

        i = len(self.dt.rows)
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
                         ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.RED, on_click=lambda _, g=i: self.delete_callback(g), expand=True)
                         )
                     ]
        dtrow = ft.DataRow(cells=cells)
        setattr(self, f'row_group{i}', dtrow)
        setattr(self, f'cell_{i}0_editing', False)
        setattr(self, f'cell_{i}1_editing', False)
        setattr(self, f'cell_{i}2_editing', False)
        #self.master.decrypted_content[note_val] = {"key":key_val, "value":value_val}
        self.dt.rows.append(dtrow)
        self.master.show_snackbar(self.l.added)

        # make inputs blank after adding data
        controls[1].value = ""
        controls[2].value = ""
        controls[3].value = ""
        self.master.page.update()

    # needs editing
    def delete_callback(self, g:int):
        def del_cll(e):
            if len(self.dt.rows) != 0:
                self.dt.rows.pop(g)
                self.master.page.close(alrt)
                self.master.page.update()

        alrt = ft.AlertDialog(modal=True, title=ft.Text(self.l.sure), content=ft.Text(self.l.delete_sure), actions=[
            ft.Button(self.l.ok, on_click=del_cll),
            ft.Button(self.l.cancel, style=ft.ButtonStyle(color=ft.Colors.RED), on_click= lambda _: self.master.page.close(alrt))])
        self.master.page.open(alrt)


    def show_callback(self, g:int):
        row_group = getattr(self, f'row_group{g}')

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
