from platformdirs import user_config_dir
import os

# Platformdirs's config directory specific to operating system 
# On Linux: "~/.config/app_name/"
APP_NAME = "password_wallet" 
AUTHOR_NAME = "duzdunya"
APP_DIR= user_config_dir(APP_NAME, AUTHOR_NAME, ensure_exists=True)

# Create usr directory inside config directory
# On Linux: "~/.config/app_name/usr/"
USR_DIR= os.path.join(APP_DIR, "usr")
if not os.path.exists(USR_DIR):
    os.makedirs(USR_DIR, exist_ok=True)

# Specify the files inside usr directory

# On Linux: "~/.config/app_name/usr/config.json"
USER_CONFIG = os.path.join(USR_DIR, "config.json")

# On Linux: "~/.config/app_name/usr/data.json"
USER_DATA = os.path.join(USR_DIR,"data.json")

# Get current working directory
CURRENTPATH = os.getcwd()
