from random import sample
from tkinter import *
from tkinter import Tk, simpledialog
from threading import Thread
from time import sleep as nap

class sudoku:
    '''This class is resposible for creating and solving the grid '''

    def __init__(self):
        # sudoku_genrator for question and solve fot the solutions by backing track
        self.side = 9
        self.side_small = int(self.side / 3)
        # self.grid = self.sudoku_genrator(elements=80) # all the funtions sre using the grid to return 
        self.grid = self.sudoku_genrator()  # all the funtions sre using the grid to return
        self.question = [a[:] for a in self.grid[:]]

    @staticmethod
    def sudoku_genrator(elements=30, side=9):
        # elements = 30 will be quite easy

        # errors
        if side % 3 != 0 or not side: raise Exception(f"'side' should be multiple of 3 and cannot be zero.")
        if elements > side ** 2: raise ValueError(
            f"Elements can not more then total elements in grid here we have {side ** 2} update 'side' for bigger grid.")

        base = int(side ** 0.5)
        # randomize rows, columns and numbers (of valid base pattern)
        shuffle = lambda s: sample(s, len(s))
        rBase = range(base) # (0,3)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)] # rows random [0,8]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)] # cols random [0,8]
        nums = shuffle(range(1, base * base + 1)) # random [1,9]

        # pattern for a baseline valid solution
        pattern = lambda r, c: (base * (r % base) + r // base + c) % side
        # produce board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # you must leave at least 17 numbers for a 9x9 sudoku for unique solution
        # remove 60 from the self.grid just a random nums 
        for p in sample(range(side ** 2), 81 - elements):
            board[p // side][p % side] = 0
        return board

    def possible(self, row, col, num):
        for cols in range(self.side):  # to range in the row length
            # Checks for number (n) in X columns
            if self.grid[row][cols] == num and col != cols:
                return False

        # reading each cell 
        for rows in self.grid:
            # Checks for number (n) in Y columns
            if rows[col] == num and row != rows:
                return False

        # for the box 
        row_range = row // self.side_small * self.side_small
        col_range = col // self.side_small * self.side_small
        for row in range(row_range, row_range + self.side_small):
            for col in range(col_range, col_range + self.side_small):
                # Checks for numbers in box(no matter the position, it finds the corner)
                if self.grid[row][col] == num:
                    return False

        return True

    def find_empty(self):
        for row in range(self.side):
            for cell in range(self.side):
                # get the each cell
                if self.grid[row][cell] == 0:
                    return (True, row, cell)
        else:
            return (False, -1, -1)

    def update_cell(self, row, col, val):
        '''Take index of the row and col and value to update useful in inheretance'''
        self.grid[row][col] = val

    def solve(self): # backing track
        is_empty, row, col = self.find_empty()
        if not is_empty: return True  # task completd
        for n in range(1, self.side + 1):
            # check all the possible value for that perticular possition
            if self.possible(row, col, n):
                # self.grid[row][col] = n
                self.update_cell(row, col, n)
                nap(0.2)
                if self.solve(): return True
                # this mean having error due to this value so make it 0 again and try with another value
                # self.grid[row][col] = 0
                self.update_cell(row, col, 0)
        return False





#######################################

class GUI(sudoku):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title('Sudoku AI')
        self.width, self.height = 455, 600
        self.head_bg = "#7f8c8d"
        self.root.geometry(f"{self.width}x{self.height}")
        self.minutes, self.seconds = 0, 0  # time
        self.moving_height = 0
        self.wrong_red = "#ffa59e"
        self.right_blue = "#bdebff"
        self.selected_yellow = "#ddffc2"
        # for users use self.question grid
        self.default_indexes = []
        for row in range(self.side):
            for col in range(self.side):
                if self.question[row][col]:
                    self.default_indexes.append([row, col])

        # head
        self.head(self.root)

        # clock in thread 😎.
        self.time_thread = Thread(target=lambda: self.clock(), daemon=True)
        self.time_thread.start()

        # board
        self.board_grid(self.root)

        # bottom_btns
        self.bottom(self.root)

    def head(self, master):
        self.moving_height += 60

        self.head_top = Label(master, bg=self.head_bg)
        self.head_top.place(height=self.moving_height, width=self.width)

        # clock - time update every second 
        self.time_value = Label(self.head_top, font=('arial', 30, 'bold'), padx=10, bg=self.head_bg, fg='white',
                                text=f"{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}")
        self.time_value.pack(side=RIGHT)

        self.Game_name = Label(self.head_top, font=('arial', 30, 'italic', UNDERLINE), padx=10, bg=self.head_bg,
                               fg='#81fcae', text=f"Sudoku AI")
        self.Game_name.pack(side=LEFT)

    def clock(self):
        # we need to make how much time is passed so -> every sec add 1 in clock and divide it by 60       
        while True:
            # update every second # update the value here till the window exits it will run
            nap(1)
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
            if self.minutes == 60: self.minutes, self.seconds = 0, 0  # reset the clock afer one hours

            time = f"{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}"
            self.time_value['text'] = time

    def board_grid(self, master):
        # use to render the grid and let user enter values
        # take 455 X 455 width and height +10 for border and all 
        self.canvas = Label(master, bg='#95a5a6')
        self.canvas.place(y=self.moving_height, width=self.width, height=self.width + 8)
        self.moving_height += self.width + 8
        # creating grid
        for row in range(9):
            for col in range(9):
                tile_num = f"{row}{col}"
                default = self.question[row][col]
                text_value = "  " if default == 0 else str(default)
                btn = Label(master=self.canvas, name=str(tile_num),
                            font=('arial', 21, 'bold'), text=text_value,
                            borderwidth=1, highlightthickness=5,
                            bg="white", relief="solid")
                btn.grid(row=row, column=col, ipadx=10, ipady=2, sticky=N + S + E + W)

        self.grid_ele = self.canvas.winfo_children()

    def check_possible(self, row, col, num):
        num = int(num)
        # row != rows and  col != cols because we dont want to compare element from it self 
        if num == 0: return False
        # default nums
        if [row, col] in self.default_indexes: return False
        # row
        for cols in range(self.side):  # to range in the row length
            if self.question[row][cols] == num and col != cols: return False

        # reading each cell 
        # for rows in self.question: 
        for rows in range(self.side):
            if self.question[rows][col] == num and row != rows: return False

        # for the box 
        row_range = row // self.side_small * self.side_small
        col_range = col // self.side_small * self.side_small
        for rows in range(row_range, row_range + self.side_small):
            for cols in range(col_range, col_range + self.side_small):
                if self.question[rows][cols] == num and rows != row and cols != col:
                    return False
        return True

    def bottom(self, master):
        # this cointain 2 buttons new game - AI solve it
        bottom = Label(master, bg=self.head_bg)
        bottom.place(y=self.moving_height, height=self.height - self.moving_height, width=self.width)

        self.new_gird = Button(bottom, font=('arial', 20, 'bold'), padx=10, relief=GROOVE, text="New Board",
                               command=self.new_setup)
        self.new_gird.place(x=10, y=10)
        self.AI_btn = Button(bottom, font=('arial', 20, 'bold'), padx=10, relief=GROOVE, text="AI solution",
                             command=self.Ai_solve)
        self.AI_btn.place(x=250, y=10)

    def Ai_solve(self):
        # for visual effects
        self.new_gird["state"] = "disabled"
        self.AI_btn["state"] = "disabled"
        self.solve()
        self.new_gird["state"] = "normal"
        self.AI_btn["state"] = "normal"

    def update_cell(self, row, col, val):
        # redefine funtion for animation in grid
        '''Take index of the row and col and value to update useful in inheretance'''
        name = f"{row}{col}"
        # nap(0.1) # for animation but tkinter is not so great for this use also lag some time
        for i in self.grid_ele:
            if name == str(i).rsplit('.', 1)[1]:
                self.grid[row][col] = val
                if val:
                    i['bg'] = '#81fcae'
                else:
                    i['bg'] = 'white'
                    val = " "
                i['text'] = val
                i.update()
                return

    def new_setup(self):
        # remove board
        self.canvas.pack_forget()

        self.grid = self.sudoku_genrator()
        self.question = [a[:] for a in self.grid[:]]
        self.moving_height = 60
        self.default_indexes = []
        for row in range(self.side):
            for col in range(self.side):
                if self.question[row][col]:
                    self.default_indexes.append([row, col])

        # board
        self.board_grid(self.root)

    @classmethod
    def runner(cls):
        # runner for the gui
        root = Tk()
        gui = cls(root)
        root.mainloop()


if __name__ == "__main__":
    GUI.runner()

