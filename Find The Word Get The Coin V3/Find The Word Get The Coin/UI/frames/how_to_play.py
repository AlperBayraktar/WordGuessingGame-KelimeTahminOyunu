from tkinter import ttk

class how_to_play:
    def __init__(self, lang, go_back):
        self.frame = ttk.Frame()
        
        self.lbl__how_to_play = ttk.Label(self.frame, text=lang["label"]["howToPlay"])
        self.lbl__how_to_play.pack()
        
        self.btn__go_back = ttk.Button(self.frame, text=lang["btn"]["goBack"], command=go_back)
        self.btn__go_back.pack(pady=(10, 0))