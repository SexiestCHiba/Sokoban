import typing

import interface.screen
import logic.listener


class Context:
    screen: interface.screen.Screen
    listener: typing.Type[logic.listener.Listener]
    type: str

    pygame_launched: bool = False

    @classmethod
    def get_context(cls):
        """Get the actual context (what's in the screen, in the listener) and store it in the 'Context' class"""
        cls.screen = interface.screen.Screen()
        cls.screen.start()
        cls.screen.init()
        cls.listener = logic.listener.Listener
        cls.type = "pygame"

    @classmethod
    def leave_context(cls):
        """Leave the actual context"""
        try:
            if cls.type == "pygame":
                cls.listener.clean()
                cls.screen.close()
                if cls.pygame_launched:
                    cls.screen.stop()
                    cls.pygame_launched = False
        except KeyError:
            pass
        return None
