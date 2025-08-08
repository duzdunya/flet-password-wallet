import flet as ft

class WarningAlert(ft.AlertDialog):
    def __init__(self, master, text, title=None):
        self.master = master
        self.l: "Local" = self.master.l

        if title is None:
            title = self.l.alert

        super().__init__(modal=True,
                         content=ft.Text(text, size=20),
                         actions=[ft.TextButton(self.l.ok, on_click= lambda _: self.master.page.close(self))]
                         )


