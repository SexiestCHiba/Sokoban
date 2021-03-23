import typing

import map.air as airfile
import map.dot
import map.box
import map.moveable
import map.player as playerfile
import map.superposeable


class Searcher:
    @classmethod
    def get_coords_player_from_map(cls, grid: typing.List[typing.List]):
        """Browse the game grid to find the player and to get his coords"""
        i = 0
        while i < len(grid):
            j = 0
            while j < len(grid[0]):
                entity = grid[i][j]
                if isinstance(entity, airfile.Air):
                    if isinstance(entity.get_last_superposer(), playerfile.Player):
                        return i, j
                j += 1
            i += 1

        raise IndexError("No player in the map.")

    @classmethod
    def get_coords_dots_from_map(cls, grid: typing.List[typing.List]):
        """Browse the game grid to find the dots and to get their coords"""
        dotsList = []
        i = 0
        while i < len(grid):
            j = 0
            while j < len(grid[0]):
                entity = grid[i][j]
                if isinstance(entity, airfile.Air) and isinstance(entity.superposer, map.dot.Dot):
                    dotsList.append((i, j))
                j += 1
            i += 1
        return dotsList

    @classmethod
    def get_coords_box_to_place_from_map(cls, grid: typing.List[typing.List]):
        """Browse the game grid to find all the boxes (execpted the ones in a dot) and to get their coords"""
        boxList = []
        i = 0
        while i < len(grid):
            j = 0
            while j < len(grid[0]):
                entity = grid[i][j]
                if isinstance(entity, airfile.Air):
                    if isinstance(entity.get_last_superposer(), map.box.Box) \
                         and not isinstance(entity.superposer, map.dot.Dot):
                        boxList.append((i, j))
                j += 1
            i += 1
        return boxList
