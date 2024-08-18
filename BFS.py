from NodeQuixo import Quixo
from Movements import Movements
from queue import PriorityQueue
from copy import deepcopy
import random

#No las puedes sumar porque al final, todas estarán ocupadas entonces las sumas siempre darán lo mismo, además es mejor trabajar con el máximo

class Heuristics:
    @staticmethod
    #Esta es la heurística más obvia, escoge el movimiento que más símbolos en alguna línea tenga
    def heuristic(node, my_symbol, opponent):
        maximum = 0
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(node.board)):
            if node.board[i][0] == my_symbol:
                cont_0 += 1
                aux += 1
            if node.board[i][1] == my_symbol:
                cont_1 += 1
                aux += 1
            if node.board[i][2] == my_symbol:
                cont_2 += 1
                aux += 1
            if node.board[i][3] == my_symbol:
                cont_3 += 1
                aux += 1
            if node.board[i][4] == my_symbol:
                cont_4 += 1
                aux += 1

            maximum = max(maximum, aux)
            aux = 0

        maximum = max(maximum, cont_0, cont_1, cont_2, cont_3, cont_4)

        aux_2 = 0

        for i in range(len(node.board)):
            if node.board[i][i] == my_symbol:
                aux += 1
            if node.board[i][4-i] == my_symbol:
                aux_2 += 1
        
        maximum = max(maximum, aux, aux_2)
        return maximum

    #Esta es la heurística más obvia, escoge el movimiento que más símbolos JUNTOS en alguna línea tenga
    @staticmethod
    def heuristic_2(node, my_symbol, opponent):
        maximum = 0
        cont_0 = 0
        max_0 = 0
        cont_1 = 0
        max_1 = 0
        cont_2 = 0
        max_2 = 0
        cont_3 = 0
        max_3 = 0
        cont_4 = 0
        max_4 = 0
        aux = 0
        max_aux = 0
        for i in range(len(node.board)):
            if node.board[i][0] == my_symbol:
                cont_0 += 1
                aux += 1
            else:
                max_0 = max(max_0, cont_0)
                cont_0 = 0
                #Esto podría no ponerse SOLO en la primer columna
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][1] == my_symbol:
                cont_1 += 1
                aux += 1
            else:
                max_1 = max(max_1, cont_1)
                cont_1 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][2] == my_symbol:
                cont_2 += 1
                aux += 1
            else:
                max_2 = max(max_2, cont_2)
                cont_2 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][3] == my_symbol:
                cont_3 += 1
                aux += 1
            else:
                max_3 = max(max_3, cont_3)
                cont_3 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][4] == my_symbol:
                cont_4 += 1
                aux += 1
            else:
                max_4 = max(max_4, cont_4)
                cont_4 = 0
                max_aux = max(max_aux, aux)
                aux = 0

            max_aux = max(max_aux, aux)
            maximum = max(maximum, max_aux)
            aux = 0
            max_aux = 0

        max_0 = max(max_0, cont_0)
        max_1 = max(max_1, cont_1)
        max_2 = max(max_2, cont_2)
        max_3 = max(max_3, cont_3)
        max_4 = max(max_4, cont_4)
        maximum = max(maximum, max_0, max_1, max_2, max_3, max_4)

        aux_2 = 0
        max_aux_2 = 0

        for i in range(len(node.board)):
            if node.board[i][i] == my_symbol:
                aux += 1
            else:
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][4-i] == my_symbol:
                aux_2 += 1
            else:
                max_aux_2 = max(max_aux_2, aux_2)
                aux_2 = 0
        
        max_aux = max(max_aux, aux)
        max_aux_2 = max(max_aux_2, aux_2)
        maximum = max(maximum, max_aux, max_aux_2)
        return maximum
    
    #Es lo mismo que la 'heuristic' pero ahora cuento los símbolos de mi oponente
    # Se guardarán valores negativos para que la 'pq' saque de las líneas máximas la más pequeña
    @staticmethod
    def heuristic_3(node, my_symbol, opponent):
        maximum = 0
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(node.board)):
            if node.board[i][0] == opponent:
                cont_0 += 1
                aux += 1
            if node.board[i][1] == opponent:
                cont_1 += 1
                aux += 1
            if node.board[i][2] == opponent:
                cont_2 += 1
                aux += 1
            if node.board[i][3] == opponent:
                cont_3 += 1
                aux += 1
            if node.board[i][4] == opponent:
                cont_4 += 1
                aux += 1

            maximum = max(maximum, aux)
            aux = 0

        maximum = max(maximum, cont_0, cont_1, cont_2, cont_3, cont_4)

        aux_2 = 0

        for i in range(len(node.board)):
            if node.board[i][i] == opponent:
                aux += 1
            if node.board[i][4-i] == opponent:
                aux_2 += 1
        
        maximum = max(maximum, aux, aux_2)
        return -maximum

    #Es lo mismo que la 'heuristic_2' pero ahora cuento los símbolos de mi oponente
    # Se guardarán valores negativos para que la 'pq' saque de las líneas máximas la más pequeña
    @staticmethod
    def heuristic_4(node, my_symbol, opponent):
        maximum = 0
        cont_0 = 0
        max_0 = 0
        cont_1 = 0
        max_1 = 0
        cont_2 = 0
        max_2 = 0
        cont_3 = 0
        max_3 = 0
        cont_4 = 0
        max_4 = 0
        aux = 0
        max_aux = 0
        for i in range(len(node.board)):
            if node.board[i][0] == opponent:
                cont_0 += 1
                aux += 1
            else:
                max_0 = max(max_0, cont_0)
                cont_0 = 0
                #Esto podría no ponerse SOLO en la primer columna
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][1] == opponent:
                cont_1 += 1
                aux += 1
            else:
                max_1 = max(max_1, cont_1)
                cont_1 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][2] == opponent:
                cont_2 += 1
                aux += 1
            else:
                max_2 = max(max_2, cont_2)
                cont_2 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][3] == opponent:
                cont_3 += 1
                aux += 1
            else:
                max_3 = max(max_3, cont_3)
                cont_3 = 0
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][4] == opponent:
                cont_4 += 1
                aux += 1
            else:
                max_4 = max(max_4, cont_4)
                cont_4 = 0
                max_aux = max(max_aux, aux)
                aux = 0
        
            max_aux = max(max_aux, aux)
            maximum = max(maximum, max_aux)
            aux = 0
            max_aux = 0

        max_0 = max(max_0, cont_0)
        max_1 = max(max_1, cont_1)
        max_2 = max(max_2, cont_2)
        max_3 = max(max_3, cont_3)
        max_4 = max(max_4, cont_4)
        maximum = max(maximum, max_0, max_1, max_2, max_3, max_4)

        aux_2 = 0
        max_aux_2 = 0

        for i in range(len(node.board)):
            if node.board[i][i] == opponent:
                aux += 1
            else:
                max_aux = max(max_aux, aux)
                aux = 0
            if node.board[i][4-i] == opponent:
                aux_2 += 1
            else:
                max_aux_2 = max(max_aux_2, aux_2)
                aux_2 = 0
        
        max_aux = max(max_aux, aux)
        max_aux_2 = max(max_aux_2, aux_2)
        maximum = max(maximum, max_aux, max_aux_2)
        return -maximum


