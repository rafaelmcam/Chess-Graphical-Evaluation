from definitions import *
from gui import *

def ask_quit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        quit()

if __name__ == "__main__":
    cg = Chess_Game(parser())
    
    root = Toplevel()

    app = Window(root)
    root.protocol("WM_DELETE_WINDOW", ask_quit)
    root.mainloop()