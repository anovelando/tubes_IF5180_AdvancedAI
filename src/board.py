class Board(object):
    def __init__(self, size=10):
        self.size = size
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.board_static = [[" " for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * (self.size * 4 - 1))

    def init_board(self, player, listWumpus, gold):
        #display board
        self.board[player.x][player.y] = "P"
        for wumpus in listWumpus:
            self.board[wumpus.x][wumpus.y] = "W"
            self.add_stench(wumpus)
        self.board[gold.x][gold.y] = "G"

        #static board
        for wumpus in listWumpus:
            self.board_static[wumpus.x][wumpus.y] = "W"
            self.add_stench_static(wumpus)
        self.board_static[gold.x][gold.y] = "G"

    def add_stench(self, wumpus):
        if wumpus.x > 0 and self.board[wumpus.x-1][wumpus.y] == " ":
            self.board[wumpus.x-1][wumpus.y] = "~"
        if wumpus.x < self.size-1 and self.board[wumpus.x+1][wumpus.y] == " ":
            self.board[wumpus.x+1][wumpus.y] = "~"
        if wumpus.y > 0 and self.board[wumpus.x][wumpus.y-1] == " ":
            self.board[wumpus.x][wumpus.y-1] = "~"
        if wumpus.y < self.size-1 and self.board[wumpus.x][wumpus.y+1] == " ":
            self.board[wumpus.x][wumpus.y+1] = "~"

    def add_stench_static(self, wumpus):
        if wumpus.x > 0 and self.board_static[wumpus.x-1][wumpus.y] == " ":
            self.board_static[wumpus.x-1][wumpus.y] = "~"
        if wumpus.x < self.size-1 and self.board_static[wumpus.x+1][wumpus.y] == " ":
            self.board_static[wumpus.x+1][wumpus.y] = "~"
        if wumpus.y > 0 and self.board_static[wumpus.x][wumpus.y-1] == " ":
            self.board_static[wumpus.x][wumpus.y-1] = "~"
        if wumpus.y < self.size-1 and self.board_static[wumpus.x][wumpus.y+1] == " ":
            self.board_static[wumpus.x][wumpus.y+1] = "~"

    def update_board(self, x, y, symbol):
        self.board[x][y] = symbol