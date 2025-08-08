import flet as ft
from .abbr import *

class WelcomePage(ft.View):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.l = self.master.l

        column = ft.Column([
            ft.Markdown(
                        self.l.welcome,
                        selectable=True,
                        ),
            ft.ElevatedButton(text=self.l.ok, on_click=lambda _: self.okay_callback())
            ], alignment=CNTR, horizontal_alignment=CX_CENTER)

        self.container = ft.Container(column, padding=50, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, alignment=ft.alignment.center)
        self.v_row = ft.ResponsiveRow([ ft.Column([ self.container ],col={"xs":12, "md":6}) ], alignment=CNTR)

        super().__init__(controls=[self.v_row], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER, *args, **kwargs)

    # mainly used in Appbar
    def __str__(self):
        return "welcome"

    def okay_callback(self):
        self.master.page.go('/login')


