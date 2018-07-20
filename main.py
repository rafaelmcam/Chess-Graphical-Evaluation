from definitions import *
from gui import *


if __name__ == "__main__":
    cg = Chess_Game(parser())
    
    root = Toplevel()

    app = Window(root)
    root.mainloop()