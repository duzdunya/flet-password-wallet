# About
<img width="700" height="109" alt="password wallet text last" src="https://github.com/user-attachments/assets/28f025de-0cce-426f-a503-8cdd65a6077d" />

This application serves to store your passwords, in a secure, simple way, the data is saved locally on your computer. Using the different users you have registered, the master password is entered into the application. 

**Store your passwords, locally, secure, in a simple way. Remember once, the master password.**

This software writed in python using flet and has a beautiful user interface.

Video Presentation (Turkish):
[youtube](https://www.youtube.com/watch?v=0g_oMW8kKD8&feature=youtu.be)

# Installation

## Executable

> [!IMPORTANT]
> This project is under BETA version and has bugs, i will add releases as soon as possible

Go to releases section in right panel and simply install executable file and run it.

## Build from source
**1 - Clone**
```
git clone https://github.com/duzdunya/flet-password-wallet.git
```
**2 - Create virtual environment in newly cloned directory**
```
python3 -m venv venv
```
**3 - Activate virtual environment**

on Windows
```
venv/Scripts/activate
```

on Linux/macOS
```
source venv/bin/activate
```
**4 - Install Requirements**
```
pip install -r requirements.txt
```

**5 - Build the app**

Linux:
Check the instructions for Linux
[for Linux](https://flet.dev/docs/publish/linux)

Windows:
Check the instructions for Windows
[for Windows](https://flet.dev/docs/publish/windows)

**6 Run it**
```
flet run
```
# Uninstall
Unistall is really easy in two steps.

Firstly,
if you cloned git repo, remove git repo, or if you downloaded executable, remove it.

Secondly,
remove these directories specific to your platform:

On Linux:<br>
```~/.config/password_wallet```

On macOS:<br>
```/Users/<username>/Library/Application Support/password_wallet```

On Windows:<br>
```C:\\Users\\<username>\\AppData\\Local\\duzdunya\\password_wallet```

# Todo list
> [x] Fixing bugs in delete function <br>
> [ ] Improving interface design, adding blurred background <br>
> [ ] Undo, Redo functions <br>
