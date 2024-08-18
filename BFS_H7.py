from NodeH5H6H7H8H9 import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import math
import random

class Heuristics_H7:
    #Esta heurística es la misma que la 'H6' pero en este caso toma de los mejores de mi oponente el peor para mí, esto debido a que no estoy
    # seguro de qué movimiento tomará y tengo que tener un lower bound ya que si llegará a agarrar otro que no es el lower bound yo sé que es mejor,
    # además, si su heurística es buena, es obvio que no va a agarrar uno que me beneficie a pesar de que sea uno de sus mejores
    #En otras palabras, de las mejores opciones de mi oponente toma la mejor lo que representa la peor para mí
    #H7
    @staticmethod
    def heuristic_7(node, my_symbol, opponent):
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

                new_node = Quixo(new_board, opponent, my_symbol)
                new_node.move = movement_44[i]
                new_node.heuristic_value = (max_lines(new_node.board, opponent), max_lines(new_node.board, my_symbol)) #(h, my_max)
                pq_h.put(new_node)
    
        #meter los nodos con los valores heurísticos más altos iguales
        # no nadamas voy a sacar el primero porque no estoy 100% seguro de que su heuristica vaya a tomar ese, por lo tanto saco los primeros iguales,
        # de esta forma ya existe más probabilidad de que le atinemos a un movimiento de su heurística
        move = pq_h.get()
        x = move.heuristic_value[0]
        while not pq_h.empty() and move.heuristic_value[0] == x:
            #Es importante que primero vaya esta condición ya que si mi movimiento hace 5 míos y le formo 5 también, pierdo, por lo tanto,
            # primero checa si el tiene 5 y si no ya podemos pasar a la siguiente asegurandonos que no perderemos por formar 5 y 5
            if move.heuristic_value[1] == 5:
                tuple = (-math.inf, move.heuristic_value[0])
            elif move.heuristic_value[0] == 5:
                tuple = (math.inf, move.heuristic_value[0])
            #Aquí se le agrega un signo '-' ya que con el '-' me va a dar el peor caso
            #El signo hace que se resten al reves, y si tiene coherencia, ya que mi peor caso es el mejor caso de mi oponente
            else:
                tuple = (move.heuristic_value[0]-move.heuristic_value[1], move.heuristic_value[0])

            pq_2h.put(tuple)

            move = pq_h.get()
        
        #SEGÚN chatGPT Y copilot NO AFECTA LA SOBRECARGA DE OPERADORES A OTRAS 'pq'

        #Si las optimalidades son iguales ya no lo tenemos que meter a una tercera 'pq' porque si son iguales eso significa que fueron
        # los mismos números que se restaron (siempre van a ser los mismos los del oponente, porque saco todos los mejores iguales, es decir,
        # puedo sacar 4 4 4 4 y míos pueden ser 1 4 2 1 por lo tanto si las optimalidades son iguales los números son iguales)
        tuple = pq_2h.get()

        #Si llega a sacar un '-math.inf' quiere decir que esa fue su mejor, es decir, que todas las demás son peores que esa, osea esa es la menos peor
        #No tengo que hacer ninguna verificación extra ya que yo me iré a ese nodo y si el agarra ese movimiento si o si perdera aunque él forme 5
        # si yo me voy a ese nodo y no agarra ese movimiento que fue el "mejor" el resto de los movimientos serán mejores para mí

        #Ahora bien, ya tengo sus mejores casos, de todos ellos escojo el peor, que se vuelve el mejor caso para mí, por lo tanto se le pone un signo '-'
        # ya que, en un principio, entre más alto el valor más prioridad y con el signo '-' como que lo voltea, entonces el que era más prioritario
        # se vuelve el menos prioritario
        return (-tuple[0], -tuple[1])


        #métele lo de si el hace 5 que de cajón no escoja ese movimiento

        #Tomar los mejores de mi oponenete en cada jugada, después de los mejores tomar el peor
        # esto significa que tomaré de los mejores de mi oponente el mejor para mí
        # esto funciona ya que puede haber un caso donde el mejor para mi oponente sea 3 y para mí un 4 por lo tanto dejaré ese movimiento como mi turno


class World_H7:
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
        pq_2 = PriorityQueue() #H7
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
        
        #H7
        move = pq.get()
        x = move.heuristic_value[0]
        while not pq.empty() and move.heuristic_value[0] == x:
            tuple = (move.heuristic_value[1], move.heuristic_value[0])
            move.heuristic_value = tuple
            pq_2.put(move)
            move = pq.get()

        my_move = pq_2.get()
        #H7

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

play = World_H7()
play.bot(board, Heuristics_H7.heuristic_7)"""