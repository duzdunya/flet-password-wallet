import flet as ft
from .alertd import WarningAlert
from .appbar import CustomAppBar
from .abbr import *
from sec.auth import register_check
from user.data import add_new_user  
from sec.encryption import get_hashed_password

class RegisterPage(ft.View):
    def __init__(self, master: "MainWindow", *args, **kwargs):
        self.master = master
        self.l = self.master.l

        self.masterpage = master.page

        self.signup = ft.Text("Sign Up", size=20)
        self.name_entry = ft.TextField(label=self.l.name, width=300)
        self.username_entry = ft.TextField(label=self.l.username, width=300)
        self.password_entry = ft.TextField(label=self.l.password, width=300, password=True, can_reveal_password=True)
        self.password_two_entry = ft.TextField(label=self.l.password_again, width=300, password=True, can_reveal_password=True)
        self.submit = ft.ElevatedButton(self.l.submit, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300, on_click= lambda _: self.register_callback())
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

    # mainly used in Appbar
    def __str__(self):
        return "register"

    # check name username password
    def register_callback(self):
        if register_check(self.name_entry.value, self.username_entry.value, self.password_entry.value, self.password_two_entry.value, self.master.datajson, self.master):
            psswd = self.password_entry.value
            add_new_user(username=self.username_entry.value,name=self.name_entry.value, password_hashed=get_hashed_password(psswd), password_raw=psswd)
            self.master.reload_data()
            self.master.page.go("/login")
            self.master.show_snackbar(self.l.registered)


