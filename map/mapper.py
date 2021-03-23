import os
import typing

import pygame

import config.constants
import map.air as airfile
import map.box as boxfile
import map.dot as dotfile
import map.player as playerfile
import map.wall as wallfile


class Mapper:
    entities = (airfile.Air, boxfile.Box, playerfile.Player,
                wallfile.Wall, dotfile.Dot)

    def __init__(self, level_path: str, from_grid=None, with_load_image=True):
        self.level_path_file = os.path.join(
            config.constants.BASE_DIR, "levels", level_path)

        self._lines: int = 0
        self._columns: int = 0
        self._measure: dict = {}
        self.images = {}

        if from_grid is not None:
            self.grid_file = from_grid
        else:
            self.grid_file = self.create_grid_from_file()
            
        if with_load_image:
            self.load_images()

    def load_images(self):
        images_path = []

        for entity in self.entities:
            if entity.path_image not in images_path and entity.path_image:
                images_path.append(entity.path_image)

            if entity.path_imageAlternative not in images_path and entity.path_imageAlternative:
                images_path.append(entity.path_imageAlternative)

        for path in images_path:
            image = pygame.image.load(path).convert_alpha()
            self.images[path] = pygame.transform.scale(image,
                                                       (self.measure["horizontal"], self.measure["vertical"]))

    @property
    def measure(self):
        if not self._measure:
            self._measure = {
                "horizontal": config.constants.SIDE_WINDOW // self.length_of_column,
                "vertical": config.constants.SIDE_WINDOW // self.length_of_line
            }

        return self._measure

    def create_grid_from_file(self):
        """Creat the map"""
        grille = []

        with open(self.level_path_file, "r") as file_of_level:
            for line in file_of_level:
                liste = []

                for letter in line:
                    if letter != "\n":
                        liste.append(letter)

                grille.append(liste)

        return grille

    def coords_in_map(self, coords: typing.Tuple):
        return (0 <= coords[0] <= self.length_of_line - 1) and (0 <= coords[1] <= self.length_of_column - 1)

    @property
    def length_of_column(self):
        if self._columns != 0:
            return self._columns

        self._columns = 0
        for line in self.grid_file:
            if len(line) > self._columns:
                self._columns = len(line)
        return self._columns

    @property
    def length_of_line(self):
        if self._lines != 0:
            return self._lines

        self._lines = len(self.grid_file)
        return self._lines

    def get_file_letter(self, _line: int, _column: int):
        try:
            letter = self.grid_file[_line][_column]
            return letter
        except IndexError:
            return "#"
