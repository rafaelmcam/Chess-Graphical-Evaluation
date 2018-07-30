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
from main import eng_PATH, gui_COLOR

class Chess_Game:
        def __init__(self, args):
                self.pgn, self.inverted, self.engine_time, self.engine_path, self.gui_color, self.print = args.p, args.Inverted, args.et, eng_PATH, gui_COLOR, args.print

                self.delete_files()

                self.vprint("\nFile: {}\nInverted Board: {}\nEngine Evaluation Time: {}ms per move\nGUI Color: {}\nEngine Path: {}\n".format(self.pgn, self.inverted, self.engine_time, self.gui_color, self.engine_path))

                self.pgn_init()
                self.game_init()
                self.ply = 1
                self.eng = []
                self.jogo = []
                self.lst_colors = []
                self.game_analysis("Moves")
                self.game_lst()
                self.num_scores_f()
                self.save_graphs("Graphs")
                self.f_lst_colors()

        def pgn_init(self):
                pgn = open(self.pgn)
                self.game = chess.pgn.read_game(pgn)
                exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                pgn_string = self.game.accept(exporter)
                pgn.close()
                return
        def game_init(self):
                self.engine = chess.uci.popen_engine(self.engine_path)
                self.engine.uci()
                self.info_handler = chess.uci.InfoHandler()
                self.engine.info_handlers.append(self.info_handler)
                self.board = self.game.board()
                self.engine.position(self.board)
                return

        def game_analysis(self, folder):
                self.vprint("Engine evaluation in progress...\n")
                with tqdm(total = len([x for x in self.game.main_line()])) as pbar:
                        for move in self.game.main_line():
                                self.san = self.board.san(move)
                                pbar.set_description("Evaluating {:3}{:4}{:5}".format(math.floor((self.ply+1)/2), '. ' if self.ply%2==1 else '...', self.san))
                                self.board.push(move)
                                self.engine.position(self.board)
                                eng_aux = self.engine.go(movetime = self.engine_time)
                                self.eng.append((self.board.san(eng_aux[0]), self.info_handler.info["depth"], self.info_handler.info["seldepth"]))
                                svg2png(bytestring = chess.svg.board(board = self.board, size = 400, lastmove = move, check = self.check_f(), flipped = self.inverted), write_to="{}/{}.png".format(folder, self.ply))
                                self.jogo.append((self.ply, self.san, self.info_handler.info["score"][1]))
                                self.ply += 1
                                pbar.update(1)
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
                self.vprint("Saving Graphs...")
                ply =  1
                z = np.zeros(len(self.num_scores))
                self.num_scores = np.array(self.num_scores)
                fig = plt.figure(figsize=(4.32, 2.88))
                ax = fig.add_subplot(111)
                ax.set_facecolor(self.gui_color)
                fig.patch.set_facecolor(self.gui_color) 
                for x in tqdm(self.gm_lst):
                        t = list(range(1, len(self.num_scores[:ply])+1, 1))
                        plt.plot(t, self.num_scores[:ply]/100, color='black', marker='o', markersize=2)
                        if abs(max(self.num_scores[:ply], key=abs))/100<300/100:
                                plt.ylim(-300/100, 300/100)
                        else:
                                plt.ylim(-500/100, 500/100)
                        plt.fill_between(t, self.num_scores[:ply]/100, 0, where=self.num_scores[:ply] >= z[:ply], facecolor='blue', interpolate=True)
                        plt.fill_between(t, self.num_scores[:ply]/100, 0, where=self.num_scores[:ply] <= z[:ply], facecolor='red', interpolate=True)
                        plt.xticks(np.arange(1, ply+1, 5) if ply>5 else np.arange(1, 5+1, 1))
                        plt.title("Position after {}, Eval: {}".format(self.gm_lst[ply-1][2], self.num_scores[ply-1]/100))
                        plt.savefig("{}/{}.png".format(folder, ply), facecolor=fig.get_facecolor(), edgecolor='none')
                        ply += 1
                return
        
        def f_lst_colors(self):
                prev = 0
                for x in self.num_scores:
                        r = int(x)-int(prev)
                        self.lst_colors.append(r)
                        prev = int(x)
                self.vprint("\nLST_COLORS:")
                self.vprint(self.lst_colors)
                return

        #temporariamente
        def color_spectrum(self, r, i):
                if i%2==0:
                        if r > -30:
                                c = "blue"
                        else:
                                c = "red"
                else:
                        if r > 30:
                                c = "red"
                        else:
                                c = "blue"
                return c

        def delete_files(self, path_list = ["Moves", "Graphs"]):
                self.vprint("\nDeleting previous files...\n")
                for path in tqdm(path_list):
                        fileList = os.listdir(path)
                        for fileName in fileList:
                                if fileName != ".gitkeep":
                                        os.remove(path + '/' + fileName)
                return
        
        def vprint(self, text):
                if self.print:
                        print(text)

def parser():
        parser = argparse.ArgumentParser(description='Local Chess Graphical Evaluation')
        parser.add_argument('p', metavar='pgn', help='PGN File to be analyzed')
        parser.add_argument('-iv', dest='Inverted', action='store_true', help = 'Inverted board')
        parser.add_argument('-et', metavar='engine time', type = int, default = 2000, help='Engine evaluation time in milisseconds per move')
        parser.add_argument('--verbose', dest = "print" , action = 'store_true', help="Print analysis to terminal")
        parser.set_defaults(Inverted = False, print = False)

        args = parser.parse_args() 

        if args.print == True:
                print(args)
        return args