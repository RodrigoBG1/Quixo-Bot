from NodeH5H6H7H8H9 import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import math
import random

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


        #métele lo de si el hace 5 que de cajón no escoja ese movimiento

        #Tomar los mejores de mi oponenete en cada jugada, después de los mejores tomar el peor
        # esto significa que tomaré de los mejores de mi oponente el mejor para mí
        # esto funciona ya que puede haber un caso donde el mejor para mi oponente sea 3 y para mí un 4 por lo tanto dejaré ese movimiento como mi turno


class World_H6:
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
        pq_2 = PriorityQueue() #H6
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
        
        #H6
        move = pq.get()
        if move.heuristic_value[0] != math.inf:
            x = move.heuristic_value[0]
            while not pq.empty() and move.heuristic_value[0] == x:
                tuple = (move.heuristic_value[1], move.heuristic_value[0])
                move.heuristic_value = tuple
                pq_2.put(move)
                move = pq.get()

            my_move = pq_2.get()
        else:
            my_move = move
        #H6

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

play = World_H6()
play.bot(board, Heuristics_H6.heuristic_6)"""