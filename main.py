from definitions import *
from gui import *

def ask_quit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        quit()
        
if __name__ == "__main__":

    cg = Chess_Game(parser())
    
    #print(cg.gm_lst)
    #print(cg.eng)
    
    root = Toplevel()

    app = Window(root)

    app.game_info(cg)
    
    root.protocol("WM_DELETE_WINDOW", ask_quit)
    root.mainloop()