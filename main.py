from tkinter import *
from tkinter import messagebox  
from PIL import ImageTk, Image
import json
from random import randint, choice
import threading

class Client:

    def __init__(self):
        with open("data/data.json") as f:
            self.data = json.load(f)
        
        mainThread = threading.Thread(target=self.quizMain, args=())
        mainThread.start()

    def quizMain(self):
        self.win = Tk()
        self.win.configure(bg='gray5')
        self.win.title("Flag Quiz")
        self.win.iconbitmap("data/icon.ico")
        self.win.resizable(False, False)
        self.win.grid_columnconfigure(0, minsize=20)
        self.win.grid_columnconfigure(2, minsize=30)
        self.win.grid_rowconfigure(0, minsize=25)
        self.win.grid_rowconfigure(4, minsize=30)
        self.win.grid_rowconfigure(6, minsize=20)
        self.win.grid_rowconfigure(8, minsize=20)

        self.indexes = []
        for num in range(0, len(self.data["country"])):
            self.indexes.append(num)

        self.topLabel = Label(self.win, text="Flag Quiz", bg="gray5", fg="ghost white" ,font=("MS Mincho", 24, "bold"))
        self.topLabel.grid(row=1, column=1)

        self.answer = self.placeFlag()

        self.input_area = Text(self.win, height=1, width=20)
        self.input_area.config(font=("MS Mincho", 16))
        self.input_area.grid(row=5, column=1, sticky=S)
        self.input_area.bind("<Return>", self._on_enter_pressed)

        self.score = 0
        self.attempted = 0
        self.score_label = Label(self.win, text=f"Score: {str(self.score)}/{str(self.attempted)}", bg="gray5", fg="green3" ,font=("MS Mincho", 16))
        self.score_label.grid(row=7, column=1, sticky=W)

        self.help = Label(self.win, text=f"Help", bg="gray1", fg="ghost white" ,font=("MS Mincho", 16), cursor='hand2', relief=RAISED, bd=2, padx=2, pady=2)
        self.help.bind("<Button-1>", self.getHelp)
        self.help.grid(row=7, column=1, sticky=NE)
            

        self.win.mainloop()

    def placeFlag(self):
            self.canvas = Canvas(self.win, bg="gray1", width=256, height=144)
            self.win.grid_rowconfigure(2, minsize=20)
            self.win.grid_rowconfigure(3, minsize=50)
            self.canvas.grid(row=3, column=1, sticky=N)
            
            if not self.indexes:
                messagebox.showinfo("Information", f"Quiz Ended with score: {str(self.score)}/{str(self.attempted)}")
                self.win.destroy()
                main = Menu()
            countryDataInd = choice(self.indexes)
            self.indexes.remove(countryDataInd)
            
                
                

            flagImgLink = self.data["country"][countryDataInd]["link"]
            flagImg = Image.open(flagImgLink)
            flagImg.thumbnail((256, 144), Image.ANTIALIAS)
            flagImg.save(flagImgLink)
            flagImg = Image.open(flagImgLink)
            wd, hg = flagImg.size
            self.canvas.configure(width = wd, height = hg)
            self.canvas.image = ImageTk.PhotoImage(flagImg)
            self.canvas.create_image(0, 0, image = self.canvas.image, anchor="nw")

            return self.data["country"][countryDataInd]["name"]
    
    def _on_enter_pressed(self, event):
        entry = self.input_area.get('1.0', 'end').strip()
        self.input_area.delete('1.0', 'end')
        if entry.lower() == str(self.answer).lower():
            self.score += 1
            self.attempted += 1
            self.score_label = Label(self.win, text=f"Score: {str(self.score)}/{str(self.attempted)}", bg="gray5", fg="green3" ,font=("MS Mincho", 16))
            self.score_label.grid(row=7, column=1, sticky=W)
            self.canvas.destroy()
            self.answer = self.placeFlag()
        else:
            self.attempted += 1
            self.score_label = Label(self.win, text=f"Score: {str(self.score)}/{str(self.attempted)}", bg="gray5", fg="green3" ,font=("MS Mincho", 16))
            self.score_label.grid(row=7, column=1, sticky=W)

    def getHelp(self, event):
        messagebox.showinfo("information", f"Answer: {self.answer}")


class Menu:

    def __init__(self):
        mainThread = threading.Thread(target=self.gui_loop, args=())
        mainThread.start()


    def gui_loop(self):
        self.win = Tk()
        self.win.configure(bg='gray5')
        self.win.title("Flag Quiz")
        self.win.iconbitmap("data/icon.ico")
        self.win.resizable(False, False)

        self.win.grid_columnconfigure(0, minsize=70)
        self.win.grid_columnconfigure(2, minsize=70)
        self.win.grid_rowconfigure(0, minsize=20)
        self.win.grid_rowconfigure(2, minsize=40)
        self.win.grid_rowconfigure(4, minsize=30)

        self.title = Label(self.win, text="World Flag Quiz", bg="gray5", fg="ghost white", font=("MS Mincho", 24, "bold"))
        self.title.grid(row=1, column=1)

        self.help = Label(self.win, text=f"Play", bg="gray1", fg="ghost white" ,font=("MS Mincho", 22), cursor='hand2', relief=RAISED, bd=4, padx=20, pady=4)
        self.help.bind("<Button-1>", self.playGame)
        self.help.grid(row=3, column=1, sticky=S)



        self.win.mainloop()


    def playGame(self, event):
        self.win.destroy()
        client = Client()



main = Menu()