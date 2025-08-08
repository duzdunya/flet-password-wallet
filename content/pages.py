from typing import NoReturn, Union
from sec.encryption import get_hashed_password, encrypt_the_content, decrypt_the_content, get_user_key
from user.data import add_new_user, save_content
from conf.settings import USER_DATA

# some brief forms
from .appbar import CustomAppBar
from .alertd import WarningAlert
from .welcomepage import WelcomePage
from .loginpage import LoginPage
from .registerpage import RegisterPage
from .contentpage import ContentPage
