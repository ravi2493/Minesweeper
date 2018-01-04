class constraint:
    value = None
    var_list = []
    def __init__(self,var_list,val):
        self.value = val
        self.var_list = var_list

    def delete(self,i,j):
        if (i,j) in self.var_list:
            self.var_list.remove((i,j))

    def get_all_sols(self):
        l = self.get_sols(self.var_list,self.value)
        return l

    def get_sols(self,var_list,val):
        # for var_list[0] = 0
        if len(var_list) == val:
            l = []
            for i in range(val):
                l.append(1)
            return [l]
        elif val == 0:
            l = []
            for i in range(len(var_list)):
                l.append(0)
            return [l]
        l1 = self.get_sols(var_list[:-1],val)
        for i in range(len(l1)):
            l1[i].append(0)
        # for var_list[1] = 1
        l2 = self.get_sols(var_list[:-1], val-1)
        for i in range(len(l2)):
            l2[i].append(1)
        return l1+l2

# c = constraint([(1,2),(2,3),(4,5)],2)
# print(c.get_all_sols())