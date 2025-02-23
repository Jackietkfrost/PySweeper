import tkinter as tk

class UI:
    def __init__(self, game):
        """
        Initialize the UI with a given game.

        :param game: a Minesweeper game
        """
        self.game = game
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.buttons = []
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                button = tk.Button(self.root, text="", width=2, command=lambda x=x, y=y: self.click(x, y))
                button.grid(row=y, column=x)
                row.append(button)
            self.buttons.append(row)

    def click(self, x, y):
        if self.game.revealed[y][x]:
            return
        self.game.revealed[y][x] = True
        if self.game.grid[y][x] == -1:
            self.buttons[y][x].config(text="*", bg="red")
            self.game.game_over = True
        elif self.game.grid[y][x] == 0:
            self.buttons[y][x].config(text="", bg="gray")
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x+dx < self.game.width and 0 <= y+dy < self.game.height:
                        self.click(x+dx, y+dy)
        else:
            self.buttons[y][x].config(text=str(self.game.grid[y][x]), bg="gray")
        if self.game.game_over:
            self.root.title("Game Over!")

    def update_button(self, x, y):
        if self.game.revealed[y][x]:
            if self.game.grid[y][x] == -1:
                self.buttons[y][x].config(text="X", bg="red")
            else:
                self.buttons[y][x].config(text=str(self.game.grid[y][x]), bg="gray")
                if self.game.grid[y][x] == 0:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if 0 <= x+dx < self.game.width and 0 <= y+dy < self.game.height:
                                if not self.game.revealed[y+dy][x+dx]:
                                    self.game.revealed[y+dy][x+dx] = True
                                    self.update_button(x+dx, y+dy)
        else:
            self.buttons[y][x].config(text="", bg="SystemButtonFace")

    def game_over(self):
        self.root.title("Game Over!")

    def run(self):
        self.root.mainloop()