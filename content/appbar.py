import flet as ft
from typing import Union

from .alertd import WarningAlert
from .abbr import *

class LanguageAlert(ft.AlertDialog):
    def __init__(self, master, used_in):
        self.master = master
        self.l = master.l 
        self.r_group = ft.RadioGroup( value=self.master.current_language, content=ft.Column([
            ft.Radio(value="en", label="English"),
            ft.Radio(value="tr", label="Türkçe")
            ], height=100) )

        self.actions = [ 
                         ft.Button("Select", color=ft.Colors.WHITE70, on_click= lambda _: self.lang_callback()),
                        ft.TextButton("Cancel",style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(self))
                        ]

        super().__init__(
                modal=True,
                title="Language",
                inset_padding=ft.padding.symmetric(vertical=40, horizontal=30), 
                content=self.r_group,
                actions=self.actions)

    def lang_callback(self):
        selected = self.r_group.value
        self.master.change_language(selected)
        self.master.page.close(self)

class CustomAppBar(ft.AppBar):
    def __init__(self, title, master: "MainWindow", used_in:Union["View", None]=None, *args, **kwargs):
        self.master = master
        self.l: "Local" = self.master.l

        self.used_in = used_in
        self.title = title

        dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(self.l.info),
                content=ft.Text(self.l.info_content),
                actions=[ft.TextButton(self.l.ok, on_click=lambda _: self.master.page.close(dlg))]
                )

        actions = []
        if str(self.used_in) == "login":
            actions.append(ft.TextButton(text=l.info,color=ft.Colors.WHITE70, icon=ft.Icons.INFO, on_click=lambda _: self.master.page.open(dlg), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), expand=True))

        elif str(self.used_in) == "data":
            actions.append(ft.TextButton(text=self.l.save,style=ft.ButtonStyle(color=ft.Colors.WHITE70), icon=ft.Icons.SAVE_SHARP, on_click=lambda _: self.used_in.save_callback()))
            actions.append(ft.TextButton(text=self.l.reload,style=ft.ButtonStyle(color=ft.Colors.WHITE70), icon=ft.Icons.CACHED, on_click=lambda _: self.used_in.reload_callback()))

        actions.append(ft.TextButton(text=self.l.info, style=ft.ButtonStyle(color=ft.Colors.WHITE70), icon=ft.Icons.INFO, on_click=lambda _: self.master.show_alert(self.l.info_content),))

        actions.append(
                ft.PopupMenuButton(items=[
                    ft.PopupMenuItem(text="Language", icon=ft.Icons.LANGUAGE, on_click=lambda _: self.lang_callback()),
                    ft.PopupMenuItem(text=self.l.quit, icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click=lambda _: self.quit_callback()),
                    ])
                )

        super().__init__(title=ft.Text(title),
                         bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                         actions=actions,
                         *args, **kwargs)

    def lang_callback(self):
        alrt = LanguageAlert(master=self.master, used_in=self)
        self.master.page.open(alrt)

    def quit_callback(self):
        if str(self.used_in) == "data": 
            if self.used_in.is_there_change():
                alert = ft.AlertDialog(title=self.l.unsaved,
                                       modal=True,
                                       content=ft.Text(self.l.unsaved_content),
                                       actions_padding=30,
                                       actions=[
                                           ft.TextButton(self.l.save, icon=ft.Icons.SAVE_SHARP, on_click= lambda _: self.exit_save_callback(alert)),
                                           ft.TextButton(self.l.exit_without_save, icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click= lambda _: self.master.page.window.destroy()),
                                           ft.TextButton(self.l.cancel,style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
                                           ])
                self.master.page.open(alert)
            else:
                alert = ft.AlertDialog(modal=True,
                                       title=self.l.exit,
                                       content=ft.Text(self.l.exit_sure,size=20),
                                       actions=[
                                           ft.TextButton(self.l.ok, on_click= lambda _: self.master.page.window.destroy()),
                                           ft.TextButton(self.l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
                                           ])
                self.master.page.open(alert)

        else:
            alert = ft.AlertDialog(modal=True,
                                   title=self.l.exit,
                                   content=ft.Text(self.l.exit_sure,size=20),
                                   actions=[
                                       ft.TextButton(self.l.ok, on_click= lambda _: self.master.page.window.destroy()),
                                       ft.TextButton(self.l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.master.page.close(alert))
                                       ])
            self.master.page.open(alert)

    def exit_save_callback(self, alert):
        self.master.page.close(alert)
        self.used_in.save_callback()


