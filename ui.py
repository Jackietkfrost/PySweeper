import tkinter as tk
from utils import Timer
from PIL import Image, ImageTk

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
        self.timer = Timer()
        self.time_label = tk.Label(master=self.root, text="Time: 0.0", font=("Helvetica", 8))
        self.time_label.grid(row=0, column=0, columnspan=self.game.width,sticky="w")
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                button = tk.Button(self.root, text="", width=2, command=lambda x=x, y=y: self.click(x, y))
                button.grid(row=y+1, column=x, sticky="nsew")
                button.bind("<3>", lambda event, x=x, y=y: self.right_click(x, y))
                row.append(button)
            self.buttons.append(row)

    def update_timer(self):
        self.timer.update()
        time_str = "Time: {:.1f}".format(self.timer.get_time())
        self.time_label.config(text=time_str)
        self.timer_id = self.root.after(100, self.update_timer)  # store the ID

    def click(self, x, y):
        if self.game.revealed[y][x]:
            return
        self.game.revealed[y][x] = True
        if self.game.grid[y][x] == -1:
            bomb_image = ImageTk.PhotoImage(Image.open("assets/bomb.png"))
            # self.buttons[y][x].config(text="*", bg="red")
            self.buttons[y][x].config(image=bomb_image, bg="red" )
            self.buttons[y][x].image = bomb_image  # keep a reference to the image
            self.game.game_over = True
            self.root.after_cancel(self.timer_id)  # stop the timer
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
        elif self.game.check_win():
            self.root.after_cancel(self.timer_id)  # stop the timer
            self.root.title("You Win!")

    def right_click(self, x, y):
        if self.game.revealed[y][x]:
            return
        flag_image = ImageTk.PhotoImage(Image.open("assets/bomb-flag.png"))
        self.buttons[y][x].config(image=flag_image, bg="yellow")
        self.buttons[y][x].image = flag_image  # keep a reference to the image

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
        self.update_timer()
        self.root.mainloop()