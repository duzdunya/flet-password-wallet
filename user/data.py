import json
import os
from conf.settings import *
from sec import encryption

# Config file contains only key and values
default_config = {"welcome_shown":False, "bgmode":"Dark"}
default_data = {}

# Edit the config file with given key and values.
def save_config(path, key, value):
    if os.path.exists(path):
        with open(file=path,mode="r") as file:
            json_data = json.loads(file.read())
            json_data[key] = value
        with open(file=path,mode="w") as file:
            file.write(json.dumps(json_data))

# This method creates new config file if not exists.
# If exists and gives json decode error, then overwrites it as default config and returns it.
def load_config(path) -> dict:
    if os.path.exists(path):
        try:
            with open(file=path,mode="r") as file:
                data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            with open(file=path, mode="w") as file:
                file.write(json.dumps(default_config))
            return default_config
        else:
            return data
    else:
        with open(file=path, mode="w") as file:
            file.write(json.dumps(default_config))
        return default_config 

def save_data(path, username, userdata):
    if os.path.exists(path):
        with open(file=path, mode="r") as file:
            data = json.loads(file.read())
            data[username] = userdata
        with open(file=path, mode="w") as file:
            file.write(json.dumps(data))

# content must be encrypted
def save_content(path, username, content:str):
    if os.path.exists(path):
        with open(file=path, mode="r") as file:
            data = json.loads(file.read())
            try:
                data[username]
            except:
                print("There is no such a user")
            else:
                data[username]["content"] = content
        with open(file=path, mode="w") as file:
            file.write(json.dumps(data))

def load_data(path):
    if os.path.exists(path):
        try:
            with open(file=path, mode="r") as file:
                data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            with open(file=path, mode="w") as file:
                file.write(json.dumps(default_data))
            return default_data
        else:
            return data 
    else:
        with open(file=path, mode="w") as file:
            file.write(json.dumps(default_data))
        return default_data

def get_default_newuser(name,password,content) -> dict:
   return  {"name":name, "password":password, "content":content}

def add_new_user(username, name, password_hashed, password_raw, content=dict()):
    userkey = encryption.get_user_key(password_raw)
    usercontent =  encryption.encrypt_the_content(content, userkey)
    newuser_data = get_default_newuser(name, password_hashed, usercontent)
    save_data(USER_DATA, username, newuser_data)

