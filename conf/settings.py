from platformdirs import user_config_dir
import os

APP_NAME = "password_wallet" 
AUTHOR_NAME = "duzdunya"
APP_DIR= user_config_dir(APP_NAME, AUTHOR_NAME)
USR_DIR= os.path.join(APP_DIR, "usr")
if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR, exist_ok=True)
if not os.path.exists(USR_DIR):
    os.makedirs(USR_DIR, exist_ok=True)

USER_CONFIG = os.path.join(USR_DIR, "config.json")
USER_DATA = os.path.join(USR_DIR,"data.json")
CURRENTPATH = os.getcwd()
