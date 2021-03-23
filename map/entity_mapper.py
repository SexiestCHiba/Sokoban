import typing

import config.constants
import pygame

import map.air as airfile
import map.dot as dotfile
import map.moveable as moveablefile
import map.wall as wallfile


class EntityMapper:
    def __init__(self, mapper, position, initsprites=True):
        self.mapper = mapper
        self.position = position
        self.grid_of_sprites = self.create_map()

        if initsprites:
            self.sprites = None
            self.update_sprites()

    def create_map(self) -> typing.List[typing.List]:
        """Creat the map"""
        grille = []
        i = 0
        while i <= self.mapper.length_of_line - 1:
            liste = []

            j = 0
            while j <= self.mapper.length_of_column - 1:
                letter = self.mapper.get_file_letter(i, j)
                entity = self.get_instance_entity_from_letter(letter, (i, j))
                liste.append(entity)
                j += 1

            grille.append(liste)
            i += 1

        return grille

    def re_map(self):
        self.grid_of_sprites = self.create_map()

    def update_sprites(self):
        if self.sprites is not None:
            self.sprites.empty()

        self.sprites = pygame.sprite.Group()
        for line in self.grid_of_sprites:
            for sprite in line:
                sprite.dx = config.constants.SIDE_WINDOW * self.position
                sprite.update()
                sprite.dx = 0
                self.sprites.add(sprite)

    def get_instance_entity_from_letter(self, letter: str, coords: typing.Tuple) -> \
            typing.Union[wallfile.Wall, airfile.Air]:
        for entity in self.mapper.entities:
            param_entity = self.get_init_param_for_sprites(entity, *coords)
            instance_entity = entity(*param_entity)

            if instance_entity.character == letter:
                if issubclass(entity, moveablefile.Moveable) or isinstance(instance_entity, dotfile.Dot):
                    param_air = self.get_init_param_for_sprites(airfile.Air, *coords)
                    air = airfile.Air(*param_air)
                    air.superposer = instance_entity
                    return air
                else:
                    return instance_entity
            elif instance_entity.alternativeCharacter == letter:
                if not issubclass(entity, moveablefile.Moveable):
                    raise ValueError("The entity is not recognized")
                param_air = self.get_init_param_for_sprites(airfile.Air, *coords)
                param_dot = self.get_init_param_for_sprites(dotfile.Dot, *coords)

                air = airfile.Air(*param_air)
                dot = dotfile.Dot(*param_dot)
                dot.superposer = instance_entity

                air.superposer = dot
                return air

        raise ValueError("The letter: " + str(letter) + " is not associated to a entity.")

    def get_init_param_for_sprites(self, entity, line, column) -> typing.List:
        params = [column * self.mapper.measure["horizontal"], line * self.mapper.measure["vertical"],
                  self.mapper.images[entity.path_image]]

        if entity.path_imageAlternative:
            params.append(self.mapper.images[entity.path_imageAlternative])

        return params
