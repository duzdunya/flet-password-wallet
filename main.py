import os
import json
from typing import NoReturn
import flet as ft

from user import data
from conf.settings import *
from content.pages import WelcomePage, LoginPage, RegisterPage, ContentPage
from sec.encryption import decrypt_the_content


# Load the json file
# There is only 2 config files: config.json and data.json.
# They are in appropriate user directories to specific OS respectively.
configjson = data.load_config(USER_CONFIG)
datajson = data.load_data(USER_DATA)


cntr = ft.MainAxisAlignment.CENTER

class MainWindow:
    def __init__(self, page):
        self.configjson = configjson
        self.datajson = datajson
        self.username = None
        self.userkey = None
        self.decrypted_content:dict = None
        self.unsaved_changes = False

        self.page = page
        self.page.title = "Password Wallet | Login Screen"
        self.page.vertical_alignment = cntr 
        self.page.on_route_change = self.route_change
        self.welcome_check()

    def welcome_check(self):
        if not configjson["welcome_shown"]:
            self.page.go('/welcome')
        else:
            self.page.go('/login')

    def add_view(self, entrypoint:str, controls:list):
        self.page.views.append(ft.View(
            entrypoint,
            controls=controls,
            horizontal_alignment=ft.alignment.center,
            vertical_alignment=ft.MainAxisAlignment.CENTER
            ))

    def route_change(self, route):
        self.page.views.clear()

        if self.page.route = '/welcome':
            self.add_view('/welcome', [WelcomePage(self.page)])

        elif self.page.route == '/login':
            self.add_view('/login',[LoginPage(self.page)])
        
        elif self.page.route == '/register':
            self.add_view('/register', [RegisterPage(self.page)])

        elif self.page.route == '/':
            self.add_view('/',[ContentPage(self.page)])

        self.page.update()


    def reload_data(self):
        self.datajson = data.load_data(USER_DATA)
        if self.username and self.userkey:
            self.decrypted_content = decrypt_the_content(self.datajson[self.username]["content"], self.userkey)

ft.app(MainWindow)
