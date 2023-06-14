import numpy as np
import random
import os

class TicTacToe:
    def __init__(self):
        self.board = None
        self.current_state = None
        self.c_learning_rate = 0.1
        self.c_discount_value = 0.9
        self.exploration_rate =  0.3
        self.computer = None
        self.computer_q_table = None
        self.max_position_to_choose = None
        self.max_q_value_to_choose = None
        self.q_table_player_O = None
        self.q_table_player_X = None
        self.previous_action = None
        self.previous_q_value = None
        self.previous_state = None
        self.reward_X = 0
        self.reward_O = 0
        self.c_episodes = 1000000

    def save_file(self):
        np.save("q_table_player_O.npy", self.q_table_player_O)
        np.save("q_table_player_X.npy", self.q_table_player_X)
    
    def load_file(self):
        self.q_table_player_X = np.load("q_table_player_X.npy", allow_pickle= True)
        self.q_table_player_O = np.load("q_table_player_O.npy", allow_pickle= True)
    
    def have_file(self):
        if os.path.exists("./q_table_player_X") and os.path.exists("./q_table_player_O"):
            return True
        return False
    
    def update_exploration_rate(self):
        if self.exploration_rate > 0.3:
            self.exploration_rate *= 0.9
    
    def make_environment(self):
        self.board = np.array([['-','-','-'],
                              ['-','-','-'],
                              ['-','-','-']], dtype = np.str0)
        self.current_state = 19682 #Theo công thức convert, đây là trạng thái bảng rỗng
        
        if  not self.have_file():
            self.q_table_player_X = np.random.uniform(low = 0, high = 1, size = [3**9,9])
            self.q_table_player_O = np.random.uniform(low = 0, high = 1, size = [3**9,9])
        else:
            self.load_file()
        
        
    def convert_to_state(self):
        num = 0
        multiplier = 1
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 'X':
                    num += 0 * multiplier
                elif self.board[i, j] == 'O':
                    num += 1 * multiplier
                else:  # Trường hợp ô trống
                    num += 2 * multiplier
                multiplier *= 3
        return num
        
    
    def reset(self):
        self.board = np.array([['-','-','-'],
                              ['-','-','-'],
                              ['-','-','-']], dtype = np.str0)
        self.current_state = self.convert_to_state() #Trạng thái bảng rỗng
        self.previous_action = None
        self.previous_q_value = None
        self.previous_state = None
        self.reward_O = 0
        self.reward_X = 0
        self.q_table_player_O = None
        self.q_table_player_X = None
        
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
        draw = True
        for i in range(3):
            for j in (range(3)):
                if self.board[i][j] == '-':
                    draw = False
        return draw
    
    def get_reward_player_X(self):
        if self.is_winner('X'):
            self.reward_X = 1
            self.reward_O = -1
        else:
            self.reward_X = 0
            self.reward_O = 0
    
    def get_reward_player_O(self):
        if self.is_winner('O'):
            self.reward_X = 1
            self.reward_O = -1
        else:
            self.reward_X = 0
            self.reward_O = 0
    
    def get_reward(self):
        self.get_reward_player_X()
        self.get_reward_player_O()
        
    def swap_player(self, player):
        return 'X' if player == 'O' else 'O'
    
    def chooseAction(self, current_state, q_table_player):
        for i in range(9):
            if self.board[i//3][i%3] == '-': 
                self.max_q_value_to_choose = q_table_player[current_state][i]
                self.max_position_to_choose = i
                break
        for i in range(9):
            if self.max_q_value_to_choose < q_table_player[current_state][i]:
                if self.board[i//3][i%3] == '-': 
                    self.max_q_value_to_choose = q_table_player[current_state][i]
                    self.max_position_to_choose = i
        return self.max_position_to_choose
        
    def play(self, player):
        
        random_value = random.random()
        action = None
        
        if random_value > self.exploration_rate:
            if player == 'O':
                action = self.chooseAction(self.current_state, self.q_table_player_O)
                current_q_value = self.q_table_player_O[self.current_state][action]
            else:
                action = self.chooseAction(self.current_state, self.q_table_player_X)  
                current_q_value = self.q_table_player_X[self.current_state][action]
        else:
            action = random.randint(0,8)
            while self.board[action//3][action%3] != '-':
                action = random.randint(0,8)
            if player == 'O':
                current_q_value = self.q_table_player_O[self.current_state][action]
            else:
                current_q_value = self.q_table_player_X[self.current_state][action]
        
        self.update_exploration_rate()
        self.board[action//3][action%3] = player
        next_q_state = self.convert_to_state()
        
        self.reward_X = 0
        self.reward_O = 0
        self.get_reward()
        if player == 'O':
            new_q_value = (1-self.c_learning_rate)*current_q_value + self.c_learning_rate*(self.reward_O + self.c_discount_value*np.max(self.q_table_player_O[next_q_state]))
            
            #if self.previous_action != None or self.previous_q_value != None or self.previous_state != None:
            if self.reward_O == 1:
                new_q_value = (1-self.c_learning_rate)*self.previous_q_value + self.c_learning_rate*(self.reward_X + self.c_discount_value*np.max(self.q_table_player_X[self.current_state]))
                self.q_table_player_X[self.previous_state][self.previous_action] = new_q_value
            
            
            self.q_table_player_O[self.current_state][action] = new_q_value
            self.previous_state = self.current_state
            self.current_state = next_q_state
        else:
            new_q_value = (1-self.c_learning_rate)*current_q_value + self.c_learning_rate*(self.reward_X + self.c_discount_value*np.max(self.q_table_player_X[next_q_state]))
            
            #if self.previous_action != None or self.previous_q_value != None or self.previous_state != None:
            if self.reward_X == 1:
                new_q_value = (1-self.c_learning_rate)*self.previous_q_value + self.c_learning_rate*(self.reward_O + self.c_discount_value*np.max(self.q_table_player_O[self.current_state]))
                self.q_table_player_O[self.previous_state][self.previous_action] = new_q_value
            
            self.q_table_player_X[self.current_state][action] = new_q_value
            self.previous_state = self.current_state
            self.current_state = next_q_state
            
            self.previous_q_value = current_q_value
            self.previous_action = action
            

    def train(self):
        player = 'X'
        episodes = self.c_episodes
        
        for ep in range(episodes):
            player = 'X'
            print("Eps = {}".format(ep))
            
            while True:
                self.play(player)
                if self.is_winner('X') or self.is_winner('O') or self.is_draw():
                    self.save_file()
                    self.reset()
                    self.load_file()
                    break
                player = self.swap_player(player)


    def play_vs_human(self):
        self.reset()
        self.load_file()
        human = input("Choose your turn X/O: ")
        if (human == 'X'):
            self.computer = 'O'
            self.computer_q_table = self.q_table_player_O
        else: 
            self.computer = 'X'
            self.computer_q_table = self.q_table_player_X
        
        turn  = human
        while True:
            if turn == human:
                action = int(input("Input position to fix the spot: "))
                while self.board[action//3][action%3] != '-':
                    print("The position has filled yet.")
                    action = int(input("Input position to fix the spot: "))
                self.board[action//3][action%3] = human
                self.current_state = self.convert_to_state()
            else:
                action = self.chooseAction(self.current_state, self.computer_q_table)
                self.board[action//3][action%3] = self.computer
                self.current_state = self.convert_to_state()
            
            print(self.board)
            if self.is_winner(human):
                print("Human win!")
                break
            if self.is_winner(self.computer):
                print("Computer win!")
                break
            if self.is_draw():
                print("Draw!!!")
                break
            turn = self.swap_player(turn)
        
boardgame = TicTacToe()
boardgame.make_environment()
#boardgame.train()
boardgame.play_vs_human()