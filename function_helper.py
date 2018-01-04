import numpy as np
import random,math

def generateBoard(size,mines):
    """

    :param size: length of side a minesweeper
    :param prob: probability than a cell can be blocked
    :return: generated matrix representation of board
    """
    maze = np.zeros([size,size],dtype=int)
    for i in range(mines):
        while(1):
            l = random.randint(0,size-1)
            k = random.randint(0,size-1)
            if maze[l,k] !=1 :
                maze[l,k] = 1
                break
    return maze

def get_Information_Board(m):
    dim = len(m[0])
    m1 = np.zeros_like(m)
    for i in range(dim):
        for j in range(dim):
            m1[i,j] = get_info_at(m,i,j)
    return m1
def get_info_at(m,i,j):
    neigh_sum = 0
    dim = len(m[0])
    for l in [-1,0,1]:
        for k in [-1,0,1]:
            if is_valid(i+l,j+k,dim):
                neigh_sum += m[i+l,j+k]
    return neigh_sum

def is_valid(i,j,dim):
    if i < 0 or j <0:
        return False
    if i > dim-1 or j > dim -1:
        return False
    return True

def make_None_matrix(m):
    dim = len(m[0])
    for i in range(dim):
        for j in range(dim):
            m[i,j] = None
    return m


def uncover(m1,m2,i,j):
    assert is_valid(i,j,len(m1[0]))
    assert is_valid(i,j,len(m2[0]))
    m2[i,j] = m1[i,j]
    return m2

def mine_inspection(m,i,j):
    if m[i,j] == 1:
        return True
    return False