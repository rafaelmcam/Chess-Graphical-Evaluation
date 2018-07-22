from definitions import *
from gui import *

eng_PATH = "stockfish" #possibly you need to change this if you didn't sudo apt install stockfish
gui_COLOR = "#d9d9d9" #GUI Window color given in Hex (Default: "#d9d9d9" - Standard Gray)

def ask_quit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        quit()
        
if __name__ == "__main__":

    cg = Chess_Game(parser())
    
    root = Toplevel()
    app = Window(root)
    app.game_info(cg)
    
    root.protocol("WM_DELETE_WINDOW", ask_quit)
    root.mainloop()