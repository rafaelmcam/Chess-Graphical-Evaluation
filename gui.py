from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
#from definitions import *

Move_Im_Pos = (0, 30)
Graph_Im_Pos = (410, 60)

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
        self.game_len = len([name for name in os.listdir('Moves/')])

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

        edit = Menu(menu)
        edit.add_command(label="Next Image", command=self.showImg)
        edit.add_command(label="Show Text", command=self.showTxt)
        
        menu.add_cascade(label = "Edit", menu=edit)

        #initial image
        load = Image.open("Moves/1.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=Move_Im_Pos[0], y=Move_Im_Pos[1])
        load.close()

        load = Image.open("Graphs/1.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=Graph_Im_Pos[0], y=Graph_Im_Pos[1])
        load.close()

        B1 = Button(self.master, text = 'Previous picture', command = lambda: self.showImg(-1)).pack(side = LEFT)
        B2 = Button(self.master, text = 'Next picture', command = lambda: self.showImg(1)).pack(side = LEFT)
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
        # load = Image.open("Moves/{}.png".format(self.move_n))
        # render = ImageTk.PhotoImage(load)

        # img = Label(self, image=render)
        # img.image = render
        # img.place(x=Move_Im_Pos[0], y=Move_Im_Pos[1])

        # load = Image.open("Graphs/{}.png".format(self.move_n))
        # render = ImageTk.PhotoImage(load)

        # img = Label(self, image=render)
        # img.image = render
        # img.place(x=400, y=30)
        return

    def showTxt(self):
        text = Label(self, text="Hey there!")
        text.pack()

    def client_exit(self):
        exit()

# root = Tk()
# root.geometry("400x300")

# app = Window(root)
# root.mainloop()