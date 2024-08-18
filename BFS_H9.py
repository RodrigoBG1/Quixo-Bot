from NodeH5H6H7H8H9 import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import math
import random

class Heuristics_H9:
    @staticmethod
    def heuristic_9(node, my_symbol, opponent):
        #En esta heurística saco mis líneas máximas iguales y de las mejores saco su optimalidad y ya escojo
        #Esta heurística mejora la 8 porque en la 8 saco la mejor optimalidad de todos pero puede haber casos así --> 4,3 3,1
        #Ahí tomaría la 3,1 cuando verdaderamente conviene la 4,3, la 'heuristica_9' resuelve este problema
        def max_lines(symbol):
            maximum = 0
            cont_0 = 0
            cont_1 = 0
            cont_2 = 0
            cont_3 = 0
            cont_4 = 0
            aux = 0
            for i in range(len(node.board)):
                if node.board[i][0] == symbol:
                    cont_0 += 1
                    aux += 1
                if node.board[i][1] == symbol:
                    cont_1 += 1
                    aux += 1
                if node.board[i][2] == symbol:
                    cont_2 += 1
                    aux += 1
                if node.board[i][3] == symbol:
                    cont_3 += 1
                    aux += 1
                if node.board[i][4] == symbol:
                    cont_4 += 1
                    aux += 1

                maximum = max(maximum, aux)
                aux = 0

            maximum = max(maximum, cont_0, cont_1, cont_2, cont_3, cont_4)

            aux_2 = 0

            for i in range(len(node.board)):
                if node.board[i][i] == symbol:
                    aux += 1
                if node.board[i][4-i] == symbol:
                    aux_2 += 1
            
            maximum = max(maximum, aux, aux_2)
            return maximum

        a = max_lines(my_symbol) #my
        b = max_lines(opponent) #opponent

        #Es importante que primero vaya esta condición ya que si mi movimiento hace 5 míos y le formo 5 también, pierdo, por lo tanto,
        # primero checa si el tiene 5 y si no ya podemos pasar a la siguiente asegurandonos que no perderemos por formar 5 y 5
        if b == 5:
            return (-math.inf, a)
        elif a == 5:
            return (math.inf, a)
        else:
            return (a, b)

class World_H9:
    def __init__(self, my_symbol, opponent):
        self.my_symbol = my_symbol
        self.opponent = opponent
        self.movement_44 = ['00D', '00R',
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
        
    def obtain_and_delete_number(self, numbers):
        if numbers:
            n = random.choice(numbers)
            numbers.remove(n)
            return n
        else:
            return None
    
    def bot(self, board, heuristic):
        pq = PriorityQueue()
        source = Quixo(board, self.my_symbol, self.opponent)

        """if self.i_win(source.board):
            print("Ganamos (Rodri y Guillermo)")
            return"""

        numbers = list(range(0, 44))
        
        for _ in range(len(self.movement_44)):
            i = self.obtain_and_delete_number(numbers)
            if source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == 0 or source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == self.my_symbol:
                obj = Movements(deepcopy(source.board))
                new_board = obj.moves(self.movement_44[i], self.my_symbol)

                new_node = Quixo(new_board, self.my_symbol, self.opponent)
                new_node.move = self.movement_44[i]
                new_node.calculate_heuristic(heuristic)
                pq.put(new_node)
        
        #H9
        pq_2 = PriorityQueue()
        pq_3 = PriorityQueue()
        move = pq.get()
        if move.heuristic_value[0] != math.inf:
            x = move.heuristic_value[0]
            while not pq.empty() and move.heuristic_value[0] == x:
                tuple = (move.heuristic_value[0]-move.heuristic_value[1], move.heuristic_value[0])
                move.heuristic_value = tuple
                pq_2.put(move)
                move = pq.get()

            move = pq_2.get()
            x = move.heuristic_value[0]
            while not pq_2.empty() and move.heuristic_value[0] == x:
                tuple = (move.heuristic_value[1], move.heuristic_value[0])
                move.heuristic_value = tuple
                pq_3.put(move)
                move = pq_2.get()
            my_move = pq_3.get()
        else:
            my_move = move
        #H9

        """if self.i_win(my_move.board):
            print("Ganamos (Rodri y Guillermo)")
            return"""
        
        return my_move.board, my_move.move
    
    def i_win(self, board):
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(board)):
            if board[i][0] == self.my_symbol:
                cont_0 += 1
                aux += 1
            if board[i][1] == self.my_symbol:
                cont_1 += 1
                aux += 1
            if board[i][2] == self.my_symbol:
                cont_2 += 1
                aux += 1
            if board[i][3] == self.my_symbol:
                cont_3 += 1
                aux += 1
            if board[i][4] == self.my_symbol:
                cont_4 += 1
                aux += 1

            if aux == 5:
                return True
            else:
                aux = 0

        if cont_0 == 5 or cont_1 == 5 or cont_2 == 5 or cont_3 == 5 or cont_4 == 5:
            return True

        aux_2 = 0

        for i in range(len(board)):
            if board[i][i] == self.my_symbol:
                aux += 1
            if board[i][4-i] == self.my_symbol:
                aux_2 += 1
        if aux == 5 or aux_2 == 5:
            return True
        
        return False

        

"""board = [[0]*5 for _ in range(5)]

play = World_H9()
play.bot(board, Heuristics_H9.heuristic_9)"""