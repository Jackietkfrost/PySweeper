from tkinter import *
from tkinter import ttk
from utils import Timer
from PIL import Image, ImageTk
from styles import MinesweeperStyles

class UI:
    root = Tk()
    def __init__(self, game):
        """
        Initialize the UI with a given game.

        :param game: a Minesweeper game
        """
        self.game = game
        self.root.title("Minesweeper")
        self.styles = MinesweeperStyles()
        self.mainframe = ttk.Frame(self.root, width=2, height=8, padding="3 3 12 12", style="MS.TFrame" )
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.timer_id = None
        self.buttons = []
        self.timer = Timer()
        self.time_label = ttk.Label(master= self.mainframe, text="Time: 0", style="MS.TLabel")
        self.time_label.grid(row=0, column=0, columnspan=self.game.width,sticky="w")
        self.flags_remaining_label = ttk.Label(master=self.mainframe, text="Flags: {}".format(self.game.flags_remaining), style="MS.TLabel")
        self.flags_remaining_label.grid(row=0, column=self.game.width//2, columnspan=self.game.width//2, sticky="e")
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                button = ttk.Button(self.mainframe, text="", command=lambda x=x, y=y: self.click(x, y), style="MS.TButton")
                button.grid(row=y+1, column=x, sticky="nsew")
                button.bind("<3>", lambda event, x=x, y=y: self.right_click(x, y))
                row.append(button)
            self.buttons.append(row)

    def update_timer(self):
        """
        Update the timer label every second to display the current elapsed time.
        
        This method is called repeatedly by the after method to update the timer
        label. It stops once the game is over.
        """
        if self.timer_id is None:
            self.timer_id = self.root.after(1000, self.update_timer)  
        else:
            self.timer.update()
            time_str = "Time: {:.0f}".format(self.timer.get_time())
            self.time_label.config(text=time_str)
            self.timer_id = self.root.after(1000, self.update_timer)

    def click(self, x, y):
        if self.game.game_over or self.game.game_win:
            return
        if self.game.revealed[y][x]:
            return
        if self.timer_id is None:
            self.update_timer()
        self.game.revealed[y][x] = True
        if self.game.check_win():
            self.game_win()
            
        # If tile is bomb:
        if self.game.grid[y][x] == -1:
            bomb_image = ImageTk.PhotoImage(Image.open("assets/bomb.png"))
            self.buttons[y][x].config(image=bomb_image, style="MS_bomb.TButton")
            self.buttons[y][x].image = bomb_image
            self.game_over()

        # Get all bombs and show them, unless the bomb has been flagged.
            for i in range(self.game.height):
                for j in range(self.game.width):
                    if self.game.grid[i][j] == -1 and not self.game.revealed[i][j]:
                        if not hasattr(self.buttons[i][j], 'flagged'):
                            bomb_image = ImageTk.PhotoImage(Image.open("assets/bomb.png"))
                            self.buttons[i][j].config(image=bomb_image)
                            self.buttons[i][j].image = bomb_image
        # Else if tile is not a bomb, and is empty:
        elif self.game.grid[y][x] == 0:
            self.buttons[y][x].config(text="", state="disabled",  style="MS_pressed.TButton")
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x+dx < self.game.width and 0 <= y+dy < self.game.height:
                        self.click(x+dx, y+dy)
        # Else show the number of the tile:
        else:
            self.buttons[y][x].config(text=str(self.game.grid[y][x]), state="disabled", style="MS_pressed.TButton")

    def right_click(self, x, y):
        if self.game.revealed[y][x] or self.game.game_win or self.game.game_over:
            return
        if self.timer_id is None:
            self.update_timer() 
        if hasattr(self.buttons[y][x], 'flagged'):
            # Remove flag
            self.buttons[y][x].config(image="")
            del self.buttons[y][x].flagged
            self.game.flags_remaining += 1
        else:
            # Add flag
            flag_image = ImageTk.PhotoImage(Image.open("assets/bomb-flag.png"))
            if self.game.flags_remaining > 0:
                self.game.flags_remaining -= 1
                self.buttons[y][x].config(image=flag_image)
                self.buttons[y][x].image = flag_image  # keep a reference to the image
                self.buttons[y][x].flagged = True
            else:
                return
        self.flags_remaining_label.config(text="Flags: {}".format(self.game.flags_remaining))


    def game_over(self):
        self.root.after_cancel(self.timer_id)
        self.game.game_over = True
        self.root.title("Game Over!")

    def game_win(self):
        self.root.after_cancel(self.timer_id)
        self.game.game_win = True
        self.root.title("You Win!")
    def run(self):
        self.root.mainloop()