from tkinter import Tk, Label, Button, Canvas
from tkinter.font import Font
from random import randint


class MenuWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.geometry("300x240")
        self.root.resizable(width=False, height=False)

        self.difficulty_label = self.create_difficulty_label(0, 0, "ВЫБЕРИТЕ СЛОЖНОСТЬ")
        self.easy_button = self.create_difficulty_button(0, 50, lambda: self.choose_difficulty(10, 10, 10),
                                                         "Легкий (10 мин)")
        self.medium_button = self.create_difficulty_button(0, 110, lambda: self.choose_difficulty(15, 15, 30),
                                                           "Средний (30 мин)")
        self.hard_button = self.create_difficulty_button(0, 170, lambda: self.choose_difficulty(30, 20, 100),
                                                         "Сложный (100 мин)")

    def create_difficulty_label(self, x, y, text):
        label = Label(self.root)
        font = Font(family='Calibre', size=15, weight="bold")
        label["font"] = font
        label["justify"] = "center"
        label["text"] = text
        label.place(x=x, y=y, width=300, height=50)
        return label

    def create_difficulty_button(self, x, y, command, text):
        button = Button(self.root)
        font = Font(family='Calibre', size=10, weight="bold")
        button["font"] = font
        button["fg"] = "#000000"
        button["justify"] = "center"
        button["text"] = text
        button.place(x=10, y=y, width=280, height=50)
        button["command"] = command
        return button

    def choose_difficulty(self, x_cells, y_cells, mines):
        self.root.destroy()
        game_window = GameWindow(x_cells, y_cells, mines)
        game_window.root.mainloop()


class GameWindow:
    def __init__(self, x_cells, y_cells, mines):    
        self.x_cells = x_cells
        self.y_cells = y_cells
        self.number_color = ['#', 'darkblue', 'green', 'red', 'red', 'red', 'red', 'red', 'red', 'red']
        self.header_size = 50
        self.cell_size = 30
        self.mines = mines
        
        self.grid = None
        self.generated = False
        
        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.geometry(f"{self.x_cells * self.cell_size + 1}x{self.y_cells * self.cell_size + self.header_size}")
        self.root.resizable(width=False, height=False)

        self.canvas = self.create_canvas()
        self.info_flag = self.create_info_flag(5, 3, 38)
        self.info_label = self.create_info_label(50, 2, str(self.mines))

    def create_canvas(self):
        canvas = Canvas(self.root, width=self.x_cells * self.cell_size, height=self.y_cells * self.cell_size,
                        bg='white')
        canvas.place(x=0, y=self.header_size)
        canvas.bind("<Button-1>", self.click_grid)
        k = self.cell_size
        for i in range(self.x_cells):
            for j in range(self.y_cells):
                canvas.create_polygon(i * k + k, j * k + k, i * k + k, j * k, i * k, j * k + k, fill='grey')
                canvas.create_rectangle(i * k + 3, j * k + 3, i * k + k - 3, j * k + k - 3, fill='silver', width=0)
        return canvas

    def create_info_flag(self, x, y, size):
        canvas = Canvas(self.root, width=size, height=size)
        canvas.place(x=x, y=y)
        canvas.create_rectangle(x + size * 0.17, y + size * 0.02, x + size * 0.27, y + size * 0.98, fill='black',
                                width=0)
        canvas.create_polygon(x + size * 0.27, y + size * 0.02, x + size * 0.81, y + size * 0.27, x + size * 0.27,
                              y + size * 0.52, fill='red')
        return canvas

    def create_info_label(self, x, y, text):
        label = Label(self.root)
        font = Font(family='Calibre', size=30, weight="bold")
        label["font"] = font
        label["justify"] = "center"
        label["text"] = text
        label.place(x=x, y=y, height=50)
        return label

    def get_clicked_cell(self, x, y):
        return (x - 1) // self.cell_size, (y - 1) // self.cell_size

    def click_grid(self, event):
        x_cell, y_cell = self.get_clicked_cell(event.x, event.y)

        if not self.generated:
            self.grid = Grid(self.x_cells, self.y_cells, self.mines, x_cell, y_cell)
            self.generated = True

        if not self.grid[(x_cell, y_cell)].is_opened:
            self.open_cell(x_cell, y_cell)

    def open_cell(self, x_cell, y_cell, reveal=False):
        number = self.grid[(x_cell, y_cell)].number
        k = self.cell_size
        if not reveal:
            self.canvas.create_rectangle(x_cell * k + 1, y_cell * k + 1, x_cell * k + k - 1, y_cell * k + k - 1,
                                         fill='silver', outline='grey', width=1)

            if self.grid[(x_cell, y_cell)].is_mine:
                self.canvas.create_oval(x_cell * k + 5, y_cell * k + 5, x_cell * k + k - 5, y_cell * k + k - 5,
                                        fill='black', outline='black')

            elif number != 0:
                self.canvas.create_text(x_cell * k + k / 2, y_cell * k + k / 2, text=number,
                                        fill=self.number_color[number],
                                        font=f"Calibri {k - 6} bold")


class Cell:
    def __init__(self, is_mine=False, is_opened=False, is_marked=False):
        self.number = 0
        self.is_mine = is_mine
        self.is_opened = is_opened
        self.is_marked = is_marked

    def __repr__(self):
        if self.is_mine:
            return "o"
        elif self.number != 0:
            return str(self.number)
        else:
            return "."


class Grid:
    def __init__(self, x_cells, y_cells, mines, x_cell, y_cell):
        self.grid = [[Cell() for i in range(y_cells)] for j in range(x_cells)]
        self.x_cells = x_cells
        self.y_cells = y_cells
        self.generate_mines(x_cell, y_cell, mines)
        self.generate_numbers()
        print(self, end="\n\n")

    def __getitem__(self, tup):
        x, y = tup
        return self.grid[x][y]

    def __str__(self):
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.grid])

    def generate_mines(self, x_cell, y_cell, mines):
        mines_coords = []
        while len(mines_coords) != mines:
            r = (randint(0, self.x_cells - 1), randint(0, self.y_cells - 1))
            if r != (x_cell, y_cell) and r not in mines_coords:
                mines_coords.append(r)
        for mine in mines_coords:
            self[mine].is_mine = True

    def generate_numbers(self):
        for x in range(self.x_cells):
            for y in range(self.y_cells):
                self[(x, y)].number = 0
                for coords in self.get_nearby_cells_coords(x, y):
                    self[(x, y)].number += int(self[coords].is_mine)

    def get_nearby_cells_coords(self, x_cell, y_cell):
        nearby_coords = []
        if x_cell >= 1 and y_cell >= 1:
            nearby_coords.append((x_cell - 1, y_cell - 1))
        if x_cell >= 1:
            nearby_coords.append((x_cell - 1, y_cell))
        if y_cell >= 1:
            nearby_coords.append((x_cell, y_cell - 1))
        if x_cell < self.x_cells - 1:
            nearby_coords.append((x_cell + 1, y_cell))
        if y_cell < self.y_cells - 1:
            nearby_coords.append((x_cell, y_cell + 1))
        if x_cell < self.x_cells - 1 and y_cell < self.y_cells - 1:
            nearby_coords.append((x_cell + 1, y_cell + 1))
        if x_cell >= 1 and y_cell < self.y_cells - 1:
            nearby_coords.append((x_cell - 1, y_cell + 1))
        if x_cell < self.x_cells - 1 and y_cell >= 1:
            nearby_coords.append((x_cell + 1, y_cell - 1))
        return nearby_coords


if __name__ == '__main__':
    menu_window = MenuWindow()
    menu_window.root.mainloop()
