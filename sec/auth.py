from .encryption import get_hashed_password

def login_check(username:str, password:str, datajson, master) -> bool:
    if len(username)==0:
        master.show_snackbar("Please give an username.")
        return False
    elif len(password)==0:
        master.show_snackbar("Please give a password.")
        return False
    else:
        if len(username) < 5 or len(username) > 100:
            master.show_snackbar("Username doesn't match.")
            return False
        elif len(password) < 5 or len(password) > 50:
            master.show_snackbar("Password doesn't match.")
            return False
        try:
            user = datajson[username]
        except:
            master.show_snackbar("Username doesn't match.")
            return False
        else:
            if datajson[username]["password"] != get_hashed_password(password):
                master.show_snackbar("Password doesn't match.")
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
        master.show_snackbar('Please give a name.')
        return False
    elif len(username)==0:
        master.show_snackbar('Please give an username.')
        return False
    elif len(password_one)==0:
        master.show_snackbar('Please give a password.')
        return False
    elif len(password_two)==0:
        master.show_snackbar('Please give password again.')
        return False
    else:
        if len(name) > 100:
            master.show_snackbar('The length of the name must not be greater than 100.')
            return False
        elif len(username) < 5:
            master.show_snackbar('The length of the username must not be less than 5.')
            return False
        elif len(username) > 100:
            master.show_snackbar('The length of the username must not be greater than 100.')
            return False
        elif len(password_one) < 5:
            master.show_snackbar('The length of the password_one must not be less than 5.')
            return False
        elif len(password_one) > 50:
            master.show_snackbar('The length of the password_one must not be greater than 50.')
            return False
        elif password_one != password_two:
            master.show_snackbar('Passwords are not the same.')
            return False
        elif is_username_used_before(username):
            master.show_snackbar('There is already such a user.')
            return False
    return True



