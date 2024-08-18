import math
import copy
from Movements import Movements
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from queue import PriorityQueue
from copy import deepcopy
from NodeH5H6H7H8H9 import Quixo
import random

symbol = 1
opponent = -1
class Heuristics_H6:
    #Esta heurística hace un movimiento mío y a partir de ese movimiento hace alguna heurística para mi oponente, de las mejores que tiene
    # mi openente checo mi línea máxima, es decir, de sus mejores tomo la mejor para mí
    #H6
    @staticmethod
    def heuristic_6(node, my_symbol, opponent):
        def max_lines(board, symbol):
            maximum = 0
            cont_0 = 0
            cont_1 = 0
            cont_2 = 0
            cont_3 = 0
            cont_4 = 0
            aux = 0
            for i in range(len(board)):
                if board[i][0] == symbol:
                    cont_0 += 1
                    aux += 1
                if board[i][1] == symbol:
                    cont_1 += 1
                    aux += 1
                if board[i][2] == symbol:
                    cont_2 += 1
                    aux += 1
                if board[i][3] == symbol:
                    cont_3 += 1
                    aux += 1
                if board[i][4] == symbol:
                    cont_4 += 1
                    aux += 1

                maximum = max(maximum, aux)
                aux = 0

            maximum = max(maximum, cont_0, cont_1, cont_2, cont_3, cont_4)

            aux_2 = 0

            for i in range(len(board)):
                if board[i][i] == symbol:
                    aux += 1
                if board[i][4-i] == symbol:
                    aux_2 += 1
            
            maximum = max(maximum, aux, aux_2)
            return maximum
        
        #Si al yo hacer un movimiento ya le formo los 5, ya no tiene caso que haga lo demás de abajo
        if max_lines(node.board, opponent) == 5:
            return (-math.inf, 0)
        #Ahora bien, también puede ser que yo al hacer un movimiento ya haya formado mis 5 entonces no tiene caso hacer lo demás
        #Importa mucho el orden de las condiciones ya que si a él le formo 5 ya no tiene chiste preguntar esto ni aunque junte 5 (por lo que dijo el profe)
        if max_lines(node.board, my_symbol) == 5: #OOOOOOOOOOOOOOJJJJJJJJJJJJJJOOOOOOOOOOOO
            return (math.inf, 0)
        
        pq_h = PriorityQueue()
        pq_2h = PriorityQueue()

        movement_44 = ['00D', '00R',
                        '10U', '10D', '10R',
                        '20U', '20D', '20R',
                        '30U', '30D', '30R',
                        '40U', '40R',

                        '01D', '01L', '01R',
                        '41U', '41L', '41R',

                        '02D', '02L', '02R',
                        '42U', '42L', '42R',

                        '03D', '03L', '03R',
                        '43U', '43L', '43R',

                        '04D', '04L',
                        '14U', '14D', '14L',
                        '24U', '24D', '24L',
                        '34U', '34D', '34L',
                        '44U', '44L']
            
        def obtain_and_delete_number(nums):
            if nums:
                n = random.choice(nums)
                nums.remove(n)
                return n
            else:
                return None
        
        nums = list(range(0, 44))

        for _ in range(len(movement_44)):
            i = obtain_and_delete_number(nums)
            if node.board[int(movement_44[i][0])][int(movement_44[i][1])] == 0 or node.board[int(movement_44[i][0])][int(movement_44[i][1])] == opponent:
                obj = Movements(deepcopy(node.board))
                new_board = obj.moves(movement_44[i], opponent)

                new_node = Quixo(new_board, opponent, my_symbol) #si te das cuenta aquí se pone al revés
                new_node.move = movement_44[i]
                new_node.heuristic_value = (max_lines(new_node.board, opponent), max_lines(new_node.board, my_symbol)) #(h, my_max)
                pq_h.put(new_node)
    
        #meter los nodos con los valores heurísticos más altos iguales
        # no nadamas voy a sacar el primero porque no estoy 100% seguro de que su heuristica vaya a tomar ese, por lo tanto saco los primeros iguales,
        # de esta forma ya existe más probabilidad de que acertemos a un movimiento de su heurística
        move = pq_h.get()
        x = move.heuristic_value[0]
        while not pq_h.empty() and move.heuristic_value[0] == x:
            #Es importante que primero vaya esta condición ya que si mi movimiento hace 5 míos y le formo 5 también, pierdo, por lo tanto,
            # primero checa si el tiene 5 y si no ya podemos pasar a la siguiente asegurandonos que no perderemos por formar 5 y 5
            if move.heuristic_value[0] == 5:
                tuple = (-math.inf, move.heuristic_value[1])
            elif move.heuristic_value[1] == 5:
                tuple = (math.inf, move.heuristic_value[1])
            else:
                tuple = (move.heuristic_value[1]-move.heuristic_value[0], move.heuristic_value[1])

            pq_2h.put(tuple)

            move = pq_h.get()
        
        #SEGÚN chatGPT Y copilot NO AFECTA LA SOBRECARGA DE OPERADORES A OTRAS 'pq'

        #No es necesario utilizar una tercera 'pq' porque si las optimalidades son iguales eso significa que mi máximo es el mismo
        # ya que el máximo del oponente siempre es el mismo entonces si son optimalidades iguales se restarían números iguales
        # 3 1 2 3 , 4 4 4 4
        tuple = pq_2h.get()

        return tuple


