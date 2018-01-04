import numpy as np
from function_helper import make_None_matrix,is_valid
from constraint import constraint
import random,copy

class solver:
    def __init__(self,dim):
        self.dim =dim
        self.degree = np.zeros([dim,dim])
        self.probability = np.zeros([dim,dim])+ 1.0
        ## 0 if only zero is possible , 1 if only one value is possible. 2 if both are possible
        self.possible_values = make_None_matrix(np.zeros([dim,dim]))
        self.known_board = make_None_matrix(np.zeros([dim,dim]))
        self.explored_board = np.zeros([dim,dim]) ## all explored nodes are 1 remaining zeros
        self.current_state = np.zeros([dim,dim])
        self.constraint_list = []
        self.safe_cells = []
        self.mines = []
        self.isVariable = np.zeros([dim,dim])

    def next_step(self,first_time = False):
        if first_time == True:
            a, b = random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)
        else:
            new_safe_cells = []
            for i in range(len(self.safe_cells)):
                if self.explored_board[self.safe_cells[i][0],self.safe_cells[i][1]] < 1 and self.safe_cells[i] not in new_safe_cells:
                    new_safe_cells.append(self.safe_cells[i])
            self.safe_cells = new_safe_cells
            if len(self.safe_cells) == 0:
                # make explored cells probability to 1.0 or high to make this function work properly
                min_prob = self.probability.min()
                min_indexs = zip(*np.where(self.probability == min_prob))
                max_degree = -1
                a = None
                b = None
                for i,j in min_indexs:
                    if self.degree[i,j] > max_degree and (i,j) not in self.mines:
                        max_degree = self.degree[i,j]
                        a,b = i,j
            #i,j = np.unravel_index(self.probability.argmin(), self.probability.shape)
            else:
                a = self.safe_cells[0][0]
                b = self.safe_cells[0][1]
                self.safe_cells = self.safe_cells[1:]
        self.explored_board[a,b] = 1
        self.probability[a,b] = 1.0
        return a,b

    def build_new_constraint(self,i,j,val):
        neighs = self.get_neighb(i,j)
        new_neighs = []
        for l,m in neighs:
            if self.known_board[l,m] == 1:
                val = val - self.current_state[l,m]
            else:
                new_neighs.append((l,m))

        for l,m in new_neighs:
            self.isVariable[l,m] = 1

        return constraint(var_list=new_neighs,val=val)

    def add_constraint(self,c):
        # check for inference
        infered_list = []
        for c_ in self.constraint_list:
            if set(c_.var_list).issubset(c.var_list):
                new_var_l = list(set(c.var_list) - set(c_.var_list))
                new_val = c.value - c_.value
                new_c = constraint(new_var_l,new_val)
                infered_list.append(new_c)
            elif set(c.var_list).issubset(c_.var_list):
                new_var_l = list(set(c_.var_list) - set(c.var_list))
                new_val = c_.value - c.value
                new_c = constraint(new_var_l, new_val)
                infered_list.append(new_c)
        self.constraint_list.append(c)
        self.constraint_list = self.constraint_list + infered_list

    def update_safety(self):
        for i,cons_ in enumerate(self.constraint_list):
            if len(cons_.var_list) == cons_.value:
                self.mines.append(cons_.var_list)
                ## remove these variables from other constraints
                for a,b in cons_.var_list:

                    self.update_known_board(a,b,1)
                    self.current_state[a,b] = 1
                    self.remove_variable_from_all_constrnts(a,b,1)
                    self.isVariable[a,b] = 0

                del self.constraint_list[i]
            if cons_.value == 0:
                self.safe_cells = self.safe_cells + cons_.var_list
                ## remove these variables from other constraints
                for a,b in cons_.var_list:
                    self.update_known_board(a, b, 1)
                    self.current_state[a,b] = 0
                    self.remove_variable_from_all_constrnts(a,b,0)
                    self.isVariable[a, b] = 0
        new_constr_list = []
        for cons_ in self.constraint_list:
            if len(cons_.var_list) > 0:
                new_constr_list.append(cons_)
        self.constraint_list = new_constr_list
    def remove_variable_from_all_constrnts(self,i,j,mine):
        for l in range(len(self.constraint_list)):
            self.constraint_list[l].delete(i,j)
            self.constraint_list[l].value = self.constraint_list[l].value - mine

    def update_probs(self,i,j,val):
        # if there is already a probability assigned we will overwrite it
        neighbs = self.get_neighb(i,j)
        if len(neighbs)>0:
            prob = val/len(neighbs)
        for i,j in neighbs:
            self.probability[i,j] = (prob+self.probability[i,j])/2

    def update_known_board(self,i,j,isknown):
        self.known_board[i,j] = isknown


    def get_neighb(self,i,j):
        neigh = []
        for l in [-1,0,1]:
            for m in [-1,0,1]:
                if is_valid(i+l,j+m,self.dim) and self.explored_board[i+l,j+m] != 1.0:
                    neigh.append((i+l,j+m))
        return neigh

    def update_degree(self):
        for i in range(self.dim):
            for j in range(self.dim):
                neighs = self.get_neighb(i,j)
                for l,m in neighs:
                    self.degree[i,j] += self.isVariable[l,m]
    def get_list_variables(self):
        l = []
        for i in self.dim:
            for j in self.dim:
                if self.isVariable[i,j] == 1:
                    l.append((i,j))


    def get_all_sols(self):
        l = self.get_sols(self.constraint_list)
        return l

    def get_sols(self,constrnt_list):
        # for var_list[0] = 0
        ## remove constrnt whose var_list is zero
        constrnt = constrnt_list[-1]
        sols = constrnt.get_all_sols()
        if len(constrnt_list) <= 1:
            return sols
        constrnt_list = constrnt_list[:-1]

        for a,b in constrnt.var_list:
            constrnt_list = self.remove_variable_from_constraints(constrnt_list,a,b)
        l = self.get_sols(constrnt_list)
        for i in range(l):
            l[i] += sols
        return l

    def remove_variable_from_constraints(self,constrnts,i,j):
        new_cons = copy(constrnts)
        for l in range(len(constrnts)):
            new_cons[l].delete(i,j)
        return new_cons