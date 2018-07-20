import chess
import chess.pgn
import chess.uci
import chess.svg
import argparse
import math
import cairo
import matplotlib.pyplot as plt
import numpy as np
import imageio
import sys
import os
from cairosvg import svg2png
from tqdm import tqdm
#from PIL import Image, ImageTk, ImageDraw, ImageFont

class Chess_Game:
        def __init__(self, args):
                self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path = args.p, args.Inverted, args.et, args.gt, args.ep
                print("\nFile: {}\nInverted Board: {}\nEngine Evaluation Time: {}ms per move\nGif Interval: {}s\nEngine Path: {}\n".format(self.pgn, self.inverted, self.engine_time, self.gif_time, self.engine_path))
                self.pgn_init()
                self.game_init()
                self.ply = 1
                self.eng = []
                self.jogo = []

                self.game_analysis("Moves")
                #print(self.jogo)
                self.game_lst()
                self.num_scores_f()
                self.save_graphs("Graphs")
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
                return

        def game_analysis(self, folder):
                print("Engine evaluation in progress...\n")
                pbar = tqdm(self.game.main_line())
                for move in pbar:
                        self.san = self.board.san(move)
                        pbar.set_description("Evaluating {}{}{}".format(math.floor((self.ply+1)/2), '. ' if self.ply%2==1 else '...', self.san))
                        self.board.push(move)
                        self.engine.position(self.board)
                        eng_aux = self.engine.go(movetime = self.engine_time)
                        self.eng.append((self.board.san(eng_aux[0]), self.info_handler.info["depth"], self.info_handler.info["seldepth"]))
                        svg2png(bytestring = chess.svg.board(board = self.board, size = 400, lastmove = move, check = self.check_f(), flipped = self.inverted), write_to="{}/{}.png".format(folder, self.ply))
                        self.jogo.append((self.ply, self.san, self.info_handler.info["score"][1]))
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
        def game_lst(self):
                self.gm_lst = []
                for x in self.jogo:
                        color = "White" if x[0]%2==1 else "Black"
                        if x[2][1] == None:
                                score = str(-x[2][0]) if color=="White" else str(x[2][0])
                                if int(score)>=0:
                                        score = "+" + score
                        else:
                                score = "{}{}{}".format('#', '-' if color=="Black" and x[2][1]<0 else '', abs(x[2][1]))
                        if color == "White":
                                nta = str(int(x[0]/2)+1) + ". " + str(x[1])
                        else:
                                nta = str(int(x[0]/2)) + "..." + str(x[1])
                        self.gm_lst.append((x[0], color, nta, score))
                return 

        def num_scores_f(self):
                self.num_scores = []
                for x in self.gm_lst:
                        if x[3][0]=='#':
                                if x[3][1]=='-':
                                        self.num_scores.append(-99999)
                                else:
                                        self.num_scores.append(+99999)
                        else:
                                self.num_scores.append(int(x[3]))
                return
        def save_graphs(self, folder):
                print("Saving Graphs...")
                ply =  1
                #z = np.array([0 for x in range(len(self.num_scores))])
                z = np.zeros(len(self.num_scores))
                self.num_scores = np.array(self.num_scores)
                plt.figure(figsize=(4.32, 2.88))
                for x in tqdm(self.gm_lst):
                        t = list(range(1, len(self.num_scores[:ply])+1, 1))
                        plt.plot(t, self.num_scores[:ply], color='black', marker='o', markersize=1)
                        if abs(max(self.num_scores[:ply], key=abs))<300:
                                plt.ylim(-300, 300)
                        else:
                                plt.ylim(-500, 500)
                        plt.fill_between(t, self.num_scores[:ply], 0, where=self.num_scores[:ply] >= z[:ply], facecolor='blue', interpolate=True)
                        plt.fill_between(t, self.num_scores[:ply], 0, where=self.num_scores[:ply] <= z[:ply], facecolor='red', interpolate=True)
                        plt.xticks(np.arange(1, ply+1, 5) if ply>5 else np.arange(1, 5+1, 1))
                        plt.title("Position after {}, Eval: {}".format(self.gm_lst[ply-1][2], self.num_scores[ply-1]))
                        plt.savefig("{}/{}.png".format(folder, ply))
                        ply += 1
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

def delete_files(path_list = ["Moves", "Graphs"]):
    for path in tqdm(path_list):
        fileList = os.listdir(path)
        for fileName in fileList:
            if fileName != ".gitkeep":
                os.remove(path + '/' + fileName)
    return