# Generate dummy training data
num_examples = 10000
X_train = []
y_train = []

for _ in range(num_examples):
    # Generate a random board configuration
    board = np.random.randint(-1, 2, size=(5, 5))  # 0 for empty, 1 for X, 2 for O

    # Create a Quixo instance with the board configuration
    node = Quixo(board, -1, 1)  # Assuming -1 is the opponent symbol and 1 is your symbol
    X_train.append(node)

    # Calculate the heuristic value for the board configuration
    heuristic_value = Heuristics_H6.heuristic_6(node, 1, -1)
    y_train.append(heuristic_value)
    
# Preprocess the data
X_train = np.array([node.board.flatten() for node in X_train])
y_train = np.array(y_train)
# Define the ANN 
model = Sequential([
    #Input
    Dense(64, activation='relu', input_shape=(25,)),
    #Hidden 
    Dense(32, activation='relu'),
    #output
    Dense(1)
])

# Compile the ANN
model.compile(optimizer='adam', loss='mean_squared_error')
# Train the ANN
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)
# Save the trained ANN model
model.save_weights('ann_model_weights.weights.h5')


class QuixoBotANN:
    def __init__(self):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.name = "ANN"
        self.symbol = None
        self.ann_model = self.load_ann_model()
        self.opponent = None
        self.moves = ['00D', '00R', '10U', '10D', '10R', '20U', '20D', '20R', '30U', '30D', '30R', '40U', '40R',
                      '01D', '01L', '01R', '41U', '41L', '41R', '02D', '02L', '02R', '42U', '42L', '42R',
                      '03D', '03L', '03R', '43U', '43L', '43R', '04D', '04L', '14U', '14D', '14L', '24U', '24D',
                      '24L', '34U', '34D', '34L', '44U', '44L']
        
    def play_turn(self, board):
        self.board = board
        best_move = self.best_move(self.board)
        print(best_move)
        if best_move:
            i = int(best_move[0])
            j = int(best_move[1])
            M1 = Movements(self.board)
            self.board = M1.moves(best_move, self.symbol)
        return self.board
    
    def reset(self, symbol):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.symbol = symbol
        self.opponent = -1 if symbol == 1 else 1
        
    
    def load_ann_model(self):
        # Load the pre-trained ANN model
        ann_model = Sequential()
        ann_model.add(Dense(64, input_dim=25, activation='relu'))
        ann_model.add(Dense(32, activation='relu'))
        ann_model.add(Dense(1, activation='linear'))
        ann_model.load_weights('ann_model_weights.weights.h5')
        #print()
        return ann_model
    
    def heuristic_ann(self, board):
        # Preprocess the board configuration into a format suitable for the ANN
        board_flat = [val for row in board for val in row]
        board_input = np.array(board_flat).reshape(1, -1)

        # Use the ANN model to predict the heuristic value
        heuristic_value = self.ann_model.predict(board_input)[0][0]

        return heuristic_value

    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if depth == 0:
            return self.heuristic_ann(board)
        
        if is_maximizing:
            best_score = -math.inf
            for move in self.moves:
                i = int(move[0])
                j = int(move[1])
            
                if board[i][j] == 0 or board[i][j] == self.symbol:
                    obj = Movements(copy.deepcopy(board))
                    new_board = obj.moves(move, self.symbol)
                    score = self.minimax(new_board, depth + 1, False, alpha, beta)
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        
        else:
            best_score = math.inf
            for move in self.moves:
                i = int(move[0])
                j = int(move[1])
            
                if board[i][j] == 0 or board[i][j] == self.opponent:
                    obj = Movements(copy.deepcopy(board))
                    new_board = obj.moves(move, self.opponent)
                    score = self.minimax(new_board, depth + 1, True, alpha, beta)
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score
          
    def best_move(self, board):
        best_score = -math.inf
        best_move = None
        for move in self.moves:
            i = int(move[0])
            j = int(move[1])
        
            if board[i][j] == 0 or board[i][j] == self.symbol:
                obj = Movements(copy.deepcopy(board))
                new_board = obj.moves(move, self.symbol)
                score = self.minimax(new_board, 0, False, -math.inf, math.inf)
                if score > best_score:
                    best_score = score
                    best_move = move
                    
        return best_move

    def check_winner(self, board,  symbol):
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(board)):
            if board[i][0] == symbol:
                cont_0 += 1
                aux += 1
            if board[i][1] == symbol:
                cont_1 += 1
                aux += 1
            if board[i][2] == symbol:
                cont_2 += 1
                aux += 1
            if board[i][3] == symbol:
                cont_3 += 1
                aux += 1
            if board[i][4] == symbol:
                cont_4 += 1
                aux += 1

            if aux == 5:
                print("Ganó el jugador con el símbolo: ", symbol)
                return True
            else:
                aux = 0

        if cont_0 == 5 or cont_1 == 5 or cont_2 == 5 or cont_3 == 5 or cont_4 == 5:
            print("Ganó el jugador con el símbolo: ", symbol)
            return True

        aux_2 = 0

        for i in range(len(board)):
            if board[i][i] == symbol:
                aux += 1
            if board[i][4-i] == symbol:
                aux_2 += 1
        if aux == 5 or aux_2 == 5:
            print("Ganó el jugador con el símbolo: ", symbol)
            return True
        
        return False

    def print_board(self):
        for i in range(5):
            print("-----------------------------")
            for j in range(5):
                print(self.board[i][j], end="  |  ")
            print()
        print("-----------------------------")
    
    def play(self):
        print("Welcome to Quixo!")
        self.print_board()

        while not self.check_winner(self.board, self.opponent) and not self.check_winner(self.board, self.symbol):
            
            self.play_turn(self.board)
            print("Computer's move:")
            self.print_board()

            if self.check_winner(self.board, self.symbol):
                print("You lose!")
                break
            
            mov = input("Insert your move like this 00D, the numbers are rows (0-4), columns (0-4), and the direction (Down 'D', Up 'U', Right 'R', Left 'L') \n")
            i = int(mov[0])
            j = int(mov[1])
            m = mov[2]
            
            if (self.board[i][j] == 0 or self.board[i][j] == self.opponent) and (not 1 <= i <= 3 or not 1 <= j <= 3):
                if (m == 'U' and i != 0) or (m == 'R' and j != 4) or (m == 'D' and i != 4) or (m == 'L' and j != 0):
                    M = Movements(self.board)
                    self.board = M.moves(mov, self.opponent)
                else:
                    print("Move not allowed")
                    continue
                self.print_board()

                if self.check_winner(self.board, self.opponent):
                    print("You win!")
                    break

            else:
                print("Move not allowed, try again")


game = QuixoBotANN()
game.reset(1)
game.play()