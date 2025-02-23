from tkinter import *
from tkinter import ttk
from utils import Timer
from PIL import Image, ImageTk

class UI:
    root = Tk()
    def __init__(self, game):
        """
        Initialize the UI with a given game.

        :param game: a Minesweeper game
        """
        self.game = game

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        
        self.root.title("Minesweeper")
        self.buttons = []
        self.bg_color = "#999999"
        self.bg_color_selected = "#656565"
        self.bg_color_bomb = "red"
        self.timer = Timer()
        self.time_label = ttk.Label(master=self.root, text="Time: 0.0", font=("Helvetica", 8))
        self.time_label.grid(row=0, column=0, columnspan=self.game.width,sticky="w")
        self.mines_marked_label = ttk.Label(master=self.root, text="Flags: 0/{}".format(self.game.num_mines), font=("Helvetica", 8))
        self.mines_marked_label.grid(row=0, column=self.game.width//2, columnspan=self.game.width//2, sticky="e")
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                button = ttk.Button(self.root, text="", width=2, command=lambda x=x, y=y: self.click(x, y))
                button.grid(row=y+1, column=x, sticky="nsew")
                button.bind("<3>", lambda event, x=x, y=y: self.right_click(x, y))
                row.append(button)
            self.buttons.append(row)

    def update_timer(self):
        """
        Update the timer label every 100ms to display the current elapsed time.
        
        This method is called repeatedly by the after method to update the timer
        label. It stops once the game is over.
        """
        
        self.timer.update()
        time_str = "Time: {:.1f}".format(self.timer.get_time())
        self.time_label.config(text=time_str)
        self.timer_id = self.root.after(100, self.update_timer)  # store the ID

    def click(self, x, y):
        if self.game.game_over or self.game.game_win:
            return
        if self.game.revealed[y][x]:
            return
        self.game.revealed[y][x] = True
        # If tile is bomb:
        if self.game.grid[y][x] == -1:
            bomb_image = ImageTk.PhotoImage(Image.open("assets/bomb.png"))
            # self.buttons[y][x].config(text="*", bg="red")
            self.buttons[y][x].config(image=bomb_image)
            self.buttons[y][x].image = bomb_image  # keep a reference to the image
            self.game.game_over = True
            self.root.after_cancel(self.timer_id)  # stop the timer
        # Else if tile is not a bomb, and is empty:
        elif self.game.grid[y][x] == 0:
            self.buttons[y][x].config(text="")
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x+dx < self.game.width and 0 <= y+dy < self.game.height:
                        self.click(x+dx, y+dy)
        # Else show the number of the tile:
        else:
            self.buttons[y][x].config(text=str(self.game.grid[y][x]))
        
        if self.game.game_over:
            self.game_over()
        elif self.game.check_win():
            self.root.after_cancel(self.timer_id)  # stop the timer
            self.game_win()

    def right_click(self, x, y):
        if self.game.revealed[y][x]:
            return
        if hasattr(self.buttons[y][x], 'flagged'):
            # Remove flag
            self.buttons[y][x].config(image="")
            del self.buttons[y][x].flagged
        else:
            # Add flag
            flag_image = ImageTk.PhotoImage(Image.open("assets/bomb-flag.png"))
            self.buttons[y][x].config(image=flag_image, )
            self.buttons[y][x].image = flag_image  # keep a reference to the image
            self.buttons[y][x].flagged = True


    def game_over(self):
        self.root.title("Game Over!")

    def game_win(self):
        self.root.title("You Win!")
    def run(self):
        self.update_timer()
        self.root.mainloop()