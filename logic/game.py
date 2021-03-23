import interface.menu
import logic.context
import logic.state
import logic.generate
import logic.player


class Game:
    state = logic.state.State


    def __init__(self):
        self.menu = interface.menu.Menu()
        self.context = logic.context.Context

    def config_context(self):
        "Set the context"""
        self.context.get_context()
        self.menu.screen = self.context.screen

    def start(self):
        """This is the function that start the game"""

        game_loop = True
        self.config_context()

        while game_loop:
            if self.state.state_go_back:
                self.state.go_back()
            elif self.state.next_state:
                self.state.leave_situation(1)
                self.state.next_state = False
            elif self.state.quit:
                game_loop = False
            else:
                self.context.screen.ask_command(self.menu)

                events = self.context.listener.listen_event()
                self.state.analizer(events, self.context.screen.textes)

                loading_conditions = self.state.situations[self.state.situation] == "select_difficult" and self.state.do_generate_levels
                loading_conditions = loading_conditions or self.state.situations[self.state.situation] == "select_versus_mode"

                if loading_conditions:
                    if self.state.do_generate_levels or self.state.versus is not None:
                        self.context.screen.clean_display()
                        self.context.screen.print_loading()
                        self.context.screen.refresh()

                    if self.state.do_generate_levels:
                        self.state.generate_levels()
                    if self.state.versus is not None:
                        self.state.select_game_traitment()

                if not self.state.quit:
                    self.context.screen.analize_state()
            self.context.screen.keep_fps()
        self.context.leave_context()
