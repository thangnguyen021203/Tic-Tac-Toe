import random

class TicTacToe:
    def __init__(self):
        self.board = [['-' for i in range(3)] for j in range (3)]
        
    def show_board(self):
        for i in range(3):
            print(str(self.board[i][0]) + "\t" + str(self.board[i][1]) + "\t" + str(self.board[i][2]))
            print("")
    
    def is_winner(self, player):
        #Check row
        for i in range (3):
            win  = True
            for j in range (3):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return True
        
        #Check column
        for i in range(3):
            win = True
            for j in range (3):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return True

        #Check main diagonals
        win = True
        for i in range(3):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return True
    
        #Check sub diagonals
        win = True
        for i in range(3):
            if self.board[i][3-i-1] != player:
                win = False
                break
        if win:
            return True
        
        return False
    
    #check if draw
    def is_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    return False
        return True
    #Change the Turn 
    def swap_player(self, player):
        return 'X' if player == 'O' else 'O'
        
        
    #Play your turn
    def play(self, player):
        row, col = list(
                map(int, input("{} turn: ".format(player)).split()))
        if self.board[row][col] != '-':
            row,col = list(
                map(int, input("This place is fill, please input another row & column:  ".format(player)).split()))
    
        self.board[row][col] = player
    
    #Start the game:
    def start(self):
        print("First player is 'X' / Second player is 'O'")
        print("Input row and column to fix the spot.")
        player = 'X'
        self.show_board()
        
        while True:
            
            self.play(player)
            self.show_board()
            end_game = False
            end_game = self.is_winner(player)
            if end_game:
                print("Player {} win!".format(player))
                break
            end_game = self.is_draw()
            if end_game:
                print("DRAW GAME!")
                break
            player = self.swap_player(player)
            print("")
    
boardgame = TicTacToe()
boardgame.start()
    