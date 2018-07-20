import chess
import chess.pgn
import chess.uci
import chess.svg
import argparse
import math
import cairo
from cairosvg import svg2png
from tqdm import tqdm

class Chess_Game:
        def __init__(self, args):
                self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path = args.p, args.Inverted, args.et, args.gt, args.ep
                print("\nFile: {}\nInverted Board: {}\nEngine Evaluation Time: {}ms per move\nGif Interval: {}s\nEngine Path: {}\n".format(self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path))
                self.pgn_init()
                self.game_init()
                self.ply = 1
                #delete file in previous folders
        def pgn_init(self):
                pgn = open(self.pgn)
                self.game = chess.pgn.read_game(pgn)
                exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                pgn_string = self.game.accept(exporter)
                #use import re later or read import chess doc.
                self.Result = pgn_string[pgn_string.find("Result")+8:pgn_string.find("Result")+11]
                self.wh = pgn_string[pgn_string.find("White"):].split("\"")[1]
                self.bl = pgn_string[pgn_string.find("Black"):].split("\"")[1]
                pgn.close()
                return
        def game_init(self):
                self.engine = chess.uci.popen_engine(self.engine_path)
                self.info_handler = chess.uci.InfoHandler()
                self.engine.info_handlers.append(self.info_handler)
                self.board = self.game.board()
                self.engine.position(self.board)
        #def move_game():
                #return svg2png sem salvar e usar no tkinter depois
                #ver como fazer pra voltar jogada
                # usar board.pop?!
                
        def game_analysis(self):
                print("Engine evaluation in progress...\n")
                pbar = tqdm(self.game.main_line())
                for move in pbar:
                        self.san = self.board.san(move)
                        pbar.set_description("Evaluating {}{}{}".format(math.floor((self.ply+1)/2), '. ' if self.ply%2==1 else '...', self.san))
                        self.board.push(move)
                        self.engine.position(self.board)
                        #depois botar a linha de baixo como self.my_image = x sem dar write_to e pegar
                        #essa self.my_image e botar no tkinter
                        svg2png(bytestring = chess.svg.board(board = self.board, size = 400, lastmove = move, check = self.check_f(), flipped = self.inverted), write_to="Moves/{}.png".format(self.ply))
                        self.ply += 1
                return
        def check_f(self):
                self.checked_king_pos = -1
                if self.board.is_check():
                        if self.ply%2==0:
                                self.checked_king_pos = self.board.king(1)
                        else:
                                self.checked_king_pos = self.board.king(0)
                return
        # def svgPhotoImage(self):
        #         print(self.my_svg)
        #         #svg2png(bytestring = self.my_svg, write_to = "teste.png")                     
        #         surface = cairo.SVGSurface(aux, 400, 400)
        #         context = cairo.Context(surface)

        #         # use rsvg to render the cairo context                                      
        #         handle = Rsvg.Handle()
        #         svg = handle.new_from_data(self.my_svg.encode("utf-8"))
        #         svg.render_cairo(context)

        #         #img.write_to_png("svg.png")
  
        #         return aux
def parser():
    parser = argparse.ArgumentParser(description='Local Chess Graphical Evaluation')
    parser.add_argument('-p', metavar='pgn', default="dumb.pgn", help='PGN File to be analyzed')
    parser.add_argument('-iv', dest='Inverted', action='store_true', \
            help = 'Inverted board')
    parser.set_defaults(Inverted = False)
    parser.add_argument('-et', metavar='engine time', type = int, \
            default = 2000, help='Engine evaluation time in milisseconds')
    parser.add_argument('-gt', metavar='gif speed', type = float, \
            default = 1.0, help='Gif speed in seconds')
    parser.add_argument('-ep', metavar='engine path', type = str, \
            default = "stockfish", help='Path to local engine')
    args = parser.parse_args() 

    #print(args)
    return args