class World:
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
            return None  # Todos los números ya fueron seleccionados
    
    def bot(self, board, heuristic):
        #No me importa si ya han sido visitados porque puede que en la partida si se repita el mismo tablero
        # y no me interesa porque en este caso no aplica lo de "si antes ya llegue a ese estado lo marco como visitado
        # y ya no creo ni me interesan los estados en la 'pq'"
        #Además no me importa porque cada vez se cambia el tablero debido a las jugadas de mi oponente
        #es decir, no pasa lo del cubo de que si primero hice 12 movimientos a la proxima hago 11 porque si no regreso al estado anterior,
        # aqui no pasa eso porque nunca regresará al estado anterior por el movimiento del oponente

        pq = PriorityQueue()
        
        source = Quixo(board, self.my_symbol, self.opponent)

        #No me sirve de nada meter el source a la 'pq'
        #No es necesario el 'while' porque no tengo que llegar a la solución en un turno,
        # es una jugada por turno, por lo tanto solo lo sacaré de la 'pq' 1 vez, lo cual representa mi jugada

        """if self.i_win(source.board):
            print("Ganamos (Rodri y Guillermo)")
            return"""
        
        #AÑADIR LO DEL SUFFLE DE 'i' en todo donde exista el moves_44
        #no se puede hacer 'self.numbers' porque en la primera llamada se vacían todos, y como ya no se crean más objetos de la clase 'World'
        # la lista 'numbers' a partir de ahí se quedaría vacía y no se generaría de nuevo
        numbers = list(range(0, 44))

        for _ in range(len(self.movement_44)):
            i = self.obtain_and_delete_number(numbers)
            if source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == 0 or source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == self.my_symbol:
                #En la clase Quixo_Movements necesita recibir un board y regresarlo ya modificado
                #Necesita tener 2 funciones, la de hacer un movimiento manualmente y la de hacer un movimiento(esta ultima es para el bfs)
                obj = Movements(deepcopy(source.board))
                new_board = obj.moves(self.movement_44[i], self.my_symbol)

                new_node = Quixo(new_board, self.my_symbol, self.opponent)
                new_node.move = self.movement_44[i]
                new_node.calculate_heuristic(heuristic)
                pq.put(new_node)
        
        my_move = pq.get()

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

        

"""board = [0 * 5 for _ in range(5)]

play = World()
play.bot(board, Heuristics.heuristic)"""