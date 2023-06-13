import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = None
        self.current_state = None
        c_learning_rate = 0.1
        c_discount_value = 0.9
        
    def make_environment(self):
        self.board = np.array([['-','-','-'],
                              ['-','-','-'],
                              ['-','-','-']], dtype = np.str0)
        self.q_table_player_X = np.random.uniform(low = 0, high = 2, size = [3**9,9])
        self.q_table_player_O = np.random.uniform(low = 0, high = 2, size = [3**9,9])
        self.current_state = 19682 #Theo công thức convert, đây là trạng thái bảng rỗng
        
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
        self.current_state = 19628 #Trạng thái bảng rỗng
    
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
        for i in self.board:
            if i != '-':
                draw = False
        return draw
    
    def get_reward_player_X(self):
        if self.is_winner('X'):
            return 1
        return 0
    
    def get_reward_player_O(self):
        if self.is_winner('O'):
            return 1
        return 0
    
    def get_reward(self, reward_X, reward_O):
        reward_X = self.get_reward_player_X()
        reward_Y = self.get_reward_player_O()
        
    def swap_player(self, player):
        return 'X' if player == 'O' else 'O'
    
    def play(self, player):
        if player == 'O':
            action = np.argmax(self.q_table_player_O[self.current_state])
            current_q_value = self.q_table_player_O[self.current_state][action]
        else:
            action = np.argmax(self.q_table_player_X[self.current_state])    
            current_q_value = self.q_table_player_X[self.current_state][action]
            
        self.board[action] = player
        next_q_state = self.convert_to_state()
        
        reward_X = 0
        reward_O = 0
        self.get_reward(reward_X,reward_O)
        if player == 'O':
            new_q_value = (1-self.c_learning_rate)*current_q_value + self.c_learning_rate*(reward_O + self.c_discount_value*np.max(self.q_table_player_O[next_q_state]))
            self.q_table_player_O[self.current_state] = new_q_value
            self.current_state = next_q_state
        else:
            new_q_value = (1-self.c_learning_rate)*current_q_value + self.c_learning_rate*(reward_X + self.c_discount_value*np.max(self.q_table_player_X[next_q_state]))
            self.q_table_player_X[self.current_state] = new_q_value
            self.current_state = next_q_state



boardgame = TicTacToe()
boardgame.make_environment()
print(boardgame.convert_to_state())
print(boardgame.board)