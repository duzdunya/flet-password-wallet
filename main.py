import os
import json
import tomllib
import flet as ft

from user import data
from conf.settings import *
from content.pages import WelcomePage, LoginPage, RegisterPage, ContentPage, WarningAlert, CustomAppBar
from sec.encryption import decrypt_the_content
from lang.header import Local


# Load the json file
# There is only 2 config files: config.json and data.json.
# They are in appropriate user directories to specific OS respectively.
configjson = data.load_config(USER_CONFIG)
datajson = data.load_data(USER_DATA)

cntr = ft.MainAxisAlignment.CENTER

class MainWindow:
    def __init__(self, page):
        #cryptography
        self.configjson = configjson
        self.datajson = datajson
        self.username = None
        self.userkey = None
        self.decrypted_content:dict = None

        # self.l is setted in change_langauge
        self.l = None

        #flet
        self.page = page
        self.page.title = "Password Wallet"
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change
        self.page.fonts = {"noto sans":"fonts/NotoSans-Bold.ttf"}
        self.page.window.prevent_close = True
        self.page.window.on_event = self.event_cllbck

        #multilanguage
        self.current_language = configjson["language"]
        self.change_language(self.current_language, init=True)

        #init pages
        self.welcomepage:ft.View = WelcomePage(self)
        self.loginpage:ft.View = LoginPage(self)
        self.registerpage:ft.View = RegisterPage(self)
        self.contentpage = None

        self.custom_views = [self.welcomepage, self.loginpage, self.registerpage]

        # show welcome page if not showed, show loginpage else
        self.welcome_check()

    def __str__(self):
        return "mainwindow"

    def event_cllbck(self, e):
        if e.data == "close":
            if self.contentpage is not None:
                if self.contentpage.is_there_change():
                    alert = ft.AlertDialog(title=self.l.unsaved,
                                           modal=True,
                                           content=ft.Text(self.l.unsaved_content),
                                           actions_padding=30,
                                           actions=[
                                               ft.TextButton(self.l.save, icon=ft.Icons.SAVE_SHARP, on_click= lambda _: self.contentpage.exit_save_callback(alert)),
                                               ft.TextButton(self.l.exit_without_save, icon=ft.Icons.SENSOR_DOOR_OUTLINED, on_click= lambda _: self.page.window.destroy()),
                                               ft.TextButton(self.l.cancel,style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.page.close(alert))
                                               ])
                    self.page.open(alert)
                else:
                    alert = ft.AlertDialog(modal=True,
                                           title=self.l.exit,
                                           content=ft.Text(self.l.exit_sure,size=20),
                                           actions=[
                                               ft.TextButton(self.l.ok, on_click= lambda _: self.master.page.window.destroy()),
                                               ft.TextButton(self.l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.page.close(alert))
                                               ])
                    self.page.open(alert)

            else:
                alert = ft.AlertDialog(modal=True,
                                       title=self.l.exit,
                                       content=ft.Text(self.l.exit_sure,size=20),
                                       actions=[
                                           ft.TextButton(self.l.ok, on_click= lambda _: self.page.window.destroy()),
                                           ft.TextButton(self.l.cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE), on_click= lambda _: self.page.close(alert))
                                           ])
                self.page.open(alert)

    def change_language(self, language:str, init:bool=False):
        langpath = f"lang/{language}.toml"
        if language == self.current_language and not init:
            return
        elif os.path.exists(langpath):
            try:
                with open(langpath, "rb") as f:
                    lang_data = tomllib.load(f)
            except Exception as e:
                raise e
            else:
                if not init:
                    data.save_config(USER_CONFIG, "language", language)
                    self.show_snackbar(f"Language {language} selected, please restart app to apply it.")
                self.current_language = language
                self.l = Local(lang_data)
                self.page.update()
        else:
            self.change_language("en")
            self.show_snackbar(f"There is no language file called {language}. Default setted to english.")

    def welcome_check(self):
        if not configjson["welcome_shown"]:
            self.page.go('/welcome')
            data.save_config(USER_CONFIG, "welcome_shown", True)
        else:
            self.page.go('/login')

    def route_change(self, route):
        self.clear_views()

        if self.page.route == '/welcome':
            self.page.views.append(self.custom_views[0])
        elif self.page.route == '/login':
            self.page.views.append(self.custom_views[1])
        elif self.page.route == '/register':
            self.page.views.append(self.custom_views[2])
        elif self.page.route == '/':
            self.contentpage:ft.View = ContentPage(self)
            self.page.views.append(self.contentpage)

        self.page.update()
    
    def clear_views(self):
        self.page.views.clear()

    def reload_data(self):
        self.datajson = data.load_data(USER_DATA)
        if self.username and self.userkey:
            self.decrypted_content = decrypt_the_content(self.datajson[self.username]["content"], self.userkey)

    def show_alert(self, text):
        warn = WarningAlert(self, text=text)
        self.page.open(warn)

    def show_snackbar(self, text):
        snack = ft.SnackBar(ft.Text(text, size=20), show_close_icon=True, bgcolor=ft.Colors.SECONDARY, )
        self.page.open(snack)

ft.app(MainWindow)
