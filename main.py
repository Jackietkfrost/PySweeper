from minesweeper import Minesweeper
from ui import UI

def main():
    game = Minesweeper()
    ui = UI(game)
    ui.run()

if __name__ == "__main__":
    main()