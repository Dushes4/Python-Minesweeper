from tkinter import *
from tkinter.font import *
from random import randint


class MenuWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.geometry("300x240")
        self.root.resizable(width=False, height=False)

        self.difficulty_label = self.create_difficulty_label(0, 0, "ВЫБЕРИТЕ СЛОЖНОСТЬ")
        self.easy_button = self.create_difficulty_button(0, 50, lambda: self.choose_difficulty(10, 10, 10), "Легкий (10 мин)")
        self.medium_button = self.create_difficulty_button(0, 110, lambda: self.choose_difficulty(15, 15, 30), "Средний (30 мин)")
        self.hard_button = self.create_difficulty_button(0, 170, lambda: self.choose_difficulty(30, 20, 100), "Сложный (100 мин)")

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
        self.header_size = 50
        self.cell_size = 30
        self.mines = mines

        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.geometry(f"{self.x_cells * self.cell_size + 1}x{y_cells * self.cell_size + self.header_size}")
        self.root.resizable(width=False, height=False)


if __name__ == '__main__':
    menu_window = MenuWindow()
    menu_window.root.mainloop()
