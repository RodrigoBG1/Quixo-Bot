class Movements:
    def __init__(self, path):
        # path == board
        self.path = path
        self.sim = True
        
    def down(self, row, col):
        aux = self.path[row][col]

        for i in range(row, 4):
            self.path[i][col] = self.path[i+1][col]

        self.path[4][col] = aux

    def up(self, row, col):
        aux = self.path[row][col]

        for i in range(row, 0, -1):
            self.path[i][col] = self.path[i-1][col]

        self.path[0][col] = aux
                 
    def right(self, row, col):
        aux = self.path[row][col]

        for j in range(col, 4):
            self.path[row][j] = self.path[row][j + 1]

        self.path[row][4] = aux
        
    
    def left(self, row, col):
        aux = self.path[row][col]

        for j in range(col, 0, -1):
            self.path[row][j] = self.path[row][j-1]

        self.path[row][0] = aux
        
        
    def moves(self, move, symbol):
        # code  0 = c, 1 = o, 2 = d, 3 = t, 4 = f   U = Up, D = Down, R = Right, L = Left
        # first caracter is i, second is j and third is direction
        # Ej. 00D, 44U
        i = int(move[0])
        j = int(move[1])
        self.path[i][j] = symbol
        d = move[2]

        if d == 'D':
            self.down(i,j)
        elif d == 'U':
            self.up(i,j)
        elif d == 'R':
            self.right(i,j)
        elif d == 'L':
            self.left(i,j)
            
        return self.path
    
    def player(self):
        if self.sim:
            symbol = 1
            self.sim = False
        else:
            symbol = -1
            self.sim = True
        return symbol

    
    def play(self):
        symbol = self.player()
        while True:
            mov = input("Insert your move like this 00D, the numbers are rows (0-4), columns (0-4), and the direction (Down 'D', Up 'U', Right 'R', Left 'L') \n")   
            i = int(mov[0])
            j = int(mov[1])
            m = mov[2]
            
            if (self.path[i][j] == 0 or self.path[i][j] == symbol) and (not 1 <= i <= 3 or not 1 <= j <= 3): 
                if m == 'U' and i != 0:
                    self.moves(mov, symbol)
                    symbol = self.player()
                elif m == 'R' and j != 4:
                    self.moves(mov, symbol)
                    symbol = self.player()
                elif m == 'D' and i != 4:
                    self.moves(mov, symbol)
                    symbol = self.player()
                elif m == 'L' and j != 0:
                    self.moves(mov, symbol)
                    symbol = self.player()
                    
                self.printPath()

                if self.i_win(self.path, 1):
                    print("!WINER! ")
                    break
                elif self.i_win(self.path, -1):
                    print("!WINER! ")
                    break
            else: 
                print("Not allowed")

            
    def i_win(self, symbol):
        cont_0 = 0
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0
        aux = 0
        for i in range(len(self.path)):
            if self.path[i][0] == symbol:
                cont_0 += 1
                aux += 1
            if self.path[i][1] == symbol:
                cont_1 += 1
                aux += 1
            if self.path[i][2] == symbol:
                cont_2 += 1
                aux += 1
            if self.path[i][3] == symbol:
                cont_3 += 1
                aux += 1
            if self.path[i][4] == symbol:
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

        for i in range(len(self.path)):
            if self.path[i][i] == symbol:
                aux += 1
            if self.path[i][4-i] == symbol:
                aux_2 += 1
        if aux == 5 or aux_2 == 5:
            print("Ganó el jugador con el símbolo: ", symbol)
            return True
        
        return False
                
    def printPath(self):
        for i in range(5):
            print("-----------------------------")
            for j in range(5):
                print(self.path[i][j], end = "  |  ")
            print()
            
    def reset(self):
        self.path = [[0] * 5 for _ in range(5)]
        
path = [[0] * 5 for _ in range(5)]        
"""M = Movements(path)
M.play()"""