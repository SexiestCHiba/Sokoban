import typing

import map.box as boxfile
import map.mapper
import map.moveable
import map.player as playerfile
import map.superposeable as superposeablefile


class Mover:
    @classmethod
    def move_player(cls, player, direction: map.moveable.DIRECTION):
        """allows to add the new place of the player"""
        coords_player = player.position
        grid = player.entity_mapper.grid_of_sprites
        mapper = player.entity_mapper.mapper

        entity_coords = grid[coords_player[0]][coords_player[1]]
        player_instance = cls.get_instance_from_coords(entity_coords, playerfile.Player)
        new_coords_player = player_instance.get_new_coords(direction, coords_player)

        if mapper.coords_in_map(new_coords_player):
            entity_new_coords = grid[new_coords_player[0]][new_coords_player[1]]

            if issubclass(entity_new_coords.__class__, superposeablefile.Superposeable):

                try:
                    if not (cls.move_box(mapper, grid, new_coords_player, direction)):
                        return False
                except AttributeError:
                    pass

                entity_new_coords.get_last_superposeable(True).superposer = player_instance
                entity_coords.get_last_superposeable(True).superposer = None

                player_instance.dx = (new_coords_player[1] - coords_player[1]) * mapper.measure["horizontal"]
                player_instance.dy = (new_coords_player[0] - coords_player[0]) * mapper.measure["vertical"]

                player_instance.update()

                player_instance.dx = 0
                player_instance.dy = 0

                player.position = new_coords_player

                return True

        return False

    @classmethod
    def move_box(cls, mapper: map.mapper.Mapper, grid, coords_box: typing.Tuple[int, int],
                 direction: map.moveable.DIRECTION):
        """Change the coords of a box"""
        entity_coords = grid[coords_box[0]][coords_box[1]]
        box_instance = cls.get_instance_from_coords(entity_coords, boxfile.Box)
        box_new_coords = box_instance.get_new_coords(direction, coords_box)

        if mapper.coords_in_map(box_new_coords):
            """Check if a box is in front of a wall dans and print a move is impossible"""
            entity_new_coords = grid[box_new_coords[0]][box_new_coords[1]]
            if issubclass(entity_new_coords.__class__, superposeablefile.Superposeable) \
                    and not isinstance(entity_new_coords.get_last_superposer(), boxfile.Box):
                """ Player can't move more than 1 box """
                entity_new_coords.get_last_superposeable(True).superposer = box_instance

                box_instance.dx = (box_new_coords[1] - coords_box[1]) * mapper.measure["horizontal"]
                box_instance.dy = (box_new_coords[0] - coords_box[0]) * mapper.measure["vertical"]

                box_instance.update()

                box_instance.dx = 0
                box_instance.dy = 0
                return True

        return False

    @classmethod
    def get_instance_from_coords(cls, superposer, object_check):
        """Check if the last superposer is in object instance"""
        last_superposer = superposer.get_last_superposer()

        if isinstance(last_superposer, object_check):
            return last_superposer
        else:
            raise AttributeError("the last superposer of superposer is not instance of object_ckeck.")
