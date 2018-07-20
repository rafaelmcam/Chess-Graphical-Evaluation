from tkinter import *
from PIL import Image, ImageTk

Move_Im_Pos = (0, 30)


class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.master.minsize(width=400, height=435)
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

        B1 = Button(self.master, text = 'Previous picture', command = lambda: self.showImg(-1)).pack(side = LEFT)
        B2 = Button(self.master, text = 'Next picture', command = lambda: self.showImg(1)).pack(side = LEFT)
        #quitButton = Button(self, text = "Quit", command = self.client_exit)
        #quitButton.place(x=0, y=0)

    def showImg(self, delta):
        self.move_n += delta
        load = Image.open("Moves/{}.png".format(self.move_n))
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=Move_Im_Pos[0], y=Move_Im_Pos[1])

    def showTxt(self):
        text = Label(self, text="Hey there!")
        text.pack()

    def client_exit(self):
        exit()

# root = Tk()
# root.geometry("400x300")

# app = Window(root)
# root.mainloop()