import customtkinter as ctk
from typing import NoReturn
from sec.auth import login_check, register_check, PopUpFrame
from sec.encryption import get_hashed_password, encrypt_the_content, decrypt_the_content, get_user_key
from user.data import add_new_user, save_content
from conf.settings import USER_DATA
from tkinter import WORD
from PIL import Image
import flet as ft

##############################
# New Pages
##############################
class WelcomePage(ft.Container):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        column = ft.Column([ft.Row([ft.Text('Hello!,\n\nWelcome to my Application for savig passwords safely.\n\nFirst you need to register with your master password. !!!Dont forget your master password!!! If you forget it, then you cannot reach your data!\n\nAfter you logged in, you can add your data with input fields.\n - Add 'note' to remember the use area of key and value. 'note' area must be unique.\n - 'key' area is mostly email or phone number, 'value' area is password.\n - All 'name', 'key' and 'values' are encrypted.\n\nAuthor: Ali Çine')],alignment=cntr), ft.Row([ft.ElevatedButton(text="Okay",on_click=lambda _: self.master.go('/login'))],alignment=cntr)])
        super().__init__(content=column, *args, **kwargs)

class LoginPage(ft.Container):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.header = ft.TextField("Welcome!")
        self.username_entry = ft.TextField(label="Username", width=300)
        self.password_entry = ft.TextField(label="Password", password=True, width=300)
        self.login_button= ft.ElevatedButton(text="Login", on_click=self.login_callback ,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)), width=300)
        self.register_button
        self.info_button

        column = ft.Column([
            ft.Row([username_input],alignment=cntr),
            ft.Row([password_input],alignment=cntr),
            ft.Row([submit_button],alignment=cntr)])

        super().__init__(content=column, bgcolor=ft.Colors.WHITE10, width=500,*args, **kwargs)


    def login_callback(self) -> NoReturn:
        if login_check(self.username_entry.get(), self.password_entry.get(), self.master.datajson, self.master):
            usercontent = self.master.datajson[self.username_entry.get()]["content"]
            userkey = get_user_key(self.password_entry.get())
            self.master.username = self.username_entry.get()
            self.master.userkey = userkey
            self.master.decrypted_content = decrypt_the_content(usercontent, userkey)
            self.master.change_page(self, self.master.contentpage)

    def info_callback(self) -> NoReturn:
        self.master.popup = PopUpFrame(self,"To encrypt data in the app, you need to register before you can start storing it.\n This app does not communicate with the internet, everything is stored locally. Content is encrypted and decrypted using your master password, master password is not stored as plain text.\n\n Data is stored\n\nOn Linux:\n'~/.config/password_wallet'\n\nOn macOS:\n'/Users/<username>/Library/Application Support/password_wallet'\n\nOn Windows:\n'C:\\Users\\<username>\\AppData\\Local\\duzdunya\\password_wallet'\n\nAuthor: Ali Çine")


class RegisterPage(ft.Container):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.signup: "text"
        self.name_entry
        self.username_entry
        self.password_entry
        self.password_two_entry
        self.submit
        self.back

        super().__init__(*args, **kwargs)

    def register_callback(self):
        if register_check(self.name_entry.get(), self.username_entry.get(), self.password_entry.get(), self.password_two_entry.get(), self.master.datajson, self.master):
            psswd = self.password_entry.get()
            add_new_user( username=self.username_entry.get(),name=self.name_entry.get(), password_hashed=get_hashed_password(psswd), password_raw=psswd)
            self.master.reload_data()
            self.master.change_page(self, self.master.loginpage)


class ContentPage(ft.Container):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.visibility_on = ctk.CTkImage(Image.open("assets/visibility.png"))
        self.visibility_off = ctk.CTkImage(Image.open("assets/visibility-off.png"))
        self.initialize_content()
        super().__init__(*args, **kwargs)

    def initialize_content(self):
        self.content = None


