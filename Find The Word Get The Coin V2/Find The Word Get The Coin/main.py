import json
import tkinter as tk
from game import game
from tkinter import messagebox as msgBox

# this function is used in language change and ui boot
# bu fonksiyon dil değiştirmede ve ui boot'da kullanılıyor
def getJSON(filename):
    try:
        with open(filename, "r", encoding="utf-8") as JSONreader:
            return [True, json.loads( JSONreader.read() )]
    except Exception as error:
        return [False, error]

class UI:
    def boot(self):
        # get json data according to player's language
        # oyuncunun diline göre json verisini al
        JSON =  getJSON(rf'languages/{self.game.player.get("language")[0]}.json')
        if JSON[0] == True:
            self.JSON, JSON = JSON[1], JSON[1]    
        else:
            return msgBox.showerror("Error!", f'Error:\n{JSON[1]}')

        # create the window and make settings
        # pencereyi yarat ve ayarlarını yap
        self.root = tk.Tk()
        self.root.title(JSON["rootTitle"])

        # put the root to middle of the screen both horizontally and vertically
        # pencereyi yatay ve dikey olarak ekranın ortasına yerleştir
        self.width, self.height = 465, 525
        self.x = self.root.winfo_screenwidth() // 2 - self.width // 2
        self.y = self.root.winfo_screenheight() // 2 - self.height // 2 - 30
        # set size settings
        # büyüklük ayarlarını yap
        self.root.maxsize(self.width, self.height)
        self.root.minsize(self.width, 400)
        self.root.resizable(False, False)
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # font
        self.fontN, self.fontS = "Arial", 18
        self.font = (self.fontN, self.fontS)
        self.root.option_add('*Font', self.fontN + ' ' + str(self.fontS) )

        # start menu 
        # başlangıç menüsü
        self.startFrame = tk.Frame(self.root)
        f = self.startFrame

        # menu buttons
        # menü butonları
        self.startButtons = tk.Frame(f)
        pady = 15
        tk.Button(self.startButtons, text=JSON["btn"]["start"], command=self.startGame).pack(pady=pady)
        tk.Button(self.startButtons, text=JSON["btn"]["resetData"], command=self.resetData).pack(pady=pady)
        tk.Button(self.startButtons, text=JSON["btn"]["howToPlay"], command=self.howToPlay ).pack(pady=pady)
        tk.Button(self.startButtons, text=JSON["btn"]["close"], command= self.root.destroy ).pack(pady=pady-5)

        # ui for language changing
        # dil değiştirme için ui
        self.languageFrame = tk.Frame(f)
        self.langVar = tk.StringVar()
        choices = [ "English",  "Türkçe" ]
        self.langVar.set(JSON["fullName"])

        langMenu = tk.OptionMenu(self.languageFrame, self.langVar, *choices)
        langMenu["menu"].config(font=(self.fontN, 16))
        langMenu.grid(row=0, column=0)

        tk.Button(self.languageFrame, text="OK", font=(self.fontN, 16), command=self.changeLanguage).grid(row=0, column=1)

        # game menu
        # oyun menüsü
        self.gameFrame = tk.Frame()
        f = self.gameFrame

        # label for level and coins
        # level ve coin'ler için label
        self.pDataLbl = tk.Label(text="")

        # frame and label to display description of the word
        # kelimenin açıklaması için bir frame ve label
        self.questionFrame = tk.Frame(f)
        self.questionLbl = tk.Label(self.questionFrame, text="")
        self.questionLbl.pack()

        # frame to put white bg squares to show answer length
        # beyaz arkaplanlı karelerle cevap uzunluğunu göstermek için bir frame
        self.squareFrame = tk.Frame(f)

        # buttons (empty labels are put for seperating the buttons)
        # butonlar (boş label'lar butonları ayırmak için)
        self.buttonsFrame = tk.Frame(f)
        tk.Button(self.buttonsFrame, text=JSON["btn"]["backToStart"], command=self.backToStart ).grid(row=0, column=0)
        tk.Label(self.buttonsFrame, text='').grid(row=0, column=1)
        tk.Button(self.buttonsFrame, text=JSON["btn"]["hint"], command=self.getHint).grid(row=0, column=2)
        tk.Label(self.buttonsFrame, text='' ).grid(row=0, column=3)
        tk.Button(self.buttonsFrame, text=JSON["btn"]["delete"], command=self.deleteLetter ).grid(row=0, column=4)

        # frame to put 22 letters
        # 22 harfi koymak için frame
        self.lettersFrame = tk.Frame(f)

        # placing start menu stuff
        # başlangıç menüsü frame'lerini konumlandır
        self.startButtons.pack()
        self.languageFrame.pack(pady=20)
        self.startFrame.pack(expand=True)        
        self.currentMenu = self.startFrame

        # place the frames of the game
        # oyun frame'lerini yerleştir
        self.pDataLbl.place(x=0,y=0)
        self.questionFrame.pack()
        self.squareFrame.pack(pady=25)
        self.buttonsFrame.pack(pady=15)
        self.lettersFrame.pack()

    # functions for frame placing stuff
    # frame yerleştirme olayı için fonksiyonlar
    def changeFrame(self, frame):
        # forget pack/place of the currentMenu (currentFrame)
        # açık olan konumlandırmayı sil
        self.currentMenu.place_forget()
        self.currentMenu.pack_forget()
        # pack the new one and change currentMenu
        # yenisini konumlandır ve currentMenu'yü değiştir
        frame.pack()
        self.currentMenu = frame

    def openWithExpand(self, frame):
        # change the frame but pack with expand
        # frame'i aç ama expand ile
        self.changeFrame(frame)
        frame.pack(expand=True)

    def backToStart(self):
        # back to start menu with hiding the player data
        # ana menüye dön ve oyunucu verisini gizle
        self.pDataLbl.config(text="")
        self.openWithExpand(self.startFrame)

    #----------------------------------------------------------------

    def startGame(self):
        # make game setup control and if game is finished
        # oyun setup'ını yap ve oyun bitmiş mi diye kontrol et
        if self.game.makeGameSetup() == "GAME_FINISHED":
            self.backToStart()
            return msgBox.showinfo(self.JSON["msg"]["gameFinishedTitle"], self.JSON["msg"]["gameFinishedMsg"] )
        # after setup
        # setup'tan sonra

        # update the labels
        # label'ları yenile
        self.questionLbl.config(text= self.fitToRow(toSplit = self.game.pData[3]["description"], maxRowLength=30 ) )         
        self.pDataLbl.config( text=f"{self.game.pData[1]} LVL - {self.game.pData[2]} COINS"  )

        # create white bg squares to show the length of answer and player's guess
        # cevabın uzunluğunu ve oyunucunun tahminini göstermek için beyaz arkaplanlı kutular oluştur
        self.squares = []
        for square in range(len(self.game.pData[3]["word"])):
            frame = tk.Frame(self.squareFrame, padx=10, width=2)
            frame.label = tk.Label(frame, text="", width=2, bg="white")
            frame.label.pack()
            frame.grid(row=0, column=square)
            self.squares.append( frame )

        # create 22 buttons and put them into a list
        # 22 buton yarat ve onları listeye ekle
        self.letterButtons = []
        for index,char in enumerate(self.game.chars):
            # create the button and make configurations of it
            # butonu yarat ve konfigürasyonunu yap
            btn = tk.Button(self.lettersFrame, text=char, width=2 )
            btn.config(command=lambda btn=btn: self.letterPress(btn) )
            btn.char = char
            self.letterButtons.append(btn)

            # place according to the index (row 0 or row 1)
            # index'ine göre satır 1'e veya satır 2'ye yerleşir
            if index+1 > 11: btn.grid(row=1, column=index-11)
            else: btn.grid(row=0, column=index)

        # after game and display setup open the game frame
        # oyun setup'ı ve görüntü hazırlandıktan sonra oyun frame'ini göster
        self.openWithExpand(self.gameFrame)

    #-----------------------------------------------------------------------

    # functions of the game frame buttons
    # oyun frame butonlarının fonksiyonları
    def letterPress(self, btn):
        self.game.letterPress(btn)

    def deleteLetter(self):
        self.game.deleteLetter()

    def getHint(s):
        if msgBox.askquestion(s.JSON["msg"]["getHintTitle"], s.JSON["msg"]["getHintMsg"]) == "yes":
            s.game.getHint()

    def resetData(s):
        if msgBox.askquestion(s.JSON["msg"]["resetDataQuestionTitle"], s.JSON["msg"]["resetDataQuestionMsg"]) == "yes":
            result = s.game.resetData()

            if result[0] == True: return msgBox.showinfo(s.JSON["msg"]["resetDataSuccessTitle"], s.JSON["msg"]["resetDataSuccessMsg"])
            else: return msgBox.showinfo(s.JSON["msg"]["resetDataErrorTitle"], s.JSON["msg"]["resetDataErrorMsg"]+str(result[1]))

    #-----------------------------------------------------------------------
    
    # other functions
    # diğer fonksiyonlar

    def changeLanguage(s):
        language = s.langVar.get()

        dict_ = {
            "English": "en",
            "Türkçe": "tr",
        }
        short = dict_.get(language)

        JSON =  getJSON(rf'languages/{short}.json')
        result = s.game.player.update("language", short )
        result2 = s.game.player.update("last_word", "{}")

        if result[0] and result2[0]:
            msgBox.showinfo(JSON[1]["msg"]["changeLanguageSuccessTitle"], JSON[1]["msg"]["changeLanguageSuccessMsg"] )
            s.root.destroy()
            s.boot()
            ui.root.focus()
            s.game.pData = s.game.player.get("*")
            ui.root.mainloop()
        
        if not result[0]:
            msgBox.showerror(s.JSON["msg"]["changeLanguageErrorTitle"], s.JSON["msg"]["changeLanguageErrorMsg"]+f"\n{result[1]}" )
        if not result2[0]:
            msgBox.showerror(s.JSON["msg"]["changeLanguageErrorTitle"], s.JSON["msg"]["changeLanguageErrorMsg"]+f"\n{result2[1]}" )

    def howToPlay(self):
        root = tk.Toplevel()
        root.grab_set()

        frame = tk.Frame(root)

        tk.Label(frame, text=self.JSON["howToPlayTitle"]).pack()

        text = self.fitToRow(toSplit=self.JSON["howToPlayContent"], maxRowLength=40).replace("-", "\n\n") + "\n\n"
        tk.Label(frame, text=text[1:], font=self.font ).pack(side="left")

        frame.pack(padx=20, pady=20)
        root.focus()
        root.mainloop()

    def fitToRow(self, **args):
        maxRowLength, rowLength, row, toReturn = args["maxRowLength"], 0, [], ""
        for word in args["toSplit"].split() :
            row.append(word)
            rowLength += len(word)
            if rowLength > maxRowLength:
                toReturn  += " ".join(row[:-1]) + "\n"
                row = [row[-1]]
                rowLength = len(row[0])

        return toReturn[:-1] + "\n" + " ".join(row)

ui = UI()
ui.game = game(ui)
ui.boot()
ui.root.mainloop()