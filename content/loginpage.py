import flet as ft
from typing import NoReturn

from .alertd import WarningAlert
from .appbar import CustomAppBar
from .abbr import *
from sec.auth import login_check
from sec.encryption import get_user_key, decrypt_the_content


class LoginPage(ft.View):
    def __init__(self, master: "MainWindow", *args, **kwargs):
        self.master = master
        self.l = self.master.l
        self.header = ft.Text(self.l.welcome, size=30, font_family="noto sans")
        self.username_entry = ft.TextField(label=self.l.username, width=300, border_color=ft.Colors.WHITE54)
        self.password_entry = ft.TextField(label=self.l.password, password=True, can_reveal_password=True, width=300, border_color=ft.Colors.WHITE54)
        self.login_button= ft.ElevatedButton(text=self.l.login, on_click=lambda _:self.login_callback(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300, color=ft.Colors.WHITE70)
        self.register_button = ft.ElevatedButton(text=self.l.register, on_click=lambda _:self.register_callback(),style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300, color=ft.Colors.WHITE70)

        self.colon = ft.Column([
            self.header,
            self.username_entry,
            self.password_entry,
            self.login_button,
            self.register_button
            ],
            alignment=CNTR,
            horizontal_alignment=CX_CENTER,
                               expand=True
                               )

        self.appbar = CustomAppBar(title=self.l.pw_login, master=self.master)
        self.v_row = ft.ResponsiveRow([ft.Column([ft.Container(content=self.colon, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), blur=4, padding=ft.padding.symmetric(50, 120))], col={"xs":12, "md":6}, alignment=CNTR, horizontal_alignment=CX_CENTER)], alignment=ft.MainAxisAlignment.CENTER, expand=True)
#ft.Container(content=self.v_row, alignment=CNTR, expand=True, image=ft.DecorationImage(src="./carbon.jpg", fit=ft.ImageFit.COVER))
        super().__init__(padding=0,controls=[ft.Container(content=self.v_row, expand=True, image=ft.DecorationImage(src="./carbon.jpg", opacity=0.5, fit=ft.ImageFit.COVER),alignment=ft.Alignment(x=0.5, y=0.5))], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, appbar=self.appbar)

    # mainly used in Appbar
    def __str__(self):
        return "login"

    def login_callback(self) -> NoReturn:
        username_val = self.username_entry.value
        password_val = self.password_entry.value
        
        # check username password
        if login_check(username_val, password_val, self.master.datajson, self.master):
            userkey = get_user_key(password_val)
            self.master.username = username_val
            self.master.userkey = userkey

            usercontent = self.master.datajson[username_val]["content"]
            self.master.decrypted_content = decrypt_the_content(usercontent, userkey)
            self.master.page.go("/")
            self.master.show_snackbar(self.l.logged_in)

    def register_callback(self) -> NoReturn:
        self.master.page.go("/register")


