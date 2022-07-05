import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox

class settings:
    def __init__(self, lang, font, db, go_back, load_ui, show_message):
        self.font = font
        self.lang = lang
        self.db = db
        self.load_ui = load_ui
        self.show_message = show_message

        self.frame = ttk.Frame()

        self.language_choices = ["English", "Türkçe"]
        self.language_files = {
            "English": "en",
            "Türkçe": "tr"
        }
        
        # This line moves app's current language to start of array
        # With this way we have two advantages:
        # - lang_var is automaticly set to index 0 of given array, which is app's current language
        # - options doesn't contain current language
        self.language_choices.insert(0, self.language_choices.pop(self.language_choices.index(lang["name"])))

        self.lbl__title = ttk.Label(self.frame, text=lang["label"]["settingsTitle"])
        self.lbl__title.pack()

        self.lbl__change_lang = ttk.Label(self.frame, text=lang["label"]["changeLanguageTitle"])
        self.lbl__change_lang.pack()

        self.lang_var = tk.StringVar()

        self.option_menu__lang= ttk.OptionMenu(self.frame, self.lang_var, *self.language_choices)
        # Font is not applied to this automaticly for some reason, so we have to set it manually
        self.option_menu__lang["menu"].config(font=font)
        self.option_menu__lang.pack(pady=10)

        self.btn__change_lang = ttk.Button(self.frame, text=lang["btn"]["apply"], command=self.apply_changes)
        self.btn__change_lang.pack(pady=10)

        self.btn__reset_data = ttk.Button(self.frame, text=lang["btn"]["resetData"], command=self.reset_data)
        self.btn__reset_data.pack()

        self.btn__go_back = ttk.Button(self.frame, text=lang["btn"]["goBack"], command=go_back)
        self.btn__go_back.pack()


    def apply_changes(self):
        lang_choice = self.lang_var.get()
        self.db.update("language", f"'{self.language_files[lang_choice]}'")

        self.show_message(self.lang["msg"]["appliedSettingsMsg"] + " " + lang_choice, "info")

        self.load_ui()

    def reset_data(self):
        if msgbox.askyesno(self.lang["msg"]["resettingDataTitle"], self.lang["msg"]["resettingDataMsg"]):
            username = self.db.get("username")
            self.db.reset_data()
            self.db.update("username", "'" + username + "'")
            self.show_message(self.lang["msg"]["resettedDataMsg"])