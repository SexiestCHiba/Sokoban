import map.entity_mapper
import solver.astar
import solver.node
import logic.searcher
import map.wall
import map.moveable

import typing
import math


class Solver:

    @classmethod
    def solve(cls, mapEntityClass: map.entity_mapper.EntityMapper) -> typing.List[typing.Tuple[int, int]]:
        """
        - Go from nearest box(from player position) to nearest validation dot - Done
        - Calculate in which path it must travel to place the box over the validation dot (use A* algorithm to check if
        player can go to position where it will move the move) - Done
        - If impossible, find if the same box can go to an other Dot - TODO
        - If impossible too, we search for an other box and we go back on this box later - TODO
        - Return finally a List of Tuple where player need to place, List can be empty or uncompleted if
        solver can't find a solution - Done
        """
        successfulDots: typing.List[typing.Tuple[int, int]] = []
        successfulBox: typing.List[typing.Tuple[int, int]] = []
        maze = mapEntityClass.grid_of_sprites
        coordsPlayer = logic.searcher.Searcher.get_coords_player_from_map(maze)
        path = [coordsPlayer]
        boxFinalPath = []
        while len(cls.get_coords_free_dots_from_map(maze, successfulDots)) > 0:
            coordsDots = cls.get_coords_free_dots_from_map(maze, successfulDots)
            coordsBox = cls.get_coords_free_box_from_map(maze, successfulBox)
            if len(coordsDots) == 0 or len(coordsBox) == 0:
                return cls.to_directions(cls.complete_path(path, mapEntityClass, boxFinalPath))
            # Search the nearest box
            nearestBox = cls.nearest_instance(coordsPlayer, coordsBox, successfulBox)
            # then we looking for the nearest validation dot
            nearestDot = cls.nearest_instance(nearestBox, coordsDots, successfulDots)

            if nearestBox == (-1, -1) or nearestDot == (-1, -1):
                raise Exception("Can found nearest Box or Dot")
            cls.boxPath(path, mapEntityClass, nearestBox, nearestDot, boxFinalPath, successfulBox, successfulDots)
            return cls.to_directions(cls.complete_path(path, mapEntityClass, boxFinalPath))

    @classmethod
    def distance(cls, coordA: typing.Tuple[int, int], coordB: typing.Tuple[int, int]) -> float:
        return math.sqrt(pow(coordB[0] - coordA[0], 2) + pow(coordB[1] - coordA[1], 2))

    @classmethod
    def nearest_instance(cls, coordsFrom: typing.Tuple[int, int], listTo: typing.List[typing.Tuple[int, int]],
                         exclude: typing.List[typing.Tuple[int, int]]) -> typing.Tuple[int, int]:
        i = 20000
        nearest: typing.Tuple[int, int] = (-1, -1)
        for c in listTo:
            if c not in exclude:
                tmp = cls.distance(coordsFrom, c)
                if tmp < i:
                    i = tmp
                    nearest = c
        return nearest

    @classmethod
    def get_coords_free_dots_from_map(cls, grid: typing.List[typing.List],
                                      successfulDots: typing.List[typing.Tuple[int, int]]) -> typing.List[
                                      typing.Tuple[int, int]]:
        """Return all dots which have no box on it"""
        dots = logic.searcher.Searcher.get_coords_dots_from_map(grid)
        freeDots = []
        for i in dots:
            if grid[i[0]][i[1]].superposer.superposer is None and i not in successfulDots:
                freeDots.append(i)
        return freeDots

    @classmethod
    def get_coords_free_box_from_map(cls, grid: typing.List[typing.List],
                                     successfulBox: typing.List[typing.Tuple[int, int]]) -> typing.List[
        typing.Tuple[int, int]]:
        """Return all box which haven't been moved on a dot"""
        box = logic.searcher.Searcher.get_coords_box_to_place_from_map(grid)
        freeBox = []
        for i in box:
            if i not in successfulBox:
                freeBox.append(i)
        return freeBox

    @classmethod
    def clear_path(cls, path: typing.List[typing.Tuple[int, int]]) -> typing.List[typing.Tuple[int, int]]:
        """Delete duplicate Tuple"""
        toDel = []
        for i in range(len(path)):
            if i < len(path) - 1:
                if path[i] == path[i + 1]:
                    toDel.append(i)
        for i in toDel[::-1]:
            del path[i]
        return path

    @classmethod
    def complete_path(cls, path: typing.List[typing.Tuple[int, int]], mapEntity,
                      boxPath: typing.List[typing.List[typing.Tuple[int, int]]]) -> typing.List[typing.Tuple[int, int]]:
        """
        give an uncomplete path in param and return path between 2 locations Tuple
        """
        newPath: typing.List[typing.Tuple[int, int]] = []
        cantWalk = []
        ignore = []
        for i in boxPath:
            for e in i:
                cantWalk.append(e)
        boxOnMap = logic.searcher.Searcher.get_coords_box_to_place_from_map(mapEntity.grid_of_sprites)
        for i in boxOnMap:
            ignore.append(i)
        for i in range(len(path)):
            if i < len(path) - 1:
                if len(cantWalk) != 0:
                    ignore.append(cantWalk[0])
                # aStarPath = solver.astar.Astar.solve(mapEntity, path[i], path[i + 1], ignore, cantWalk)
                aStarPath = solver.astar.Astar.solve(mapEntity, path[i], path[i + 1])
                if len(cantWalk) != 0:
                    ignore.remove(cantWalk[0])
                if aStarPath is not None:
                    for y in aStarPath:
                        newPath.append(y)
                        pathToDel = []
                        for e in range(len(cantWalk)):
                            if y == cantWalk[e]:
                                pathToDel.append(e)
                        for e in pathToDel[::-1]:
                            del cantWalk[e]
        # newPath.append(path[-1])
        return cls.clear_path(newPath)

    @classmethod
    def to_directions(cls, path):
        """Convert path Tuple to the direction Enum"""
        movementDirection = None
        directionsEnum = map.moveable.DIRECTION
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        newPath = []
        for i, value in enumerate(path):
            if i < len(path) - 1:
                movement = (path[i + 1][0] - value[0], path[i + 1][1] - value[1])
                if movement not in directions:
                    raise Exception("Movement isn't in direction", movement)  # Error
                if movement == (1, 0):
                    movementDirection = directionsEnum.DOWN
                if movement == (-1, 0):
                    movementDirection = directionsEnum.UP
                if movement == (0, 1):
                    movementDirection = directionsEnum.RIGHT
                if movement == (0, -1):
                    movementDirection = directionsEnum.LEFT
                newPath.append(movementDirection)
        return newPath

    @classmethod
    def boxPath(cls, path, mapEntityClass, nearestBox, nearestDot, boxFinalPath, successfulDots, successfulBox) -> None:
        """using A* algo from Box to Dot and return locations Tuple where the player need to be to move the box"""
        astar = solver.astar.Astar(mapEntityClass.mapper.grid_file)
        boxNode = astar.get_node(*nearestBox)
        dotNode = astar.get_node(*nearestDot)
        boxPath = astar.solve(boxNode, boxNode)
        boxPath2 = []
        for i in range(len(boxPath)):
            if i < len(boxPath) - 1:
                movement = (boxPath[i + 1][0] - boxPath[i][0], boxPath[i + 1][1] - boxPath[i][1])
                playerPosition = (boxPath[i][0] - movement[0], boxPath[i][1] - movement[1])
                path.append(playerPosition)
                path.append(boxPath[i])
                boxPath2.append(boxPath[i])
        # path.append(boxPath[-1])
        boxFinalPath.append(boxPath2)
        successfulDots.append(nearestDot)
        successfulBox.append(nearestBox)
