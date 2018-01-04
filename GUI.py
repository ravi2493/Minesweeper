from tkinter import *
from tkinter import messagebox,simpledialog
from play import game
root = Tk()

images = {}
images['blank'] = PhotoImage(file="images/img_blank.gif")
images['mine'] = PhotoImage(file="images/img_mine.gif")
images['hit_mine'] = PhotoImage(file="images/img_hit_mine.gif")
images['flag'] = PhotoImage(file="images/img_flag.gif")
images['wrong'] = PhotoImage(file="images/img_wrong_mine.gif")
images['question'] = PhotoImage(file="images/img_question.gif")
for i in range(0, 9):
    images[str(i)] = PhotoImage(file = "images/img_"+str(i)+".gif")


row_size=9
col_size=9

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

def explore_cell(button,x,y,gm):
    """

    :param button:
    :return:
    """
    global grid_size,num_mines,root
    button.unbind('<Button-1>')
    # px,py = gm.get_next_step()
    answer = simpledialog.askinteger("Input", "Input Value for Position ({0},{1}) \n \n -1 if there is mine \n 0-8 if there is no mine \n".format(x,y),
                                     parent=root,
                                     minvalue=-1, maxvalue=8)
    if answer is not None:
        if answer >=0:
            button.config(image=images[str(answer)])
        elif answer == -1:
            button.config(image=images['hit_mine'])
    return answer

    # f.tkraise()

def create_frame2(row_size,col_size,gm):
    """

    :return:
    """
    for row in range(row_size):
        for col in range(col_size):
            img = None
            if gm.board[row][col]==0:
                img=images["blank"]
            else:
                img=images['mine']
            button = Button(f2, image=img)
            button.grid(row=row+2, column=col)
            # button.bind('<Button-1>', lambda event, id=button, x=row, y=col: explore_cell(id, x, y))

    # for row in range(row_size):
    #     for col in range(col_size):
    #         button = Button(f2, image=images['blank'])
    #         button.grid(row=row+1, column=col)

    label1 = Label(f2, text="Left: Generated Board | Right: Playing Board")
    label1.grid(row=0, column=col_size)

    label1 = Label(f2, text="Dimension {0}*{1} | Number of Mines {2}".format(row_size,row_size,gm.num_mines))
    label1.grid(row=1, column=col_size)

    button_list = []
    for row in range(row_size):
        temp_lis = []
        for col in range(col_size):
            button = Button(f2, image=images['question'])
            button.grid(row=row+2, column=col+col_size+4)
            button.bind('<Button-1>', lambda event, id=button, x=row, y=col: explore_cell(id, x, y,gm))
            temp_lis.append(button)
        button_list.append(temp_lis)
    while(1):
        px,py=gm.get_next_step()
        value = explore_cell(button_list[px][py],px,py,gm)
        if value >= 0:
            x = gm.run_algo(px, py, value)
            if x == 1:
                for row in range(row_size):
                    for col in range(col_size):
                        if gm.board[row][col] < 0:
                            button_list[row][col].config(image=images['mine'])
                messagebox.showinfo("solved", "solved")
                root.destroy()
        else:
            check = messagebox.showinfo("Game Over", "GameOver")
            root.destroy()
    # for button in button_list:
    #     for but in button:
    #         but.config(image=images['hit_mine'])

def checkInput():
    """

    :return:
    """
    print("asasaas")
    global grid_size,num_mines,row_size,col_size

    if grid_size.get():
        if num_mines.get():
            row_size = int(grid_size.get())
            col_size = int(grid_size.get())
            mine_size = int(num_mines.get())
            f2.tkraise()
            gm = game(row_size,mine_size)
            create_frame2(row_size,col_size,gm)
            return True
        else:
            num_mines.focus_set()
            return False
        return True
    else:
        grid_size.focus_set()
        return False


f1.tkraise()

label1 = Label(f1,text="MineSweeper")
label1.grid(row=0,column=1)
label1 = Label(f1,text="Enter the Board Size")
label1.grid(row=1)
grid_size = Entry(f1)
grid_size.grid(row=1,column=1)

label1 = Label(f1,text="Enter the Number of Mines")
label1.grid(row=2)
num_mines = Entry(f1)
num_mines.grid(row=2,column=1)



start_game = Button(f1,text='Play Game',command= lambda : checkInput())
start_game.grid(row=3,column=0)

root.mainloop()
