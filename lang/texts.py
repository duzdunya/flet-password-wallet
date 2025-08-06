class Local:
    def __init__(self, language:str):
        if language == "en":
            self.init_en()

    def init_en(self):
        self.welcome = """
# Hello!,
## Welcome to my Application.
Before you can start using this password wallet app, you need to register with your master password.
Signup and login, then start adding your data to encrypt it with your master password.

__Dont forget your master password!!! If you forget it, then you cannot reach your data!__

After you logged in, you can add your data with input fields.

- Add 'note' to remember the use area of key and value. 'note' area must be unique.
- 'key' area is mostly email or phone number, 'value' area is password.
- All 'name', 'key' and 'values' are encrypted.


Have a nice day,
Ali Çine.
                    """
        self.ok = "Ok"
        self.cancel = "Cancel"
        self.info = "Info"
        self.print = "Print"
        self.quit = "Quit"
        self.exit = "Exit"
        self.save = "Save"
        self.reload = "Reload"

        self.name = "Name"
        self.username = "Username"
        self.password = "Password"
        self.password_again = "Password (again)"
        self.login = "Login"
        self.register = "Register"
        self.submit = "Submit"

        self.new_entry = "New Entry"
        self.note = "Note"
        self.key = "Key"
        self.value = "Value"
        self.show = "Show"
        self.delete = "Delete"
        self.add = "Add"

        self.info_content = "To encrypt data in the app, you need to register before you can start storing it.\nThis app does not communicate with the internet, everything is stored locally. Content is encrypted and decrypted using your master password, master password is not stored as plain text.\n\nData located:\n\nOn Linux:\n'~/.config/password_wallet'\n\nOn macOS:\n'/Users/<username>/Library/Application Support/password_wallet'\n\nOn Windows:\n'C:\\Users\\<username>\\AppData\\Local\\duzdunya\\password_wallet'\n\nAuthor: Ali Çine"

        self.save_before_reload = "You have unsaved changes, save before reloading data."


        self.exit_sure = "You are exiting the app, are you sure?"
        self.unsaved = "Unsaved Changes"
        self.unsaved_content = "You have unsaved changes!\nYou can save or exit without saving."
        self.no_changes  = "You dont have any changes"
        self.exit_without_save = "Exit without saving"
        self.check_equal= "is equal?"

        self.added = "Added successfully!"
        self.saved = "Saved successfully!"
        self.reloaded = "Reloaded"
        self.logged_in = "You are logged in!"
        self.registered = "You have registered!"
