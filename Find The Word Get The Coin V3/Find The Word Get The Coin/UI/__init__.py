import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from info_provider import *

# Import frames
from UI.frames.main_menu import main_menu
from UI.frames.settings import settings
from UI.frames.how_to_play import how_to_play
from UI.frames.profile import profile
from UI.frames.game import game

class SCREEN_SIZES:
    MAIN_MENU = "720x430"
    HOW_TO_PLAY = "950x525"

class app_ui:
    def __init__(s, db):
        # Setup
        s.db = db
        s.load_language()

        # Create window and set size/location
        s.win = ThemedTk(theme="equilux")
        s.win.geometry(SCREEN_SIZES.MAIN_MENU)
        s.center_window()
        s.win.resizable(False, False) # unresizable

        # Styles
        style = ttk.Style(s.win)

        # Font
        s.font_name, s.font_size = "Segoe UI", 15
        s.font = (s.font_name, s.font_size)

        style.configure("TButton", font=s.font)
        style.configure("guess_letter.TLabel", font=s.font)
        s.win.option_add('*Font', s.font) # applies font automaticly
        
        # Colors
        s.win.config(bg="#464646")

        # Load frames
        s.load_ui()


    def load_ui(s):
        s.load_language()

        def go_back():
            s.open_frame(s.main_menu.frame)

        def open_how_to_play():
            s.win.geometry(SCREEN_SIZES.HOW_TO_PLAY)
            s.center_window()
            s.open_frame(s.how_to_play.frame)

        def close_how_to_play():
            go_back()
            s.win.geometry(SCREEN_SIZES.MAIN_MENU)
            s.center_window()

        def open_profile():
            s.profile.entry__player_name_input.delete(0, "end")
            s.profile.entry__player_name_input.insert(0, s.db.get("username"))
            s.profile.update_stats()
            s.open_frame(s.profile.frame)


        # Create frames
        s.main_menu = main_menu(s.lang)

        s.settings = settings(s.lang, s.font, s.db, go_back, s.load_ui, s.show_message )
        s.apply_command_to_btn(s.main_menu.btn__settings, lambda: s.open_frame(s.settings.frame))

        s.how_to_play = how_to_play(s.lang, close_how_to_play)
        s.apply_command_to_btn(s.main_menu.btn__how_to_play, open_how_to_play)

        s.profile = profile(s.lang, s.db, go_back, s.show_message)
        s.apply_command_to_btn(s.main_menu.btn__profile, open_profile )

        s.game = game(s.lang, s.db, go_back, s.win, s.show_message)
        s.apply_command_to_btn(s.main_menu.btn__game_start, lambda: s.game.start_game(s.open_frame) )

        # Pack the main menu
        s.active_frame = s.main_menu.frame # This is for initializing active_frame
        s.open_frame(s.main_menu.frame)

        SUCCESS("Loaded UI")


    # Default props center the frame
    def open_frame(self, frame_to_open, locating_type="place", options={
            "relx": 0.5,
            "rely": 0.5,
            "anchor": "center"
        }):

        self.active_frame.pack_forget()
        self.active_frame.place_forget()

        if locating_type == "place":
            frame_to_open.place(**options)
        
        elif locating_type == "pack":
            frame_to_open.pack(**options)

        self.active_frame = frame_to_open

    def load_language(self):
        # TODO player db

        with open(f"languages/{self.db.get('language')}.json", "r", encoding="utf8") as reader:
            a = reader.read()
            self.lang = json.loads(a)

        SUCCESS("Loaded language")

    def apply_command_to_btn(self, btn, command):
        btn.config(command=command)

    def run(self):
        INFO("Opening the app.")
        self.win.mainloop()

    def center_window(s):
        # Center window
        s.win.update() # Updating because otherwise winfo_width and winfo_height will be 1
        ww = s.win.winfo_width()
        wh = s.win.winfo_height()

        x = s.win.winfo_screenwidth() // 2 - ww // 2
        y = s.win.winfo_screenheight() // 2 - wh // 2 - 30
        s.win.geometry(f"{ww}x{wh}+{x}+{y}")
        s.win.title(s.lang["windowTitle"])
        
    def show_message(s, msg, type_="info"):
        msg_frame = tk.Frame(background="#3d3c3c")
        
        if type_ == "info":
            color = "#0366fc"
        elif type_ == "error":
            color = "#eb2138"
        
        msg_lbl = tk.Label(msg_frame, text=msg, foreground=color, background="#3d3c3c")
        msg_lbl.pack(padx=12, pady=5)

        def down():
            msg_frame.place_forget()
            msg_frame.y += 4
            
            msg_frame.place(x = 0, y=msg_frame.y)
            
            if not msg_frame.y > 430:
                msg_frame.after(5, down)
            else:
                msg_frame.place_forget()


        def up():
            msg_frame.place_forget()
            msg_frame.y -= 4
            
            msg_frame.place(x = 0, y=msg_frame.y)
            if not msg_frame.y < 375:
                msg_frame.after(5, up)
            else:
                msg_frame.after(1000, down )

        msg_frame.y = 430 + 80
        msg_frame.after(200, up)
        msg_frame.place(x=0, y=msg_frame.y)