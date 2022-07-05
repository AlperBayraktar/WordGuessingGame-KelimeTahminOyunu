from tkinter import ttk

class main_menu:
    def __init__(self, lang):
        self.frame = ttk.Frame()
        self.buttons = ttk.Frame(self.frame)

        self.btn__game_start = ttk.Button(self.buttons, text=lang["btn"]["start"])
        self.btn__game_start.pack(pady=15)
        
        self.btn__profile = ttk.Button(self.buttons, text=lang["btn"]["profile"])
        self.btn__profile.pack(pady=15)

        self.btn__how_to_play = ttk.Button(self.buttons, text=lang["btn"]["howToPlay"] )
        self.btn__how_to_play.pack(pady=15)

        self.btn__settings = ttk.Button(self.buttons, text=lang["btn"]["settings"] )
        self.btn__settings.pack(pady=15)

        self.btn__quit = ttk.Button(self.buttons, text=lang["btn"]["quit"], command= lambda: quit())
        self.btn__quit.pack(pady=15)
        
        self.buttons.pack()