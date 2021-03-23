import typing

import pygame

import logic.mover
import logic.searcher
import map.box
import map.moveable
import map.moveable as movfile


class Player:
    def __init__(self, entity_mapper):
        self.entity_mapper = entity_mapper
        self.full_path = None
        self.full_path_temoin = []

        self.position = logic.searcher.Searcher.get_coords_player_from_map(self.entity_mapper.grid_of_sprites)
        self.position_start = self.position[:]
        self.direction: typing.Optional[map.moveable.DIRECTION] = None

        self.blow_counter = 0

        self.restarted = False
        self.wanted_move = False
        self.had_moved = False
        self.interrupt = False

        if self.entity_mapper.position == 1:
            self.inputs = ["left", "right", "up", "down", 'p']
            self.direction_association = None
        else:
            self.inputs = ["q", "d", "z", "s", 'o']
            self.direction_association = dict(zip(self.inputs, ["left", "right", "up", "down"]))

    def player_analizer(self, event):
        """Check if the player want to restart the game. Then move the player using the 'move' function"""
        if self.interrupt:
            return None

        if event.key == pygame.K_o and self.entity_mapper.position == 0:
            self.restart_player_game()
        elif event.key == pygame.K_p and self.entity_mapper.position == 1:
            self.restart_player_game()
        elif self.direction is None:
            key_direction = ""
        
            if self.entity_mapper.position == 0:
                str_key = event.unicode.lower()
                try:
                    key_direction = self.direction_association[str_key].upper()
                except KeyError:
                    return None
            else:
                for direction in ("left", "right", "up", "down"):
                    if event.key == getattr(pygame, "K_" + direction.upper()):
                        key_direction = direction.upper()
                        break

            direction_enum = getattr(movfile.DIRECTION, key_direction, None)
            if direction_enum is not None:
                self.direction = direction_enum
                self.move()

    def move(self):
        """If the player want to move, the he moves (if the movement is possible) 
        and the blow_counter is increamentedby 1. If the player has win the his part of the screen is 
        interrupt"""
        if self.direction is not None:
            self.wanted_move = True
            if logic.mover.Mover.move_player(self, self.direction):
                self.had_moved = True
                self.blow_counter += 1
                if self.has_win():
                    self.interrupt = True

            self.direction = None

    def move_from_full_path(self):
        """Move the computer considering a full path accross the grid"""
        if self.full_path:
            self.direction = self.full_path.pop(0)
            self.move()

    def reset_status(self):
        """Reset the player statuts 'wanted_move' and 'had_moved' """
        self.wanted_move = False
        self.had_moved = False

    def restart_player_game(self):
        """Restart the player game (the first or the second one, independently of the other one)"""
        self.restarted = True
        self.entity_mapper.re_map()
        self.entity_mapper.update_sprites()
        self.position = self.position_start
        self.interrupt = False
        self.blow_counter = 0

    def has_win(self):
        """Return True if a player win the game(boxs are superposed
         with all validation dots), else return False"""
        dots_coords = logic.searcher.Searcher.get_coords_dots_from_map(self.entity_mapper.grid_of_sprites)
        for dot_coords in dots_coords:
            if not isinstance(self.entity_mapper.grid_of_sprites[dot_coords[0]][dot_coords[1]].get_last_superposer(),
                              map.box.Box):
                return False
        return True
