from NodeH5H6H7H8H9 import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import math
import random

class Heuristics_H8:
    #Esta heurística hace un movimiento mío, luego hace los 44 del otro y ve el más óptimo de todos ellos sin tomar en cuenta sus mejores
    # 4,3 y 2,0
    #H8
    @staticmethod
    def heuristic_8(node, my_symbol, opponent):
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
        if max_lines(node.board, my_symbol) == 5:
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

                new_node = Quixo(new_board, opponent, my_symbol)
                new_node.move = movement_44[i]
                a = max_lines(new_node.board, opponent) #opponent
                b = max_lines(new_node.board, my_symbol) #my
                new_node.heuristic_value = (a-b, a)
                pq_h.put(new_node)
    
        #En esta heurística no saco las líneas máximas si no que saco los más óptimos
        #Aquí si es necesario una 'pq' para las optimalidades iguales, ya que en este caso si se pueden formar optimalidades iguales con diferentes
        # números porque no estoy tomando solo los máximos
        move = pq_h.get()
        x = move.heuristic_value[0]
        while not pq_h.empty() and move.heuristic_value[0] == x:
            pq_2h.put((move.heuristic_value[1], move.heuristic_value[0]))
            move = pq_h.get()
        
        aux = pq_2h.get()

        #Se le ponen ambas negativas, tanto la optimalidad porque su mejor es mi peor, 
        # como al valor de la línea máxima porque la más alta no es la que debo de tomar

        #Aquí esta lo de 5 y 5
        if aux[0] == 5:
            tuple = (-math.inf, -aux[0])
        # a-b = x --> a = x + b --> b = a-x
        # osea 'elif b == 5:'
        elif aux[0] - aux[1] == 5:
            tuple = (math.inf, -aux[0])
        else:
            tuple = (-aux[1], -aux[0])

        return tuple


        #métele lo de si el hace 5 que de cajón no escoja ese movimiento

class World_H8:
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
        pq_2 = PriorityQueue() #H8
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

        #H8
        move = pq.get()
        x = move.heuristic_value[0]
        while not pq.empty() and move.heuristic_value[0] == x:
            tuple = (move.heuristic_value[1], move.heuristic_value[0])
            move.heuristic_value = tuple
            pq_2.put(move)
            move = pq.get()

        my_move = pq_2.get()
        #H8

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

play = World_H8()
play.bot(board, Heuristics_H8.heuristic_8)"""