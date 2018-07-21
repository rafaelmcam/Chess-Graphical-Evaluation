from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
#from definitions import *

Move_Im_Pos = (0, 30)
Graph_Im_Pos = (410, 50)
Player_Text_Pos = (626, 30)
Text_Pos = (626, 400)

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.master.minsize(width=850, height=470)
        self.master.config()

        self.init_window()
        self.move_n = 1

        self.master.bind("<Right>", self.right_key)
        self.master.bind("<Left>", self.left_key)

    def right_key(self, event):
        self.showImg(1)

    def left_key(self, event):
        self.showImg(-1)

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill = BOTH, expand = True)
        
        menu = Menu(self.master)
        self.master.config(menu = menu)
        
        file = Menu(menu)
        file.add_command(label = "Exit", command = self.client_exit)
        menu.add_cascade(label = "File", menu=file)

        #initial image

        for x in ["Moves", "Graphs"]:
            load = Image.open("{}/1.png".format(x))
            render = ImageTk.PhotoImage(load)

            img = Label(self, image=render)
            img.image = render
            if x == "Moves":
                img.place(x=Move_Im_Pos[0], y=Move_Im_Pos[1])
            else:
                img.place(x=Graph_Im_Pos[0], y=Graph_Im_Pos[1])
            load.close()
        
        B1 = Button(self.master, text = 'Previous move', command = lambda: self.showImg(-1)).pack(side = LEFT)
        B2 = Button(self.master, text = 'Next move', command = lambda: self.showImg(1)).pack(side = LEFT)
        #quitButton = Button(self, text = "Quit", command = self.client_exit)
        #quitButton.place(x=0, y=0)

    def showImg(self, delta):
        if delta == -1 and self.move_n == 1 or delta == 1 and self.move_n == self.game_len:
            return

        self.move_n += delta
        
        for x in ["Moves", "Graphs"]:
            load = Image.open("{}/{}.png".format(x, self.move_n))
            render = ImageTk.PhotoImage(load)

            img = Label(self, image=render)
            img.image = render
            if x == "Moves":
                img.place(x=Move_Im_Pos[0], y=Move_Im_Pos[1])
            else:
                img.place(x=Graph_Im_Pos[0], y=Graph_Im_Pos[1])
            load.close()

        text = Label(self, text="\"{}\" recommendation: {:4}{:5}\nDepth: {:3}\nSel. Depth: {:3}\n".format(self.cg.engine.name, str(int(self.move_n/2)+1) + ". " if self.move_n%2==0 else str(int(self.move_n/2 + 1)) + "..." , self.cg.eng[self.move_n-1][0], self.cg.eng[self.move_n-1][1], self.cg.eng[self.move_n-1][2]))

        text.place(x=Text_Pos[0], y=Text_Pos[1], anchor="center")
        return
        
    def game_info(self, cg):
        self.cg = cg
        self.game_len = len(self.cg.gm_lst)

        #initial texts
        text = Label(self, text="{} - {} ({})".format(self.cg.game.headers["White"], self.cg.game.headers["Black"], self.cg.game.headers["Result"]))
        text.place(x=Player_Text_Pos[0], y=Player_Text_Pos[1], anchor="center")

        text = Label(self, text="\"{}\" recommendation: {:4}{:5}\nDepth: {:3}\nSel. Depth: {:3}\n".format(self.cg.engine.name, str(int(self.move_n/2)+1) + ". " if self.move_n%2==0 else str(int(self.move_n/2 + 1)) + "..." , self.cg.eng[self.move_n-1][0], self.cg.eng[self.move_n-1][1], self.cg.eng[self.move_n-1][2]))
        text.place(x=Text_Pos[0], y=Text_Pos[1], anchor="center")

        print(self.cg.gm_lst)
        print(self.cg.eng)

    def client_exit(self):
        exit()