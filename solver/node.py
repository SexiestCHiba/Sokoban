class Node:
    """ From https://fr.wikipedia.org/wiki/Algorithme_A* """
    def __init__(self, x, y, character, cost=0, heuristic=0):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.character = character
        self.exception = False
        self.transform_to_obstacle = False

    def compare(self, other):
        if self.heuristic < other.heuristic:
            return 1
        elif self.heuristic == other.heuristic:
            return 0
        else:
            return -1

    def heuristic_calc(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def reset_data(self):
        self.transform_to_obstacle = False
        self.exception = False
        self.reset_calc_data()

    def reset_calc_data(self):
        self.heuristic = 0
        self.cost = 0
