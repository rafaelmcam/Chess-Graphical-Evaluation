import chess
import chess.pgn
import argparse

class Chess_Game:
    def __init__(self, args):
        self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path = args.p, args.Inverted, args.et, args.gt, args.ep
        print("\nFile: {}\nInverted Board: {}\nEngine Evaluation Time: {}ms per move\nGif Interval: {}s\nEngine Path: {}\n".format(self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path))
        self.pgn_init()
    def pgn_init(self):
        pgn = open(self.pgn)
        game = chess.pgn.read_game(pgn)
        exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
        pgn_string = game.accept(exporter)
        #use import re later or read import chess doc.
        self.Result = pgn_string[pgn_string.find("Result")+8:pgn_string.find("Result")+11]
        self.wh = pgn_string[pgn_string.find("White"):].split("\"")[1]
        self.bl = pgn_string[pgn_string.find("Black"):].split("\"")[1]
        pgn.close()
        return

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