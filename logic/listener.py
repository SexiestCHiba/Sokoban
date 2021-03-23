import typing
import pygame


class Listener:
    azerty_conversion = {"K_w": ["K_z"], "K_z": ["K_w"], "K_a": ["K_q"], "K_q": ["K_a"]}

    @classmethod
    def clean(cls):
        """Clean the pygame's event list"""
        pygame.event.clear()

    @classmethod
    def listen_event(cls):
        """Create a list name 'events' and fill it with all the keys the user type during the game"""

        events = []
        for event in pygame.event.get():
            if hasattr(event, "key"):
                for azerty_key in cls.azerty_conversion.keys():
                    if event.key == getattr(pygame, azerty_key):
                        event.key = getattr(pygame, cls.azerty_conversion[azerty_key][0], None)
                        break

            events.append(event)

        return events
