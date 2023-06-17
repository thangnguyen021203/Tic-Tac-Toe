import random
import numpy as np
import enum
class TicTacToe:
    def __init__(self):
        self.board = np.array([['-','-','-'],
                               ['-','-','-'],
                               ['-','-','-']], dtype= np.str0)
        self.position_available = [0,1,2,3,4,5,6,7,8]
        self.position_chosen = None
        print("There are positions that you will choose to put in:")
        print(np.array([['0','1','2'],
                        ['3','4','5'],
                        ['6','7','8']], dtype= np.str0))
                
    def show(self):
        print(self.board)
    
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
    
    def is_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    return False
        return True
    
    def is_over(self, human, computer):
        if self.is_winner(computer) or self.is_winner(human) or self.is_draw():
            return True
        return False
    
    def Game_Result(self, computer):
        if self.is_winner(computer):
            return 1
        if self.is_draw():
            return 0
        return -1
    
    def minimax(self, human, computer, is_computer):
        #if game is over
        if self.is_over(human, computer):
            return self.Game_Result(computer)

        if is_computer:
            best_Value = -np.Infinity
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = computer
                        value = self.minimax(human, computer, False)
                        self.board[i][j] = '-'
                        if best_Value < value:     
                            best_Value = value
            return best_Value
        else:
            best_Value = np.Infinity
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = human
                        value = self.minimax(human, computer, True)
                        if best_Value > value:     
                            best_Value = value
                        self.board[i][j] = '-'
            return best_Value
    
    def Best_Move(self, human, computer):
        best_Score = -np.Infinity
        best_move = None
        for i in range (3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.board[i][j] = computer
                    score = self.minimax(human,computer,False)
                    self.board[i][j] = '-'
                    if best_Score < score:
                        best_Score = score
                        best_move = i*3+j
        return best_move
    
    def play(self):
        human = input("Choose your chess X/O: ")
        computer = 'X' if human == 'O' else 'O'
        print("Your turn first")
        self.show()
        while True:
            #human
            human_turn = int(input("Your turn: "))
            while self.board[human_turn//3][human_turn%3] != '-':
                human_turn=int(input("This spot has filled yet. Please input another position: "))
            self.board[human_turn//3][human_turn%3] = human
            self.show()
            
            if self.is_over(human, computer):
                if self.is_winner(human):
                    print("Human with chess {} win!".format(human))
                    break
                if self.is_winner(computer):
                    print("Computer with chess {} win!".format(computer))
                    break
                else:
                    print("Tie Game!!!")
                    break
            
            #computer
            print("Computer turn: ")
            computer_turn = self.Best_Move(human,computer)
            self.board[computer_turn//3][computer_turn%3] = computer
            self.show()
            
            if self.is_over(human, computer):
                if self.is_winner(human):
                    print("Human with chess {} win!".format(human))
                    break
                if self.is_winner(computer):
                    print("Computer with chess {} win!".format(computer))
                    break
                else:
                    print("Tie Game!!!")
                    break
                
board_game = TicTacToe()
board_game.play()