import numpy as np
import random
from function_helper import generateBoard,get_Information_Board,make_None_matrix,uncover
from function_helper import mine_inspection
from solver import solver

class game():
    def __init__(self,dm,num_mines):
        self.dim = dm
        self.num_mines = num_mines
        p = num_mines/(self.dim*self.dim)
        ## one for mine cell, zero for non-mine cell
        self.board = generateBoard(self.dim,mines=num_mines)
        info_board = get_Information_Board(self.board)

        ########## game ############

        self.game_state = make_None_matrix(np.zeros([self.dim,self.dim]))
        self.solvr = solver(self.dim)
        self.first_time = True

    def get_next_step(self):
        x, y = self.solvr.next_step(first_time=self.first_time)
        self.first_time = False
        return x,y

    def run_algo(self,x,y,num_mines):
        # x = input("enter row index:")
        # y = input("enter column index:")
        # if first_time == True:
        #     x,y = random.randint(0,dim-1),random.randint(0,dim-1)
        #     first_time = False
        # else:

        print("x and y ::"+str(x)+"\t"+str(y))
        # game_state = uncover(self.board,self.game_state,x,y)
        # if mine exists end the game
        # if mine_inspection(game_state,x,y):
        #     print("game ended\n")
        #     print("score \t"+str(self.dim*self.dim-np.count_nonzero(game_state)))
        #     return -1
        if num_mines == 0:
            print("conclusive moves!")
        # game_state[x,y] = 0
        self.solvr.update_known_board(x,y,isknown=0)
        self.solvr.current_state[x,y] = 0
        # print("known board updated")
        self.solvr.isVariable[x,y] = 0
        c = self.solvr.build_new_constraint(x,y,val=num_mines)
        self.solvr.add_constraint(c)
        # print("constraint added!")
        self.solvr.update_degree()
        # print("degree updated !")
        self.solvr.update_probs(x,y,val=num_mines)
        # print("probability updated !")
        self.solvr.update_safety()
        # print("safe cells updated")
        print("done")
        if np.array_equal(self.solvr.current_state,self.board):
            print("solved")
            return 1