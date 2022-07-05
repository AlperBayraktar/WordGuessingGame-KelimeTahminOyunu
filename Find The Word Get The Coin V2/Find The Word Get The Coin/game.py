import json, random
from player import db as playerDB
from words import db as wordsDB
from tkinter import messagebox as msgBox



def playFalse():
    pass

def playTrue():
    pass

# special upper for function for turkish characters
# türkçe karakterler için özel bir büyültme fonksiyonu
def upperForTR(text):
    output = ""
    for character in text:
        if character == "ğ": output += "Ğ"
        elif character == "ü": output += "Ü"
        elif character == "i": output += "İ"
        elif character == "ö": output += "Ö"
        elif character == "ç": output += "Ç"
        else: output += character.upper()
    return output

# a class for game processes
# oyun işlemleri için bir class
class game:
    def __init__(self, uiSelf):
        # get uiSelf to update the ui
        # arayüzü yenilemek için ui'ın selfini al
        self.ui = uiSelf
        self.player = playerDB()
        self.words = wordsDB()

    def makeGameSetup(self):
        # generate a new word if there is not last_word
        # eğer en son kalınan kelime yoksa yeni bir kelime al
        self.pData = list ( self.player.get('*') )
        self.pData[3] = json.loads(self.pData[3])
        charList = self.ui.JSON["charList"]
        self.playerGuess = ""
        self.emptyButtons = []

        if self.pData[3] == {}:
            if len ( json.loads( self.player.get("guessed_words")[0] ) ) == len(self.words.conn.execute("SELECT * FROM words").fetchall() ) : 
                return "GAME_FINISHED"

            while True:
                # find a word ID which is not answered before
                # cevaplanmamış bir kelime ID'si bul
                self.currentWordID = self.words.getRandomWordID()
                if self.words.getWordData(self.currentWordID, self.ui.JSON)["word"] not in json.loads( self.player.get('guessed_words')[0] ):
                    break
                continue
            
            # update the database
            # veritabanını yenile
            self.pData[3] = self.words.getWordData(self.currentWordID, self.ui.JSON)
            self.player.update('last_word', json.dumps(self.pData[3]))

        # generate chars with 22 letters which must contain the letters of the answer
        # cevabın harflerini taşıyan 22 tane karakter oluştur
        self.answer_letter_indexes = []
        while True:
            number = random.randint(1, 22)
            if number in self.answer_letter_indexes: continue
            self.answer_letter_indexes.append(number)
            if len(self.answer_letter_indexes) == len(self.pData[3]["word"]): break
        
        self.chars = []

        if self.pData[-1] == "tr":
            for charIndex in range(1, 23):
                if charIndex in self.answer_letter_indexes:
                    self.chars.append( upperForTR( self.pData[3]["word"][self.answer_letter_indexes.index(charIndex)] ) )
                else:
                    self.chars.append( random.choice( charList ).upper() )
        else:
            for charIndex in range(1, 23):
                if charIndex in self.answer_letter_indexes: self.chars.append( self.pData[3]["word"][self.answer_letter_indexes.index(charIndex)].upper() )
                else: self.chars.append( random.choice( charList ).upper() )

        return True

    def letterPress(self, button):
        # control if pressed button is empty
        # basılan buton boş mu diye kontrol et
        if button["text"] == "": return None

        if len( self.playerGuess ) == len(self.pData[3]["word"]):
            playFalse()
        else:
            # add the word to player guess
            # player guess'e oyuncu tahminini ekle
            self.playerGuess += button["text"]

            # make the controls if the guess is true 
            # cevap doğru mu diye kontrol et
            if len( self.playerGuess ) == len(self.pData[3]["word"]):
                self.isGuessRightControl()

            # refresh the button display
            # görüntüyü yenile
            self.ui.squares[ len(self.playerGuess)-1 ].label.config(text=button["text"])
            button.config(text="")
            self.emptyButtons.append(button)

    def isGuessRightControl(self):
        if self.pData[-1] == "tr": result = self.playerGuess == upperForTR(self.pData[3]["word"])
        else: result = self.playerGuess == self.pData[3]["word"].upper()
        if result:
            self.changeGuessColor("green")
            playTrue()

            def nextQuestion(self):
                self.player.update("last_word", "{}")

                words = json.loads(self.player.get("guessed_words")[0])
                words.append(self.pData[3]["word"])
                self.player.update("guessed_words",  json.dumps(words))

                self.disableSquares()

                self.pData[2] += 10
                self.pData[1] += 1
                self.player.update("coins", self.pData[2] )
                self.player.update("level", self.pData[1] )
                self.ui.pDataLbl.config( text=f"{self.pData[1]} LVL - {self.pData[2]} COINS"  )
                self.ui.startGame()

            self.ui.root.after(1000, lambda: nextQuestion(self) )

        else:
            self.changeGuessColor("red")
            playFalse()

    def disableSquares(self):
        try:
            for square in self.ui.squares:
                square.label.pack_forget()
                square.grid_forget()
        except:
            pass
    

    def deleteLetter(self):
        # control if there is no letter
        # harf yoksa diye kontrol et
        if len(self.playerGuess) < 1:
            return playFalse()

        # remove the last letter of player guess and refresh the display
        # player guess'in son harfini sil ve görüntüyü yenile
        self.playerGuess = self.playerGuess[:-1]
        self.ui.squares[ len(self.playerGuess) ].label.config(text="")
        
        # put the letter to it's own letter button
        # harfi kendi butonuna yerleştir
        btn = self.emptyButtons[-1]
        btn.config(text=btn.char)
        self.emptyButtons.pop()

    def changeGuessColor(self, color):
        for square in self.ui.squares: square.label.config(fg=color)
        self.ui.root.after(3000, lambda: self.changeGuessColor("black") )

    def getHint(self):
        # control if player doesn't have enough coins
        # oyuncunun coin sayısını kontol et
        if self.pData[2] - 10 < 0:
            return msgBox.showerror("Error", "You're out of coins!\nYou must have at least 10 coins to get a hint.")
        elif len(self.playerGuess) == len(self.pData[3]["word"]):
            return msgBox.showerror("Oops", "There is no empty letter to give you a hint!")

        # get hint, add to playerGuess and refresh the display
        # ipucunu al, player guess'e ekle ve görüntüyü yenile
        hint = self.pData[3]["word"][ len(self.playerGuess) ]
        self.playerGuess += hint.upper()
        self.ui.squares[ len(self.playerGuess)-1 ].label.config(text=hint.upper())

        # change the text of button that contains hint to "" and add it to empty buttons list
        # ipucunun olduğu butonun metnini "" yap ve empty buttons listesine o butonu ekle
        btn = self.ui.letterButtons[ self.answer_letter_indexes[ len(self.playerGuess)-1 ] - 1 ]
        btn.config(text="")
        self.emptyButtons.append(btn)

        # descresase coinsy by 10
        # coinleri 10 azalt
        self.pData[2] -= 10
        self.player.update("coins", self.pData[2] )
        self.ui.pDataLbl.config( text=f"{self.pData[1]} LVL - {self.pData[2]} COINS"  )
    
        if len( self.playerGuess ) == len(self.pData[3]["word"]):
            self.isGuessRightControl()

    def resetData(self):
        result = self.player.resetData()
        if result[0]:
            self.disableSquares()
            return [True]
        else: return result