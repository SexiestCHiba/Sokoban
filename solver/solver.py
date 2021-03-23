import solver.astar
import logic.searcher
import map.moveable
import map.box


class Solver:
    def __init__(self, player):
        self.player = player
        self.astar = solver.astar.Astar(player.entity_mapper.mapper.grid_file)
        self.boxs_to_place = set(logic.searcher.Searcher.get_coords_box_to_place_from_map(player.entity_mapper.grid_of_sprites))
        self.dots = set(logic.searcher.Searcher.get_coords_dots_from_map(player.entity_mapper.grid_of_sprites))

    def get_box_near_player(self):
        player_node = self.astar.get_node(self.player.position[0], self.player.position[1])
        near_box_data = [None, None]

        for box in self.boxs_to_place:
            node_box = self.astar.get_node(box[0], box[1])
            heuristic = player_node.heuristic_calc(node_box)
            
            if near_box_data[0] is None or heuristic <= near_box_data[1]:
                near_box_data[0] = node_box
                near_box_data[1] = heuristic
        
        return near_box_data[0], player_node

    def get_dot_near_box(self, box_node):
        near_dot_data = [None, None]
        for dot in self.dots:
            node_dot = self.astar.get_node(dot[0], dot[1])
            heuristic = box_node.heuristic_calc(node_dot)
            
            if near_dot_data[0] is None or heuristic <= near_dot_data[1]:
                near_dot_data[0] = node_dot
                near_dot_data[1] = heuristic
        
        return near_dot_data[0], box_node

    def get_symetric_node(self, from_node, to_node):
        relative_position = (to_node.x - from_node.x, to_node.y - from_node.y)
        return self.astar.get_node(from_node.x - relative_position[0], from_node.y - relative_position[1])

    def get_diagonal_node(self, from_node, relative_position):
        next_target_pos = [from_node.x + relative_position[0], from_node.y + relative_position[1]]
        next_target_pos_temoin = next_target_pos[:]

        additive = [1, -1]
        if relative_position[1]:
            arg = 0
        else:
            arg = 1

        next_target_pos[arg] += additive[0]
        next_target = self.astar.get_node(*next_target_pos)
        if self.astar.is_obstacle(next_target):
            next_target_pos = next_target_pos_temoin
            next_target_pos[arg] += additive[1]
            next_target = self.astar.get_node(*next_target_pos)
            if self.astar.is_obstacle(next_target):
                raise Exception("No diagonal available found.", next_target.x, next_target.y)
        
        return next_target

    def analyse_path_from_box_to_dot(self, path):
        box_node = path[0]
        target_dot = path[-1]
        path_predecalage = path[:-1]
        path_postdecalage = path[1:]
        steps = []
        history = None
        intermediate_target = None

        for i in range(len(path_postdecalage)):
            try:
                previous = path_predecalage[i - 1]
            except IndexError:
                previous = None
            current = path_predecalage[i]
            post = path_postdecalage[i]
            
            symetric_node = self.get_symetric_node(current, post)
            if self.astar.is_obstacle(symetric_node):
                steps = False
                if current == box_node:
                    post.transform_to_obstacle = True
                    if post == target_dot:
                        relative_position = (post.x - current.x, post.y - current.y)
                        intermediate_target = self.get_diagonal_node(current, relative_position)
                    break
                else:
                    current.transform_to_obstacle = True
            elif steps is not False:
                bifurcation = self.get_bifurcation_from_path(current, post)
                if bifurcation != history:
                    if history is not None:
                        steps.extend([{previous: current}, {symetric_node: current}])
                    history = bifurcation

            if i == len(path_postdecalage) - 1 and steps is not False:
                steps.append({current: post})

        return steps, self.get_symetric_node(path[0], path[1]), intermediate_target

    def get_bifurcation_from_path(self, current, post):
        relative_position = (post.x - current.x, post.y - current.y)
        return self.astar.offsets[relative_position]

    def generate_steps(self, box_node, dot_node):
        box_node.exception = True
        change_target = False
        intermediate_target = None
        default = True
        path_from_box_to_dot_base = []
    
        path_from_box_to_dot = self.astar.solve(box_node, dot_node)
        analyse = self.analyse_path_from_box_to_dot(path_from_box_to_dot)
        while analyse[0] is False:
            if analyse[2]:
                param = (box_node, analyse[2])
                intermediate_target = analyse[2]
                change_target = True
                default = False
            else:
                if change_target:
                    dot_node.transform_to_obstacle = False
                    param = (intermediate_target, dot_node, False)
                    default = False
                else:
                    param = (box_node, dot_node)
                    default = True
                change_target = False

            path_from_box_to_dot = self.astar.solve(*param)
            self.astar.reset_grid_calcul_data()

            if not default:
                path_from_box_to_dot_base.extend(path_from_box_to_dot)
                if change_target is False:
                    analyse = self.analyse_path_from_box_to_dot(path_from_box_to_dot_base)
                else:
                    analyse = False, None, None
            else:
                path_from_box_to_dot_base = []
                analyse = self.analyse_path_from_box_to_dot(path_from_box_to_dot)
        
        self.astar.reset_grid_data()
        return analyse

    def path_for_player_to_join_adjacent_box(self, player_node, adjacent_box_node):
        path = self.astar.solve(player_node, adjacent_box_node, include_coords_start=False)
        self.astar.reset_grid_calcul_data()
        return path

    def get_path_from_steps(self, steps, box_node):
        box_node.exception = True
        path = []

        for i, step_dict in enumerate(steps, start=1):
            goal = tuple(step_dict.keys())[0]
            box = step_dict[goal]
            if i % 2 == 0:
                box.transform_to_obstacle = True
            player_node = self.astar.get_node(self.player.position[0], self.player.position[1])
            path.extend(self.astar.solve(player_node, goal, include_coords_start=False))

            if path:
                self.player.position = path[-1].x, path[-1].y

            self.astar.reset_grid_data()
            box_node.exception = True
        
        return path

    def transform_path_to_direction(self, path):
        path_predecalage = path[:-1]
        path_postdecalage = path[1:]
        path = []

        for i in range(len(path_postdecalage)):
            current = path_predecalage[i]
            post = path_postdecalage[i]
            relative_position = (post.x - current.x, post.y - current.y)
            path.append(getattr(map.moveable.DIRECTION, self.astar.offsets[relative_position]))
                
        return path

    def get_full_path(self):
        full_path = []

        while self.dots and self.boxs_to_place:
            near_box_from_player = self.get_box_near_player()
            near_dot_from_box = self.get_dot_near_box(near_box_from_player[0])[0]

            steps, adjacent_box_node, _ = self.generate_steps(near_box_from_player[0], near_dot_from_box)

            path_to_join_adjacent_box = self.path_for_player_to_join_adjacent_box(near_box_from_player[1], adjacent_box_node)
            
            full_path.extend(path_to_join_adjacent_box)

            if full_path:
                self.player.position = full_path[-1].x, full_path[-1].y
            
            path_from_steps = self.get_path_from_steps(steps, near_box_from_player[0])

            full_path.extend(path_from_steps)

            self.boxs_to_place.remove((near_box_from_player[0].x, near_box_from_player[0].y))
            self.dots.remove((near_dot_from_box.x, near_dot_from_box.y))
            self.astar.reset_grid_data()
            near_box_from_player[0].character = " "
            near_dot_from_box.character = "#"
            near_box_from_player[1].character = " "
            self.astar.get_node(self.player.position[0], self.player.position[1]).character = "@"

        self.player.position = self.player.position_start
        full_path.insert(0, self.astar.get_node(self.player.position[0], self.player.position[1]))
        self.player.full_path = self.transform_path_to_direction(full_path)
        self.player.full_path_temoin = self.player.full_path[:]

        return True
