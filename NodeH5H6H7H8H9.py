class Quixo:
    def __init__(self, board, my_symbol, opponent):
        self.board = board
        self.my_symbol = my_symbol
        self.opponent = opponent
        self.heuristic_value = () #H5 #H6 #H7 #H8 #H9
        self.move = ''

    def __lt__(self, other):
        if not isinstance(other, Quixo):
            return False

        return self.heuristic_value > other.heuristic_value #H5 #H6 #H7 #H8 #H9

    def calculate_heuristic(self, heuristic):
        self.heuristic_value = heuristic(self, self.my_symbol, self.opponent)

#quiero ver lo del return, si si lo saca bien la de la 'pq' y si si hace bien el intercambio de valores en las tuplas