from NodeH5H6H7H8H9 import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import math
import random

class Heuristics_H5:
    #Creo que sería mejor que abarque símbolos separados, es decir, usar la 'heurística'
    #Si llego a hacer un 5 que termine porque puede que la 'pq' no saque ese nodo (5,4 y 4,0), chance le pongo un 'inf' para que la 'pq' lo escoja
    #Ver chat para la prioridad (no me interesa ordenarlos de menor a mayor, ni tampoco tomar los míos que sean mayores al oponente,
    # solo me importa hacer la resta y si se empatan tomar el que tenga el mío más grande)
    #Esta heurística hace un movimiento mío y a partir de ese movimiento checa mi línea máxima y la de mi oponente que pueden ser:
    # Me beneficio yo pero beneficio más al otro
    # Nos beneficiamos igual
    # Me beneficio yo y él no
    #Por lo tanto escogeré el movimiento óptimo para mí
    #H5
    @staticmethod
    def heuristic_5(node, my_symbol, opponent):
        #SE REDUJO ESTA FUNCION, EN VEZ DE TENER 2 LA HICE EN UNA, YA QUE LO UNICO QUE CAMBIA ES EL SIMBOLO QUE COMPARA
        #OOOOOOOOOOOOOOOOOOOOJJJJJJJJJJJJJJJJJJJOOOOOOOOO
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

        a = max_lines(my_symbol)
        b = max_lines(opponent)

        #Tengo que preguntar si en mi turno formo un 5 pero también el otro, gano yo ? o cómo sería ?
        #Si yo gano escojo de una ese movimiento (arriba se explica porqué)
        #Si el gana le pondremos '-inf' (esto no lo había pensado porque la 'pq' escoge la más óptima para mí pero
        # puede haber un caso en que sea 4,5 y todas peores 1,3, entonces agarraría esa como la más óptima, no creo que llege a pasar eso
        # pero por si acaso)
        
        #Es importante que primero vaya esta condición ya que si mi movimiento hace 5 míos y le formo 5 también, pierdo, por lo tanto,
        # primero checa si el tiene 5 y si no ya podemos pasar a la siguiente asegurandonos que no perderemos por formar 5 y 5
        if b == 5:
            return (-math.inf, a)
        elif a == 5:
            return (math.inf, a)
        else:
            return (a-b, a)

class World_H5:
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
                            '44U', '44L'
                            ]
        
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
        
        #AÑADIR LO DEL SUFFLE DE 'i' en todo donde exista el moves_44
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
        
        #H5
        pq_2 = PriorityQueue()
        move = pq.get()

        if move.heuristic_value[0] != math.inf:
            x = move.heuristic_value[0]
            #Al yo sacar el primer nodo de la 'pq' yo sé que nunca estará vacía porque hay otros movimientos existentes, eso me asegura que si entre a este while
            # ya que si se lo salta la 'pq_2' no tendría nada, pero esto nunca pasa
            #OOOOOOOJJJJJJJJJJJJJJOOOOOOOOOOO
            #AGREGUE 'not pq.empty()' porque puede que todos los nodos de la 'pq' sean iguales entonces llega un punto donde 'move' es none y hace cosas raras
            while not pq.empty() and move.heuristic_value[0] == x: #AGREGUE 'not pq.empty()'
                tuple = (move.heuristic_value[1], move.heuristic_value[0])
                move.heuristic_value = tuple
                pq_2.put(move)
                move = pq.get()

            my_move = pq_2.get()
        else:
            my_move = move
        #H5

        """if self.i_win(my_move.board):
            print("Ganamos (Rodri y Guillermo)")
            return"""
        
        #PREGUNTAR SI TAMBIEN REGRESAMOS EL MOVIMIENTO QUE HIZO EL BOT
        #OJOOOOOOOOO para quitar 'my_move.move'
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

play = World()
play.bot(board, Heuristics.heuristic_5)"""