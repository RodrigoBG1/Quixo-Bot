from NodeQuixoA import Quixo
from Movements import Movements
from copy import deepcopy
import unittest
from queue import PriorityQueue

#Aqui cambio la ficha que me toca
MY_SYMBOL = 'o'

class Heuristics:
    @staticmethod
    def heuristic(node):
        board = node.board
        my_symbol = 'o' 

        # Check for rows and columns
        def check_line(line):
            consecutive = 0
            max_consecutive = 0
            for symbol in line:
                if symbol == my_symbol:
                    consecutive += 1
                else:
                    max_consecutive = max(max_consecutive, consecutive)
                    consecutive = 0
            max_consecutive = max(max_consecutive, consecutive)
            return 5 - max_consecutive

        distance = 0
        for row in board:
            distance += check_line(row)
        for col in range(5):
            column = [row[col] for row in board]
            distance += check_line(column)

        # Check for diagonals
        main_diagonal = [board[i][i] for i in range(5)]
        distance += check_line(main_diagonal)
        secondary_diagonal = [board[i][4 - i] for i in range(5)]
        distance += check_line(secondary_diagonal)

        return distance

class World:
    def __init__(self):
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
        self.visited = set()
        
    def bot(self, board, heuristic):
        pq = PriorityQueue()
        source = Quixo(board)

        if self.i_win(source.board):
            print("Ganamos (Rodri y Guillermo)")
            return
        
        while not pq.empty():
            curr_node = pq.get()
            
            if self.i_win(curr_node.board):
                return self.path[1]

            if not self.is_visited(curr_node.board):
                self.visited.add(curr_node.board)
                for i in range(len(self.movement_44)):
                    if source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == ' ' or source.board[int(self.movement_44[i][0])][int(self.movement_44[i][1])] == MY_SYMBOL:
                        #En la clase Quixo_Movements necesita recibir un board y regresarlo ya modificado
                        #Necesita tener 2 funciones, la de hacer un movimiento manualmente y la de hacer un movimiento(esta ultima es para el bfs)
                        obj = Movements(deepcopy(source.board))
                        new_board = obj.moves(self.movement_44[i])
                        if not self.is_visited(curr_node.board):
                            new_node = Quixo(new_board)
                            new_node.distance = curr_node.distance + 1
                            new_node.move = self.movement_44[i]
                            new_node.path.extend(curr_node.path)
                            new_node.path.append(new_node)
                            new_node.calculate_heuristic(heuristic)
                            pq.put(new_node)
        
        my_move = pq.get()

        if self.i_win(my_move.board):
            print("Ganamos (Rodri y Guillermo)")
            return
        
        return my_move.board
    
    def is_visited(self, board):
        return board in self.visited
    
    
    def i_win(self, board):
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(board)):
            if board[i][0] == MY_SYMBOL:
                cont_0 += 1
                aux += 1
            if board[i][1] == MY_SYMBOL:
                cont_1 += 1
                aux += 1
            if board[i][2] == MY_SYMBOL:
                cont_2 += 1
                aux += 1
            if board[i][3] == MY_SYMBOL:
                cont_3 += 1
                aux += 1
            if board[i][4] == MY_SYMBOL:
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
            if board[i][i] == MY_SYMBOL:
                aux += 1
            if board[i][4-i] == MY_SYMBOL:
                aux_2 += 1
        if aux == 5 or aux_2 == 5:
            return True
        
        return False

        

class TestQuixo(unittest.TestCase):
    def setUp(self):
        self.board = [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'o', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']
        ]
        self.world = World()

    def test_bot(self):
        # Test the bot function with the initial board
        result = self.world.bot(self.board, Heuristics.heuristic)
        expected_result = [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'o', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']
        ]
        self.assertEqual(result, expected_result)

    def test_is_visited(self):
        # Test the is_visited function
        self.world.visited.add(tuple(map(tuple, self.board)))
        self.assertTrue(self.world.is_visited(self.board))

    def test_i_win(self):
        # Test the i_win function with a winning board
        winning_board = [
            ['o', 'o', 'o', 'o', 'o'],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']
        ]
        self.assertTrue(self.world.i_win(winning_board))

        # Test the i_win function with a non-winning board
        non_winning_board = [
            ['o', ' ', ' ', ' ', ' '],
            [' ', 'o', ' ', ' ', ' '],
            [' ', ' ', 'o', ' ', ' '],
            [' ', ' ', ' ', 'o', ' '],
            [' ', ' ', ' ', ' ', 'o']
        ]
        self.assertFalse(self.world.i_win(non_winning_board))

if __name__ == '__main__':
    unittest.main()