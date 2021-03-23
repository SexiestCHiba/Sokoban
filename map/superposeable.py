import typing

import map.entity
import map.moveable as moveablefile


class Superposeable(map.entity.Entity):

    def __init__(self, x, y, image, image_alternative=None):
        super(Superposeable, self).__init__(x, y, image, image_alternative)
        self._superposer: typing.Union[None, moveablefile.Moveable, Superposeable] = None

    @property
    def superposer(self) -> typing.Union[None, moveablefile.Moveable, "Superposeable"]:
        return self._superposer

    @superposer.setter
    def superposer(self, superposer: typing.Union[None, moveablefile.Moveable, "Superposeable"]) -> None:
        self._superposer = superposer

    @property
    def images(self) -> typing.List[str]:
        images = [self.image]

        superposers = self.get_superposers()

        for superposer in superposers:
            images.append(superposer.image)

        return images

    def get_last_superposeable(self, include_self=False) -> typing.Optional["Superposeable"]:
        superposeable: typing.Optional["Superposeable"]

        if issubclass(self.superposer.__class__, Superposeable):
            superposeable = self.superposer

            while issubclass(superposeable.__class__, Superposeable) and issubclass(superposeable.superposer.__class__,
                                                                                    Superposeable):
                superposeable = superposeable.superposer
        else:
            superposeable = None

        if superposeable is None and include_self:
            return self

        return superposeable

    def get_last_superposer(self, include_self=False) -> typing.Union[None, moveablefile.Moveable, "Superposeable"]:
        superposer = self.superposer
        while issubclass(superposer.__class__, Superposeable) and superposer.superposer is not None:
            superposer = superposer.superposer

        if superposer is None and include_self:
            return self

        return superposer

    def get_superposers(self, include_self=False) -> typing.List[typing.Union["Superposeable", moveablefile.Moveable]]:
        if self.superposer is None:
            if include_self:
                return [self]
            else:
                return []

        superposers: typing.List[
            typing.Union[
                "Superposeable",
                moveablefile.Moveable]
        ] = [self.superposer]

        superposer = superposers[0]
        while issubclass(superposer.__class__, Superposeable) and superposer.superposer is not None:
            superposer = superposer.superposer
            superposers.append(superposer)

        if include_self:
            return [self] + superposers
        else:
            return superposers
