import heapq
import map.wall
import map.box
import solver.node
import solver.pathNotFoundException


class Astar:
    """ From https://fr.wikipedia.org/wiki/Algorithme_A* and http://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/ """
    offsets = {(0, 1): "RIGHT", (1, 0): "DOWN", (0, -1): "LEFT", (-1, 0): "UP"}

    def __init__(self, grid):
        self.grid = [[solver.node.Node(i, j, grid[i][j]) for j in range(len(grid[i]))] for i in range(len(grid))]
        self.obstacle = {map.wall.Wall._character, map.box.Box._character}

    def get_node(self, line, column):
        return self.grid[line][column]

    def reset_grid_data(self):
        for line in self.grid:
            for node in line:
                node.reset_data()
    
    def reset_grid_calcul_data(self):
        for line in self.grid:
            for node in line:
                node.reset_calc_data()

    def is_obstacle(self, node):
        """Return True if node is an obstacle (wall or box) else return False"""
        return (node.character in self.obstacle and node.exception is False) or node.transform_to_obstacle

    def get_neighbors(self, node, goal):
        """Return a list of neighbors nodes from the left, right, up and down direction of `node` param if nodes aren't obstacle"""
        neighbors = []
        for x, y in self.offsets.keys():

            try:
                _node = self.grid[node["x"] + x][node["y"] + y]
            except IndexError:
                continue

            if not self.is_obstacle(_node):
                neighbors.append(_node)
            elif _node.x == goal.x and _node.y == goal.y:
                raise solver.pathNotFoundException.Path_not_found_exception("No path found")

        return neighbors

    def get_neighbor_from_openlist(self, neighbor, openlist):
        for data in openlist:
            _dict = data[3]
            if neighbor.x == _dict["x"] and neighbor.y == _dict["y"]:
                return _dict
        return False

    def neighbor_in_closedlist(self, neighbor, closedList):
        for _dict in closedList:
            if neighbor.x == _dict["x"] and neighbor.y == _dict["y"]:
                return True
        return False

    def solve(self, node_start, node_goal, include_coords_start=True):
        """Return a path to go from node_start to node_goal"""
        start = node_start.__dict__

        goal = node_goal
        
        closedList = []
        openList = []
        came_from = {}
        heapq.heappush(openList, (0, 0, id(start), start))

        while openList:
            current_node = heapq.heappop(openList)[3]

            if current_node["x"] == goal.x and current_node["y"] == goal.y:
                # path was found
                data = []
                while id(current_node) in came_from:
                    data.append(self.get_node(current_node["x"], current_node["y"]))
                    current_node = came_from[id(current_node)]
                if include_coords_start:
                    data.append(node_start)
                return list(reversed(data))

            neighbors = self.get_neighbors(current_node, goal)
            i = 0
            while i < len(neighbors):
                neighbor = neighbors[i]

                the_neighbor_from_openlist = self.get_neighbor_from_openlist(neighbor, openList)
                if not (self.neighbor_in_closedlist(neighbor, closedList)
                        or (the_neighbor_from_openlist is not False and neighbor.cost <= the_neighbor_from_openlist.get("cost", None))):
                    neighbor.cost = current_node["cost"] + 1
                    neighbor.heuristic = neighbor.cost * neighbor.heuristic_calc(goal)
                    neighbor_copy = neighbor.__dict__
                    came_from[id(neighbor_copy)] = current_node

                    class_current_node = self.get_node(current_node["x"], current_node["y"])
                    heapq.heappush(openList, (class_current_node.compare(neighbor), neighbor.heuristic, id(neighbor_copy), neighbor_copy))
                i += 1

            closedList.append(current_node)
        
        raise solver.pathNotFoundException.Path_not_found_exception("no path found", start["x"], start["y"], "&", goal.x, goal.y)
