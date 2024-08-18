from BFS_H5 import World_H5, Heuristics_H5
from BFS_H6 import World_H6, Heuristics_H6
from BFS_H7 import World_H7, Heuristics_H7
from BFS_H8 import World_H8, Heuristics_H8
from BFS_H9 import World_H9, Heuristics_H9
from BFS import World, Heuristics
from MinMaxAlBe import QuixoBot
#from pp import QuixoBot1
from Ann2 import QuixoBotANN
class evaluation:
    def __init__(self):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
    
    def evaluator(self):
        B = QuixoBotANN()
        #M = ()
        #B = World(1, -1)
        M= World_H5(-1, 1)
        h1 = 0
        h2 = 0
        B.reset(1)
        for j in range(1):
            self.board = [[0 for _ in range(5)] for _ in range(5)]
            for i in range(100):
                print("Turno: " , i)
                if self.i_win(1):
                    h1 += 1
                    break
                elif self.i_win(-1):
                    h2 += 1
                    break
                else:
                    self.board = B.play_turn(self.board)
                    #self.board, move = B.bot(self.board, Heuristics.heuristic)
                    self.board, move = M.bot(self.board, Heuristics_H5.heuristic_5)
            self.printPath()
                    
        print("Heuristica 1 gano: ", h1)
        print("Heuristica 2 gano: ", h2)

    def printPath(self):
        for i in range(5):
            print("-----------------------------")
            for j in range(5):
                print(self.board[i][j], end = "  |  ")
            print()
            
    def i_win(self, symbol):
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(self.board)):
            if self.board[i][0] == symbol:
                cont_0 += 1
                aux += 1
            if self.board[i][1] == symbol:
                cont_1 += 1
                aux += 1
            if self.board[i][2] == symbol:
                cont_2 += 1
                aux += 1
            if self.board[i][3] == symbol:
                cont_3 += 1
                aux += 1
            if self.board[i][4] == symbol:
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

        for i in range(len(self.board)):
            if self.board[i][i] == symbol:
                aux += 1
            if self.board[i][4-i] == symbol:
                aux_2 += 1
        if aux == 5 or aux_2 == 5:
            print("Ganó el jugador con el símbolo: ", symbol)
            return True
        
        return False
            
e = evaluation()
e.evaluator()
        
         