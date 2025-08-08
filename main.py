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

        #flet
        self.page = page
        self.page.title = "Password Wallet"
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change

        #multilanguage
        self.change_language("en")

        #init pages
        self.welcomepage:ft.View = WelcomePage(self)
        self.loginpage:ft.View = LoginPage(self, )
        self.registerpage:ft.View = RegisterPage(self)

        self.custom_views = [self.welcomepage, self.loginpage, self.registerpage]

        # show welcome page if not showed, show loginpage else
        self.welcome_check()

    def __str__(self):
        return "mainwindow"

    def change_language(self, language:str):
        langpath = f"lang/{language}.toml"
        if os.path.exists(langpath):
            try:
                with open(langpath, "rb") as f:
                    data = tomllib.load(f)
            except Exception as e:
                raise e
            else:
                self.l = Local(data)
                self.page.update()
                print(f"Language {language} initialized!")
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
            contentpage:ft.View = ContentPage(self)
            self.page.views.append(contentpage)

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