##############################
# Legacy Pages
##############################
class CContentPage(ctk.CTkScrollableFrame):
    def __init__(self, master):

    def grid(self, *args, **kwargs):
        super().grid(sticky="nsew",*args, **kwargs)
        self.initialize_content()

    def initialize_content(self):
        for x in self.winfo_children():
            x.grid_forget()

        note_title= ctk.CTkLabel(self, text="Note")
        note_title.grid(row=0, column=0)

        key_title = ctk.CTkLabel(self, text="Key")
        key_title.grid(row=0, column=1)

        value_title = ctk.CTkLabel(self, text="Value")
        value_title.grid(row=0, column=2)

        decrypted:dict = self.master.decrypted_content
        # format for "decrypted" content is:
        #  {"note":
        #    {"key": ,
        #    "value": value},
        #  }
        for index,i in enumerate(decrypted):
            setattr(self, f'note_entry{index}', ctk.CTkEntry(self,corner_radius=0))
            note_entry=getattr(self, f'note_entry{index}')
            note_entry.grid(row=index+1, column=0, sticky="nsew")
            note_entry.insert("0",i)
            note_entry.configure(state="readonly")

            setattr(self, f'key_entry{index}', ctk.CTkEntry(self,corner_radius=0))
            key_entry = getattr(self, f'key_entry{index}')
            key_entry.grid(row=index+1, column=1, sticky="nsew")
            key_entry.insert("0",decrypted[i]["key"])
            key_entry.configure(state="readonly")

            setattr(self, f'value_entry{index}', ctk.CTkEntry(self, corner_radius=0, show="*"))
            setattr(self, f'value_entry_state{index}',False)

            value_entry = getattr(self, f'value_entry{index}')
            value_entry.grid(row=index+1, column=2, sticky="nsew")
            value_entry.insert("0",decrypted[i]["value"])
            value_entry.configure(state="readonly")

            setattr(self, f'show_value_btn{index}', ctk.CTkButton(self,text="", image=self.visibility_off, corner_radius=50, command= lambda ix=index: self.show_btn(ix), width=10, height=10))
            getattr(self, f'show_value_btn{index}').grid(row=index+1, column=3, sticky="w", padx=5)

        len_dec = len(decrypted)
        self.note_add = ctk.CTkEntry(self, placeholder_text="add Note", corner_radius=0)
        self.note_add.grid(row=len_dec+1, column=0, pady=(30,0), sticky="nsew")

        self.key_add = ctk.CTkEntry(self, placeholder_text="add Key", corner_radius=0)
        self.key_add.grid(row=len_dec+1, column=1, pady=(30,0), sticky="nsew")

        self.value_add= ctk.CTkEntry(self, placeholder_text="add Value", corner_radius=0)
        self.value_add.grid(row=len_dec+1, column=2, pady=(30,0), sticky="nsew")



        self.add_button = ctk.CTkButton(self, text="Add", command=self.callback_add, corner_radius=0)
        self.add_button.grid(row=len_dec+1, column=3, pady=(30,0), sticky="nsew")

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit_callback, corner_radius=0, fg_color="#F23333", hover_color="#C62828")
        self.quit_button.grid(row=len_dec+2, column=0, pady=(30,0), sticky="nsew")

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_callback, corner_radius=0)
        self.save_button.grid(row=len_dec+2, column=1, pady=(30,0), sticky="nsew")

        self.reload_button = ctk.CTkButton(self, text="Reload", command=self.reload_callback, corner_radius=0)
        self.reload_button.grid(row=len_dec+2, column=2, pady=(30,0), sticky="nsew")

    def show_btn(self, ix):
        value_entry = getattr(self, f'value_entry{ix}')
        if getattr(self, f'value_entry_state{ix}'):
            value_entry.configure(show="*")
            getattr(self, f'show_value_btn{ix}').configure(image=self.visibility_off)
            setattr(self, f'value_entry_state{ix}',False)
        else:
            value_entry.configure(show="")
            getattr(self, f'show_value_btn{ix}').configure(image=self.visibility_on)
            setattr(self, f'value_entry_state{ix}',True)

    def quit_callback(self):
        master = self.master
        if master.unsaved_changes:
            master.popup = PopUpFrame(master, "You have unsaved changes!")
        else:
            self.master.quit()

    def save_callback(self):
        master = self.master
        if master.unsaved_changes:
            encrypted_content = encrypt_the_content(master.decrypted_content, master.userkey)
            try:
                save_content(USER_DATA, master.username, encrypted_content)
            except Exception as e:
                raise e
            else:
                master.unsaved_changes = False
                master.popup = PopUpFrame(master, "Saved Successfully.")
        else:
            master.popup = PopUpFrame(master, "You dont have any changes.")

    def reload_callback(self):
        master = self.master
        if master.unsaved_changes:
            master.popup = PopUpFrame(master, "You have unsaved changes, save before reloading data.")
        else:
            master.reload_data()
            self.initialize_content()

    def callback_add(self):
        master = self.master

        note_val = self.note_add.get()
        key_val = self.key_add.get()
        value_val = self.value_add.get()

        if len(note_val) == 0:
            master.popup = PopUpFrame(master, "Please add something to Note Area")
            return
        elif len(key_val) == 0:
            master.popup = PopUpFrame(master, "Please add something to Key Area")
            return
        elif len(value_val) == 0:
            master.popup = PopUpFrame(master, "Please add something to Value Area")
            return
        else:
            try:
                master.decrypted_content[note_val]
            except:
                pass
            else:
                master.popup = PopUpFrame(master, "Note Area must be unique")
                return
        master.decrypted_content[note_val] = {"key":key_val, "value":value_val}
        master.unsaved_changes = True
        master.popup = PopUpFrame(master, "Added Successfully")
        self.initialize_content()

