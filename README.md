Minesweeper Game Application
==========================

A Python implementation of the classic Minesweeper game.

##### Table of Contents
[Installation](#Installation)

[Running the Application](#RunningtheApplication)

[Gameplay](#Gameplay)

# Installation
To install the application, follow these steps:

1. Clone the repository using Git:
```bash
git clone https://github.com/your-repo-url/minesweeper.git
```

2. Navigate to the project directory:
```bash
  cd minesweeper
```
Install the required dependencies using pip:
``` bash
pip install -r requirements.txt
```
Pillow

# Running the Application
-------------------------

To run the application, execute the following command:
```bash
python main.py
```
This will launch the Minesweeper game window.

# Gameplay
The game starts with a grid of hidden cells, some of which contain mines.
Click on a cell to reveal its contents. If it's a mine, the game is over.
If the clicked cell is empty, all adjacent empty cells will be recursively revealed.
Right-click on a cell to flag it as a potential mine.
The game ends when all non-mine cells are revealed or a mine is clicked.

Note: This implementation uses a simple random number generator to place mines on the grid. 
The difficulty level can be adjusted by modifying the Minesweeper class in minesweeper.py.
