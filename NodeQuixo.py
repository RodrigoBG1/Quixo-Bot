class Quixo:
    def __init__(self, board, my_symbol, opponent):
        self.board = board
        self.my_symbol = my_symbol
        self.opponent = opponent
        self.heuristic_value = 0
        self.move = ''

    def __lt__(self, other):
        if not isinstance(other, Quixo):
            return False
        
        #Creo que tengo que cambiar el '<' a '>' porque quiero el mayor valor, es decir, la línea que tenga más símbolos míos
        return self.heuristic_value > other.heuristic_value

    def calculate_heuristic(self, heuristic):
        self.heuristic_value = heuristic(self, self.my_symbol, self.opponent)