from definitions import *
from gui import *


if __name__ == "__main__":
    cg = Chess_Game(parser())
    cg.game_analysis()
    #print("a")

    root = Tk()
    root.geometry("400x300")

    app = Window(root)
    root.mainloop()



#no primeiro loop salvar só a game analysis da engine e com os botoes do tkinter e mudando a imagem sem salvar
#nenhuma imagem