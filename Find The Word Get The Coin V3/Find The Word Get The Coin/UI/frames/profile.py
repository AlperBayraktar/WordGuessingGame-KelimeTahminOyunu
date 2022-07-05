import psycopg2
from tkinter import messagebox as msgbox
from tkinter import ttk

class profile:
    def __init__(self, lang, db, go_back, show_message):
        self.lang = lang
        self.db = db
        self.show_message = show_message
        
        self.frame = ttk.Frame()
        
        self.lbl__title = ttk.Label(self.frame, text=lang["btn"]["profile"])
        self.lbl__title.pack(pady=(0, 20))

        # Get input
        self.input_frame = ttk.Frame(self.frame)
        
        self.lbl__input_type = ttk.Label(self.input_frame, text=lang["label"]["playerName"] + ":")
        self.lbl__input_type.grid(row=0, column=0)
        
        ttk.Label(self.input_frame, text="  ").grid(row=0, column=1)
        
        self.entry__player_name_input = ttk.Entry(self.input_frame)
        self.entry__player_name_input.grid(row=0, column=2)
        
        self.input_frame.pack(pady=(0, 10))

        self.btn__apply_player_name = ttk.Button(self.frame, text=lang["btn"]["apply"], command=self.apply_new_username)
        self.btn__apply_player_name.pack()


        # Statistics        
        self.stats_frame = ttk.Frame(self.frame)

        self.lbl__answered_questions = ttk.Label(self.stats_frame, text="")
        self.lbl__answered_questions.pack(pady=(15, 10))

        self.lbl__coins = ttk.Label(self.stats_frame, text="")
        self.lbl__coins.pack(pady=10)

        self.lbl__hints_used = ttk.Label(self.stats_frame, text="")
        self.lbl__hints_used.pack(pady=(10, 15))

        self.stats_frame.pack()


        # Go back
        self.btn__go_back = ttk.Button(self.frame, text=lang["btn"]["goBack"], command=go_back)
        self.btn__go_back.pack()

    def update_stats(s):
        answered_questions = len(s.db.get("guessed_words_indexes"))
        total_questions = len(s.lang["words"])
        s.lbl__answered_questions.config(text=f"{s.lang['label']['answeredQuestions']}: {answered_questions}/{total_questions}")

        s.lbl__coins.config(text=f"{s.lang['label']['coins']}: {s.db.get('coins')}")

        s.lbl__hints_used.config(text=f"{s.lang['label']['hintsUsed']}: {s.db.get('hints_used')}")


    def apply_new_username(self):
        new_username = "'" + self.entry__player_name_input.get() + "'"
        
        try:
            self.db.update("username", new_username)
        
        except psycopg2.errors.StringDataRightTruncation:
            self.show_message(self.lang["msg"]["usernameIsLongMsg"] + new_username[1:-1], "error")
            self.db.conn.rollback()
        else:
            self.show_message(self.lang["msg"]["usernameChangedMsg"] + new_username[1:-1], "info")
