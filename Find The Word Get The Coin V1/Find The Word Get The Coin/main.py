import tkinter as tk
from game import game
from tkinter import messagebox as msgBox

class UI:
    def __init__(self):
        # create the window and make settings (pencereyi yarat ve ayarlarını yap)
        self.root = tk.Tk()
        self.fontN, self.fontS = "Arial", 18
        #self.root.option_add('*'+self.fontN, str(self.fontS))
        self.root.option_add('*Font', self.fontN + ' ' + str(self.fontS) )
        self.root.title("Find The Word Get The Coin")
        self.width, self.height = 465, 525
        # put the root to mid of the screen both horizontally and vertically
        # pencereyi yatay ve dikey olarak ekranın ortasına yerleştir
        self.x = self.root.winfo_screenwidth() // 2 - self.width // 2
        self.y = self.root.winfo_screenheight() // 2 - self.height // 2 - 30
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # code for start menu (başlangıç menüsü için kod)
        self.startFrame = tk.Frame()
        f = self.startFrame

        tk.Button(f, text='Play', command=self.startGame).pack(pady=15)
        tk.Button(f, text='Reset Data', command=self.resetData).pack(pady=15)
        tk.Button(f, text='Close', command= self.root.destroy ).pack(pady=15)

        # code for game menu
        self.gameFrame = tk.Frame()
        f = self.gameFrame

        self.pDataLbl = tk.Label(text="")

        self.questionFrame = tk.Frame(f)
        self.questionLbl = tk.Label(self.questionFrame, text="")
        self.questionLbl.pack()

        self.squareFrame = tk.Frame(f)

        self.buttonsFrame = tk.Frame(f)

        tk.Button(self.buttonsFrame, text='Back', command=self.backToStart ).grid(row=0, column=0)
        tk.Label(self.buttonsFrame, text='').grid(row=0, column=1)
        tk.Button(self.buttonsFrame, text='Hint', command=self.getHint).grid(row=0, column=2)
        tk.Label(self.buttonsFrame, text='').grid(row=0, column=3)
        tk.Button(self.buttonsFrame, text='Delete', command=self.deleteLetter ).grid(row=0, column=4)

        self.lettersFrame = tk.Frame(f)

        self.startFrame.pack(expand=True)
        self.currentMenu = self.startFrame

        self.pDataLbl.place(x=0,y=0)
        self.questionFrame.pack()
        self.squareFrame.pack(pady=25)
        self.buttonsFrame.pack(pady=15)
        self.lettersFrame.pack()

    def openWithExpand(self, frame):
        self.changeFrame(frame)
        frame.pack(expand=True)

    def changeFrame(self, frame):
        self.currentMenu.place_forget()
        self.currentMenu.pack_forget()
        frame.pack()
        self.currentMenu = frame

    def backToStart(self):
        self.pDataLbl.config(text="")
        self.openWithExpand(self.startFrame)

    def startGame(self):
        if self.game.makeGameSetup() == "GAME_FINISHED":
            self.backToStart()
            return msgBox.showinfo("Congratulations!", "Congratulations! You have finished the game!")

        self.questionLbl.config( text=self.game.words.get(self.game.pData[3])[2] )
        self.pDataLbl.config( text=f"{self.game.pData[1]} LVL - {self.game.pData[2]} COINS"  )

        self.letterButtons = []
        for index,char in enumerate(self.game.chars):
            btn = tk.Button(self.lettersFrame, text=char, width=2 )
            btn.config(command=lambda btn=btn: self.game.letterPress(btn) )
            btn.char = char
            self.letterButtons.append(btn)

            if index+1 > 11:
                btn.grid(row=1, column=index-11)
            else:
                btn.grid(row=0, column=index)
        
        self.openWithExpand(self.gameFrame)

        self.squares = []
        for square in range(len(self.game.pData[3])):
            frame = tk.Frame(self.squareFrame, padx=10, width=2)
            frame.label = tk.Label(frame, text="", width=2, bg="white")
            frame.label.pack()
            frame.grid(row=0, column=square)
            self.squares.append( frame )

    def deleteLetter(self):
        self.game.deleteLetter()

    def getHint(self):
        self.game.getHint()

    def resetData(self):
        if msgBox.askquestion("Careful!", "Are you sure you want reset your progress? This process is irrecoverable?") == "yes":
            self.game.resetData()
            return msgBox.showinfo("Done.", "Your data is resetted now.")

ui = UI()
ui.game = game(ui)
ui.root.mainloop()
