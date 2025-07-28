import flet as ft

cntr = ft.MainAxisAlignment.CENTER

class ValueInput(ft.Container):
    def __init__(self, master):
        

class ContentPage(ft.Container):
    def __init__(self, master):

        self.note = ft.ListView(spacing=10, padding=10)
#        self.key = ft.ListView(spacing=10, padding=10)
#        self.value = ft.ListView(spacing=10, padding=10)
#        self.config = ft.ListView(spacing=10, padding=10)

        self.initialize_content()
        column = ft.Column([
            ft.Row(self.note),
            ]) 

        super().__init__()

    def initialize_content(self):
        for i in range(0,10):
            self.note.controls.append(ft.Row([ft.I],alignmet=cntr))
        

class MainWindow:
    def __init__(self,page):
        self.page = page
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change
        self.page.go("/welcome")

    def add_view(self, entrypoint:str, controls:list):
        self.page.views.append(ft.View(
            entrypoint,
            controls=controls,
            horizontal_alignment=ft.alignment.center,
            vertical_alignment=ft.MainAxisAlignment.CENTER
            ))

    def route_change(self, route):
        self.page.views.clear()

        if self.page.route == '/':
            self.add_view('/', [ContentPage(self.page)])

        self.page.update()



ft.app(MainWindow)
