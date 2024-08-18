import math
import copy

class QuixoBot:
    def __init__(self):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.symbol = None
        self.opponent = None
        self.max_depth = 2
        
    def play_turn(self, board):
        self.board = board
        best_move = self.get_best_move(self.board)
        if best_move:
            i = int(best_move[0])
            j = int(best_move[1])
            self.board[i][j] = 'O'
            self.moves(self.board, best_move)
        return self.board
    
    def reset(self, symbol):
        self.board = [[0 for _ in range(5)] for _ in range(5)] 
        self.symbol = symbol
        
        
    def down(self, board, row, col):
        aux = board[row][col]
        for i in range(row, 4):
            board[i][col] = board[i+1][col]
        board[4][col] = aux

    def up(self, board, row, col):
        aux = board[row][col]
        for i in range(row, 0, -1):
            board[i][col] = board[i-1][col]
        board[0][col] = aux
                 
    def right(self, board, row, col):
        aux = board[row][col]
        for j in range(col, 4):
            board[row][j] = board[row][j + 1]
        board[row][4] = aux
        
    def left(self, board, row, col):
        aux = board[row][col]
        for j in range(col, 0, -1):
            board[row][j] = board[row][j-1]
        board[row][0] = aux
        
    def moves(self, board, move):
        i = int(move[0])
        j = int(move[1])
        d = move[2]

        if d == 'D':
            self.down(board, i, j)
        elif d == 'U':
            self.up(board, i, j)
        elif d == 'R':
            self.right(board, i, j)
        elif d == 'L':
            self.left(board, i, j)
            
        return board
    
    def heuristic(self, board, player):
        score = 0
        opponent = 'O' if player == 'X' else 'X'

        # Check for rows
        for row in board:
            player_count = row.count(player)
            opponent_count = row.count(opponent)
            score += player_count ** 2 - opponent_count ** 2

        # Check for columns
        for col in range(5):
            player_count = sum(row[col] == player for row in board)
            opponent_count = sum(row[col] == opponent for row in board)
            score += player_count ** 2 - opponent_count ** 2

        # Check for diagonals
        player_count = sum(board[i][i] == player for i in range(5))
        opponent_count = sum(board[i][i] == opponent for i in range(5))
        score += player_count ** 2 - opponent_count ** 2

        player_count = sum(board[i][4 - i] == player for i in range(5))
        opponent_count = sum(board[i][4 - i] == opponent for i in range(5))
        score += player_count ** 2 - opponent_count ** 2

        return score

    def minimax_alpha_beta(self, board, depth, is_maximizing, alpha, beta):
        if depth >= self.max_depth:
            return self.heuristic(board, 'O' if is_maximizing else 'X')

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_valid_moves():
                i = int(move[0])
                j = int(move[1])
                if board[i][j] == 0 or board[i][j] == 'X':
                    new_board = copy.deepcopy(board)
                    self.moves(new_board, move)
                    score = self.minimax_alpha_beta(new_board, depth+1, False, alpha, beta)
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break     
            return best_score
        else:
            best_score = math.inf
            for move in self.get_valid_moves():
                i = int(move[0])
                j = int(move[1])
                if board[i][j] == 0 or board[i][j] == 'O':
                    new_board = copy.deepcopy(board)
                    self.moves(new_board, move)
                    score = self.minimax_alpha_beta(new_board, depth+1, True, alpha, beta)
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def get_best_move(self, board):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for move in self.get_valid_moves():
            i = int(move[0])
            j = int(move[1])
            if board[i][j] == 0 or board[i][j] == 'O':
                new_board = copy.deepcopy(board)
                self.moves(new_board, move)
                score = self.minimax_alpha_beta(new_board, 0, False, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
        print(best_move)
        i = int(best_move[0])
        j = int(best_move[1])
        self.board[i][j] = 'O'
        self.moves(self.board, best_move)
        return self.board

    
    def get_valid_moves(self):
        return ['00D', '00R', '10U', '10D', '10R', '20U', '20D', '20R', '30U', '30D', '30R', '40U', '40R',
                '01D', '01L', '01R', '41U', '41L', '41R', '02D', '02L', '02R', '42U', '42L', '42R',
                '03D', '03L', '03R', '43U', '43L', '43R', '04D', '04L', '14U', '14D', '14L', '24U', '24D',
                '24L', '34U', '34D', '34L', '44U', '44L']

    def check_winner(self, board, player):
        for i in range(5):
            if all(board[i][j] == player for j in range(5)) or all(board[j][i] == player for j in range(5)):
                return True
        if all(board[i][i] == player for i in range(5)) or all(board[i][4-i] == player for i in range(5)):
            return True
        return False

    def print_board(self):
        for i in range(5):
            print("-----------------------------")
            for j in range(5):
                print(self.board[i][j], end = "  |  ")
            print()
        print("-----------------------------")

    def play(self):
        print("Welcome to Quixo!")
        self.print_board()

        while not self.check_winner(self.board, 'X') and not self.check_winner(self.board, 'O'):
            self.get_best_move(self.board)
                
            print("Computer's move:")
            self.print_board()

            if self.check_winner(self.board, 'O'):
                print("You lose!")
                break
            
                
            mov = input("Insert your move like this 00D, the numbers are rows (0-4), columns (0-4), and the direction (Down 'D', Up 'U', Right 'R', Left 'L') \n")   
            i = int(mov[0])
            j = int(mov[1])
            m = mov[2]
            
            if self.board[i][j] == 0 or self.board[i][j] == 'X':
                if (m == 'U' and i != 0) or (m == 'R' and j != 4) or (m == 'D' and i != 4) or (m == 'L' and j != 0):
                    self.board[i][j] = 'X'
                    self.moves(self.board, mov)
                else:
                    print("Move not allowed")
                    continue

                self.print_board()

                if self.check_winner(self.board, 'X'):
                    print("You win!")
                    break
            else:
                print("Move not allowed, try again")



game = QuixoBot()
game.play()
