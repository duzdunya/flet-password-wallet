from .encryption import get_hashed_password

def login_check(username:str, password:str, datajson, master) -> bool:
    if len(username)==0:
        master.show_snackbar(master.l.give_username)
        return False
    elif len(password)==0:
        master.show_snackbar(master.l.give_password)
        return False
    else:
        if len(username) < 5 or len(username) > 100:
            master.show_snackbar(master.l.username_match)
            return False
        elif len(password) < 5 or len(password) > 50:
            master.show_snackbar(master.l.password_match)
            return False
        try:
            user = datajson[username]
        except:
            master.show_snackbar(master.l.username_match)
            return False
        else:
            if datajson[username]["password"] != get_hashed_password(password):
                master.show_snackbar(master.l.password_match)
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
        master.show_snackbar(master.l.give_name)
        return False
    elif len(username)==0:
        master.show_snackbar(master.l.give_username)
        return False
    elif len(password_one)==0:
        master.show_snackbar(master.l.give_password)
        return False
    elif len(password_two)==0:
        master.show_snackbar(master.l.give_password_again)
        return False
    else:
        if len(name) > 100:
            master.show_snackbar(master.l.length_name_greater)
            return False
        elif len(username) < 5:
            master.show_snackbar(master.l.length_username)
            return False
        elif len(username) > 100:
            master.show_snackbar(master.l.length_username_greater)
            return False
        elif len(password_one) < 5:
            master.show_snackbar(master.l.length_password)
            return False
        elif len(password_one) > 50:
            master.show_snackbar(master.l.length_password_greater)
            return False
        elif password_one != password_two:
            master.show_snackbar(master.l.passwords_not_same)
            return False
        elif is_username_used_before(username):
            master.show_snackbar(master.l.such_user)
            return False
    return True



