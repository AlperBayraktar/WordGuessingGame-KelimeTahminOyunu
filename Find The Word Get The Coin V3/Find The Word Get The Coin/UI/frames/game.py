from multiprocessing.dummy import current_process
import random
from tkinter import messagebox as msgbox
from tkinter import ttk
import tkinter as tk
from dataclasses import dataclass



# This should be in 10 * n format to make choosable letters work as expected
CHOOSABLE_LETTER_AMOUNT = 2 * 10


# A special dataclass that is used to store player's word guess
@dataclass
class guess_letter:
    # Letter itself
    content: str
    
    # If this guess_letter is placed to guess_letters_frame via a hint, then is_hint is True
    # If this guess_letter is placed to guess_letters_frame via a choosen letter, then is_hint is False
    is_hint: bool

    # Which letter button is used to put this guess_letter to guess_letters_frame

    # TODO: UPDATE THESE TWO RULES
    # If guess_letter.is_hint is False, this can't be None, this IS a button
    # If guess_letter.is_hint is True, this IS None
    belongs_to: ttk.Button 

# A special dataclass that is used to store and manage asked word in an easier way
@dataclass
class word:
    index: int
    content: str
    description: str



class game:
    def __init__(s, lang, db, go_back, win, show_message):
        s.lang, s.go_back, s.db, s.win, s.show_message= lang, go_back, db, win, show_message
        s.words = lang["words"]

        s.frame = ttk.Frame()

        PADY = 10

        s.word_description_frame = ttk.Frame(s.frame)

        s.lbl__word_description = ttk.Label(s.word_description_frame, text="")
        s.lbl__word_description.pack()
        s.word_description_frame.pack()

        s.guess_letters_frame = ttk.Frame(s.frame)
        s.guess_letters_frame.pack(pady=PADY)


        s.lbl__user_info = ttk.Label(s.win, text="")
        s.lbl__user_info.place(x=0, y=0)

        s.choosable_letters_frame = ttk.Frame(s.frame)
        s.choosable_letters_frame.pack(pady=PADY)

        s.action_btns_frame = ttk.Frame(s.frame)
        s.action_btns_frame.pack(pady=(PADY, 0))

        s.btn__go_back = ttk.Button(s.action_btns_frame, text=lang["btn"]["goBack"], command=s.back_to_menu)
        s.btn__go_back.grid(row=0, column=0)

        ttk.Label(s.action_btns_frame, text=" ").grid(row=0, column=1)

        s.btn__get_hint = ttk.Button(s.action_btns_frame, text=lang["btn"]["getHint"], command=s.get_hint)
        s.btn__get_hint.grid(row=0, column=2)

        ttk.Label(s.action_btns_frame, text=" ").grid(row=0, column=3)

        s.btn__delete = ttk.Button(s.action_btns_frame, text=lang["btn"]["delete"], command=s.delete_last_letter_from_guess)
        s.btn__delete.grid(row=0, column=4)


    def start_game(s, open_frame):
        if s.control_is_game_finished():
            return None
        
        last_word_id = s.db.get("last_word_id")
        if last_word_id == -1:
            s.set_next_word()
        else:
            word_ = s.words[ str(last_word_id) ]
            s.current_word = word(index=last_word_id, content=word_["word"], description=word_["description"] )

        s.update_user_info()
        s.load_current_word()
        open_frame(s.frame)

    def back_to_menu(s):
        try:
            s.clean_guess_letters()
        except:
            pass
        s.lbl__user_info.config(text="")
        s.go_back()

    def clean_guess_letters(s):
        for guess_letter_ in s.guess_letters:
            guess_letter_.grid_forget()

    def load_next_word(s):
        s.set_next_word()
        s.load_current_word()

    def control_is_game_finished(s):
        if len(s.db.get("guessed_words_indexes")) == len(s.words):
            s.back_to_menu()
            s.show_message(s.lang["msg"]["youHaveFinishedTheGame"], "info")
            return True

    def set_next_word(s):
        # Generate an unguessed word id
        guessed_words_indexes = s.db.get("guessed_words_indexes")
        
        if s.control_is_game_finished():
            return None

        
        while True:
        
            # Generate an random word index
            index = random.randint(0, len(s.words) - 1)

            # If it is not guessed, set next word to it.
            if index not in guessed_words_indexes:
                word_ = s.words[str(index)]
                s.current_word = word(index=index, content=word_["word"], description=word_["description"] )
                s.db.update("last_word_id", s.current_word.index)                
                break

        try:
            s.clean_guess_letters()
        except:
            pass

    def update_user_info(s):
        s.lbl__user_info.config(text=f"{s.db.get('username')}: {s.db.get('coins')} coin")

    def load_current_word(s):
        # Set s.guess
        s.guess = [ guess_letter("", False, None)  for i in range(len(s.current_word.content)) ]

        # Set s.guess_letters
        # This array contains labels that we will use to show player's guess to player

        s.guess_letters = []
        for letter_index in range(len(s.current_word.content)):
            # Create label and add it to guess_letters (bg is white)
            
            letter = ttk.Label(s.guess_letters_frame, text="", width=3, background="#3d3c3c")
            s.guess_letters.append(letter)


        # Set choosable_letters
        s.choosable_letters = ["" for i in range(CHOOSABLE_LETTER_AMOUNT)]

        # Make sure that choosable letters contain letters of answer.
        # Otherwise player may not be able write the right answer.
        for letter in s.current_word.content:
            while True:
                random_index = random.randint(0, CHOOSABLE_LETTER_AMOUNT - 1)
                if s.choosable_letters[random_index] == "":
                    s.choosable_letters[random_index] = letter.upper()
                    break


        # Other letters will be chosen randomly
        for letter_index, letter in enumerate(s.choosable_letters):
            if letter == "" :
                s.choosable_letters[letter_index] = random.choice(s.lang["alphabet"])

        # Now convert those choosable_letters into buttons
        for index, choosable_letter in enumerate(s.choosable_letters):
            btn = ttk.Button(s.choosable_letters_frame, text=choosable_letter, width=2 )
            btn.letter = choosable_letter
            btn.config( command=lambda x=btn: s.add_new_letter_to_guess(None, False, x) )
            s.choosable_letters[index] =  btn

        # Render description
        description = ""
        for nth, word in enumerate(s.current_word.description.split(" "), 1):
            description += ( word + " " )
            if nth % 5 == 0:
                description += "\n"

        s.lbl__word_description.config(text=description)

        # Render guess letters
        col = 0
        
        for guess_letter_index, guess_letter_ in enumerate(s.guess_letters):
            # Render guess_letter
            guess_letter_.grid(row=0, column=col)
            
            # Add a space (make sure you are not adding a space when there isn't a next guess_letter)
            if guess_letter_index != len(s.guess_letters) - 1:
                ttk.Label(s.guess_letters_frame, text=" ").grid(row=0, column=col+1)

            col += 2

        # Render choosable letters
        index = 0
        for row in range( int ( CHOOSABLE_LETTER_AMOUNT / 10) ):
            for col in range(10):
                s.choosable_letters[index].grid(row=row, column=col)
                index+=1


    def add_new_letter_to_guess(s, letter_to_add, is_hint, belongs_to):
        if belongs_to != None:
            letter_to_add = belongs_to["text"]
            belongs_to.config(text="", state="disabled")
        
        for guess_letter_index, guess_letter_ in enumerate(s.guess):
            if guess_letter_.content == "":
                s.guess[guess_letter_index].content = letter_to_add
                s.guess[guess_letter_index].is_hint = is_hint


                if is_hint:
                    s.guess[guess_letter_index].belongs_to = None
                else:
                    s.guess[guess_letter_index].belongs_to = belongs_to

                break
        
        if guess_letter_index + 1 == len(s.current_word.content):
            guess = ""
            for guess_letter_ in s.guess:
                guess += guess_letter_.content


            if guess == s.current_word.content.upper():
                s.show_message(s.lang["msg"]["rightAnswerMessage"])

                s.db.update("coins", s.db.get("coins") + 10)
                s.update_user_info()

                new_guesssed_words_indexes = s.db.get("guessed_words_indexes")
                new_guesssed_words_indexes.append(s.current_word.index)
                s.db.update("guessed_words_indexes", "'{" + str(new_guesssed_words_indexes)[1:-1] + "}'")

                s.set_next_word()
                s.load_current_word()
            else:
                s.show_message(s.lang["msg"]["wrongAnswerMessage"], "error")
                s.delete_last_letter_from_guess()
            return None


        s.guess_letters[guess_letter_index].config(text=guess_letter_.content)
        
        if is_hint:
            s.guess_letters[guess_letter_index].config(foreground="#28eb2b")

    # Deletes the last deletable letter from the guess
    def delete_last_letter_from_guess(s):
        reversed_ = s.guess[::-1]

        # TODO Ask this        
        # [a, b, c, d] -> official
        # [d, c, b, a] -> reversed
        # How to convert reversed array's index to official one's ?
        for guess_letter_ in reversed_:
            if guess_letter_.content != "" and not guess_letter_.is_hint:
                guess_letter_to_delete_index =  s.guess.index(guess_letter_)

                s.guess[guess_letter_to_delete_index].content = ""
                s.guess_letters[guess_letter_to_delete_index].config(text="")

                if s.guess[guess_letter_to_delete_index].is_hint == False:
                    deleted_letter_belongs_to = s.guess[guess_letter_to_delete_index].belongs_to
                    deleted_letter_belongs_to.config(text=deleted_letter_belongs_to.letter, state="active")

                break
        else:
            s.show_message(s.lang["msg"]["noLetterToDeleteMsg"], "error")

    def get_hint(s):
        current_coins = s.db.get("coins")
        if current_coins - 20 < 0:
            s.show_message(s.lang["msg"]["outOfCoins"], "error")
            return None

        for next_letter_index, guess_letter_ in enumerate(s.guess):
            if guess_letter_.content == "":
                break

        s.add_new_letter_to_guess(s.current_word.content[next_letter_index].upper(), True, None)

        s.db.update("coins", current_coins - 20)
        s.update_user_info()
        s.db.update("hints_used", s.db.get("hints_used") + 1 )