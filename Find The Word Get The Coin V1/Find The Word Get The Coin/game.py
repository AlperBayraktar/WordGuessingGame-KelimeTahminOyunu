import json, random
from player import db as playerDB
from words import db as wordsDB
from tkinter import messagebox as msgBox


def playFalse():
    pass

def playTrue():
    pass


def makeList(string):
    return json.loads(string)

class game:
    def __init__(self, uiSelf):
        # get "uiSelf" to update the ui (arayüzü yenilemek için ui'ın selfini al)
        self.ui = uiSelf
        self.player = playerDB()
        self.words = wordsDB()

    def makeGameSetup(self):
        # generate a new word if there is not last_word
        # eğer en son yarıda kalınan kelime yoksa yeni bir kelime al
        self.pData = list ( self.player.get('*') )
        #self.pData = list((1, 1, 50, '', '[]', '[]', '[]'))
        
        self.playerGuess = ""
        self.emptyButtons = []
        chars = ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R",
                "S","Ş","T","U","Ü","V","Y","Z"]
        if self.pData[3] == "":

            if len ( json.loads( self.player.get("guessed_words")[0] ) ) == len(self.words.conn.execute("SELECT * FROM words").fetchall() ) : 
                return "GAME_FINISHED"

            while True:
                self.pData[3] = self.words.getRandomWord()
                if self.pData[3] not in makeList(self.player.get('guessed_words')[0]):
                    break
            self.player.update('last_word', self.pData[3])

        # generate chars with 22 letters which MUST CONTAIN the letters of the answer
        self.answer_letter_indexes = []
        while True:
            number = random.randint(1, 22)
            if number in self.answer_letter_indexes: continue
            self.answer_letter_indexes.append(number)
            if len(self.answer_letter_indexes) == len(self.pData[3]): break
        
        # generate list of chars with letters of the answer
        self.chars = []
        for charIndex in range(1, 23):
            if charIndex in self.answer_letter_indexes:
                self.chars.append( self.pData[3][self.answer_letter_indexes.index(charIndex)].title() )
            else:
                self.chars.append( random.choice( chars ) )

    def letterPress(self, button):
        # control if pressed button is empty (basılan buton boş mu diye kontrol et)
        if button["text"] == "": return None

        if len( self.playerGuess ) == len(self.pData[3]):
            playFalse()
        else:
            # add the word to player guess (player guess'e oyuncu tahminini ekle)
            self.playerGuess += button["text"]

            # make the controls if the guess is true (cevap doğru mu diye kontrol et)
            if len( self.playerGuess ) == len(self.pData[3]):
                if self.playerGuess == self.pData[3].upper():
                    self.changeGuessColor("green")
                    playTrue()

                    def nextQuestion(self):
                        self.player.update("last_word", "")

                        words = json.loads(self.player.get("guessed_words")[0])
                        words.append(self.pData[3])
                        self.player.update("guessed_words",  json.dumps(words))

                        for square in self.ui.squares:
                            square.label.pack_forget()
                            square.grid_forget()
                        self.ui.squares = []

                        self.pData[2] += 10
                        self.pData[1] += 1
                        self.player.update("coins", self.pData[2] )
                        self.player.update("level", self.pData[1] )
                        self.ui.pDataLbl.config( text=f"{self.pData[1]} LVL - {self.pData[2]} COINS"  )
                        self.makeGameSetup()
                        self.ui.startGame()

                    self.ui.root.after(1000, lambda: nextQuestion(self) )

                else:
                    self.changeGuessColor("red")
                    playFalse()

            # refresh the button display (görüntüyü yenile)
            self.ui.squares[ len(self.playerGuess)-1 ].label.config(text=button["text"])
            button.config(text="")
            self.emptyButtons.append(button)

    def deleteLetter(self):
        # control if there is no letter (harf yoksa diye kontrol et) 
        if len(self.playerGuess) < 1:
            return playFalse()
        
        # remove the last letter of player guess and refresh the display
        # player guess'in son harfini sil ve görüntüyü yenile
        self.playerGuess = self.playerGuess[:len(self.playerGuess) - 1]
        self.ui.squares[ len(self.playerGuess) ].label.config(text="")
        
        btn = self.emptyButtons[ len(self.emptyButtons) - 1]
        btn.config(text=btn.char)
        self.emptyButtons.pop()

    def changeGuessColor(self, color):
        for square in self.ui.squares: square.label.config(fg=color)
        self.ui.root.after(3000, lambda: self.changeGuessColor("black") )

    def getHint(self):
        choice = msgBox.askquestion("Are you sure?", "Do you want to get a hint? It will cost 10 coins and you will be able to see the next letter of your guess.")

        if choice == "yes":
            # control if player doesn't have enough coins
            # oyuncunun coin sayısını kontol et
            if self.pData[2] - 10 == 0:
                return msgBox.showerror("Error", "You're out of coins!\nYou must have at least 10 coins to get a hint.")
            elif len(self.playerGuess) == len(self.pData[3]):
                return msgBox.showerror("Oops", "There is no empty letter to give you a hint!")

            # get hint, add to playerGuess and refresh the display
            # ipucunu al, player guess'e ekle ve görüntüyü yenile
            hint = self.pData[3][ len(self.playerGuess) ]
            self.playerGuess += hint.upper()
            self.ui.squares[ len(self.playerGuess)-1 ].label.config(text=hint.upper())

            # change the text of button that contains hint to "" and add it to empty buttons list
            # ipucunun olduğu butonun metnini "" yap ve empty buttons listesine o butonu ekle
            btn = self.ui.letterButtons[ self.answer_letter_indexes[ len(self.playerGuess)-1 ] - 1 ]
            btn.config(text="")
            self.emptyButtons.append(btn)

            # descresase coinsy by 10 (coinleri 10 azalt)
            self.pData[2] -= 10
            self.player.update("coins", self.pData[2] )
            self.ui.pDataLbl.config( text=f"{self.pData[1]} LVL - {self.pData[2]} COINS"  )
            
    
    def resetData(self):
        self.player.resetData()