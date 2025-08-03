from .encryption import get_hashed_password
import customtkinter as ctk

def login_check(username:str, password:str, datajson, master) -> bool:
    if len(username)==0:
        master.show_alert("Please give an username.")
        return False
    elif len(password)==0:
        master.show_alert("Please give a password.")
        return False
    else:
        if len(username) < 5 or len(username) > 100:
            master.show_alert("Username doesn't match.")
            return False
        elif len(password) < 5 or len(password) > 50:
            master.show_alert("Password doesn't match.")
            return False
        try:
            user = datajson[username]
        except:
            master.show_alert("Username doesn't match.")
            return False
        else:
            if datajson[username]["password"] != get_hashed_password(password):
                master.show_alert("Password doesn't match.")
                return False

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
        master.show_alert('Please give a name.')
        return False
    elif len(username)==0:
        master.show_alert('Please give an username.')
        return False
    elif len(password_one)==0:
        master.show_alert('Please give a password.')
        return False
    elif len(password_two)==0:
        master.show_alert('Please give password again.')
        return False
    else:
        if len(name) > 100:
            master.show_alert('The length of the name must not be greater than 100.')
            return False
        elif len(username) < 5:
            master.show_alert('The length of the username must not be less than 5.')
            return False
        elif len(username) > 100:
            master.show_alert('The length of the username must not be greater than 100.')
            return False
        elif len(password_one) < 5:
            master.show_alert('The length of the password_one must not be less than 5.')
            return False
        elif len(password_one) > 50:
            master.show_alert('The length of the password_one must not be greater than 50.')
            return False
        elif password_one != password_two:
            master.show_alert('Passwords are not the same.')
            return False
        elif is_username_used_before(username):
            master.show_alert('There is already such a user.')
            return False
    return True



