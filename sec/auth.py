from .encryption import get_hashed_password
import customtkinter as ctk

class PopUpFrame(ctk.CTkToplevel):
    def __init__(self,master,label="", **kwargs):
        super().__init__(master, **kwargs)
        self.label=ctk.CTkLabel(self, text=label)
        self.label.grid(row=0,column=0, padx=30, pady=30)


        self.ok = ctk.CTkButton(self, text="Ok", corner_radius=0, command=self.ok_callback)
        self.ok.grid(row=1,column=0, padx=10, pady=10)

        self.bind("<Return>",lambda x: self.ok_callback())

    def ok_callback(self):
        self.destroy()


def login_check(username:str, password:str, datajson, master) -> bool:
    if len(username)==0:
        master.popup = PopUpFrame(master, "Please give an username.")
        return False
    elif len(password)==0:
        master.popup = PopUpFrame(master, "Please give a password.")
        return False
    else:
        if len(username) < 5 or len(username) > 100:
            master.popup = PopUpFrame(master,"Username doesn't match.")
            return False
        elif len(password) < 5 or len(password) > 50:
            master.popup = PopUpFrame(master,"Password doesn't match.")
            return False
        try:
            user = datajson[username]
        except:
            master.popup = PopUpFrame(master,"Username doesn't match.")
            return False
        else:
            if datajson[username]["password"] != get_hashed_password(password):
                master.popup = PopUpFrame(master,"Password doesn't match.")
                return False

    master.popup = PopUpFrame(master,"You are logged in.")
    return True


def register_check(name:str, username:str, password_one:str, password_two:str, datajson, master):
    def is_username_used_before(username:str) -> bool:
        try:
            user = datajson[username]
        except:
            return False
        else:
            return True

    if len(name)==0:
        master.popup = PopUpFrame(master, 'Please give a name.')
        return False
    elif len(username)==0:
        master.popup = PopUpFrame(master, 'Please give an username.')
        return False
    elif len(password_one)==0:
        master.popup = PopUpFrame(master, 'Please give a password.')
        return False
    elif len(password_two)==0:
        master.popup = PopUpFrame(master, 'Please give password again.')
        return False
    else:
        if len(name) > 100:
            master.popup = PopUpFrame(master, 'The length of the name must not be greater than 100.')
            return False
        elif len(username) < 5:
            master.popup = PopUpFrame(master,'The length of the username must not be less than 5.')
            return False
        elif len(username) > 100:
            master.popup = PopUpFrame(master,'The length of the username must not be greater than 100.')
            return False
        elif len(password_one) < 5:
            master.popup = PopUpFrame(master,'The length of the password_one must not be less than 5.')
            return False
        elif len(password_one) > 50:
            master.popup = PopUpFrame(master,'The length of the password_one must not be greater than 50.')
            return False
        elif password_one != password_two:
            master.popup = PopUpFrame(master, 'Passwords are not the same.')
            return False
        elif is_username_used_before(username):
            master.popup = PopUpFrame(master, 'There is already such a user.')
            return False
    master.popup = PopUpFrame(master, "You have registered successfully")
    return True


