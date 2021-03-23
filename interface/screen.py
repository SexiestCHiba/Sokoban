import typing

import pygame
import pygame.locals as pg_var

import config.constants
import interface.goback
import interface.texte
import logic.state


class Screen:
    _init = False
    state = logic.state.State

    def __init__(self):
        self.clock = None
        self.display = None
        self.printer_surface = None
        self.printer_left = None
        self.printer_right = None
        self.surface_game = None
        self.font = None

        self.textes = pygame.sprite.Group()

    def init(self, ratio_x=1):
        """Inintialize the game window, creating areas were we can print 
        content. The font is also set"""
        if not self._init:
            self.clock = pygame.time.Clock()
            # initialization of the main display
            width_display = config.constants.SIDE_WINDOW * ratio_x
            self.display = pygame.display.set_mode(
                (width_display,
                 config.constants.SIDE_WINDOW + config.constants.PRINTER_SURFACE_HEIGHT * 2))
            pygame.display.set_caption(config.constants.TITLE_WINDOW)

            # initialization of the subwindows with its width and height
            self.printer_surface = pygame.Surface((width_display, config.constants.PRINTER_SURFACE_HEIGHT))

            self.printer_left = pygame.Surface((width_display // 2, config.constants.PRINTER_SURFACE_HEIGHT))
            self.printer_right = pygame.Surface((width_display // 2, config.constants.PRINTER_SURFACE_HEIGHT))

            self.surface_game = pygame.Surface((width_display, config.constants.SIDE_WINDOW))

            self.font = pygame.font.SysFont("arial", int(config.constants.SIDE_WINDOW * 0.04))
            pygame.key.set_repeat(400,100)

    def blit_surface_game(self):
        """Set the position of the game surface created above"""
        self.display.blit(self.surface_game, (0, config.constants.PRINTER_SURFACE_HEIGHT * 2))

    def blit_printer_surface(self):
        """Set the position of the printer surface (were we show informations like the number of strokes)
         created above"""
        self.display.blit(self.printer_surface, (0, 0))

    def blit_printer_left(self):
        """Set the position of the left display surface created above"""
        self.display.blit(self.printer_left, (0, config.constants.PRINTER_SURFACE_HEIGHT))

    def blit_printer_right(self):
        """Set the position of the right display surface created above"""
        self.display.blit(self.printer_right, (config.constants.SIDE_WINDOW, config.constants.PRINTER_SURFACE_HEIGHT))

    def refresh(self):
        """Refresh the screen"""
        pygame.display.flip()

    def close(self):
        """Enable to close the window"""
        pygame.key.set_repeat(0, 0)
        pygame.display.quit()

    def wait(self, ms):
        """Freeze the screen for a certain duration"""
        pygame.time.wait(ms)

    def start(self):
        """Enable to start the game"""
        pygame.init()

    def stop(self):
        """Enable to end the game"""
        pygame.quit()

    def clean_display(self):
        """Fill the display with black (clean it)"""
        self.display.fill(pg_var.color.THECOLORS['black'])

    def clean_printer_surface(self):
        """Fill the printer surface with black (clean it)"""
        self.printer_surface.fill(pg_var.color.THECOLORS['black'])

    def clean_printer_left(self):
        """Fill the printer left surface with black (clean it)"""
        self.printer_left.fill(pg_var.color.THECOLORS['black'])

    def clean_printer_right(self):
        """Fill the printer right surface with black (clean it)"""
        self.printer_right.fill(pg_var.color.THECOLORS['black'])

    def clean_surface_game(self):
        """Fill the game surface with black (clean it)"""
        self.surface_game.fill(pg_var.color.THECOLORS['black'])

    def draw_sprites_on_surface_game(self, sprites_group):
        """Enable to show a group of sprites on the screen"""
        for sprite in sprites_group.sprites():
            sprite.draw(self.surface_game)

        self.blit_surface_game()
        self.refresh()

    def print_sentence_on_display(self, question: str, coord_x: typing.Optional[int] = None,
                                  coord_y: typing.Optional[int] = None):
        """Enable to print a sentence on the display surface considering some coordinates"""
        self.textes.empty()
        for line in question.splitlines():
            if coord_x is not None and coord_y is not None:
                params = (coord_x, coord_y)
            else:
                params = (self.display.get_rect().centerx // 2, self.display.get_rect().centery // 2)
            text = interface.texte.Texte(self.font, line, *params)
            self.textes.add(text)

        for i, text in enumerate(self.textes.sprites()):
            text.dy = 30 * i
            text.update()
            text.dy = 0
            self.display.blit(text.image, text.rect)

    def print_sentence_on_surface_printer(self, sentence: str, coord_x: typing.Optional[int] = None,
                                          coord_y: typing.Optional[int] = None):
        """Enable to print a sentence on the printer surface considering some coordinates"""
        self.print_sentence_on_printer(self.printer_surface, sentence, coord_x, coord_y)
        self.blit_printer_surface()

    def print_sentence_on_printer_left(self, sentence: str, coord_x: typing.Optional[int] = None,
                                       coord_y: typing.Optional[int] = None):
        """Enable to print a sentence on the left printer surface considering some coordinates"""
        self.print_sentence_on_printer(self.printer_left, sentence, coord_x, coord_y)
        self.blit_printer_left()

    def print_sentence_on_printer_right(self, sentence: str, coord_x: typing.Optional[int] = None,
                                        coord_y: typing.Optional[int] = None):
        """Enable to print a sentence on the right printer surface considering some coordinates"""
        self.print_sentence_on_printer(self.printer_right, sentence, coord_x, coord_y)
        self.blit_printer_right()

    def print_sentence_on_printer(self, surface, sentence: str, coord_x: typing.Optional[int] = None,
                                  coord_y: typing.Optional[int] = None):
        """Enable to print a sentence on the printer surface considering some coordinates"""

        self.textes.empty()
        if coord_x is not None and coord_y is not None:
            params = (coord_x, coord_y)
        else:
            params = (surface.get_rect().centerx // 2, surface.get_rect().centery // 2)
        text = interface.texte.Texte(self.font, sentence, *params)
        self.textes.add(text)

        for i, text in enumerate(self.textes.sprites()):
            text.dy = 30 * i
            text.update()
            text.dy = 0
            surface.blit(text.image, text.rect)

    def add_goback(self):
        """Print the goback arrow on the screen that allows the player to go back in the menu
        (this arrow is a sprite already created in interface/goback.Goback)"""
        goback = interface.goback.GoBack(100, 100)
        self.textes.add(goback)
        self.display.blit(goback.image, goback.rect)

    def print_loading(self):
        """Print a "loading" message in the display surface when the game is loading (using 
        the 'print_sentence_on_display' function"""
        self.print_sentence_on_display("Loading...")
        self.refresh()

    def ask_command(self, menu):
        """Clean the screen and move in the menu depending on the program state (see "state.py")"""
        if self.state.situations[self.state.situation] == "select_difficult":
            self.clean_display()
            menu.get_difficulty()
            self.add_goback()
        elif self.state.situations[self.state.situation] == "select_level":
            self.clean_display()
            menu.get_map_file(self.state.difficulty)
            self.add_goback()
        elif self.state.situations[self.state.situation] == "select_versus_mode":
            self.clean_display()
            menu.get_versus_mode()
            self.add_goback()
        elif self.state.situations[self.state.situation] == "game":
            pass

        self.refresh()

    def analize_state(self):
        """Print a message depending on the program state (see "state.py")"""
        if self.state.situations[self.state.situation] == "select_versus_mode" and self.state.next_state:
            self.close()
            self.init(2)
            for player in self.state.players:
                self.draw_sprites_on_surface_game(player.entity_mapper.sprites)
            self.refresh()
        elif self.state.situations[self.state.situation] == "game":
            self.game_traitment()            
            if self.state.next_state:
                for player in self.state.players:
                    self.draw_sprites_on_surface_game(player.entity_mapper.sprites)

                if self.state.players[0].blow_counter > self.state.players[1].blow_counter:
                    sentence_win = "Player 2 has win."
                    if self.state.versus == "a":
                        sentence_win = "Computer has win."                
                elif self.state.players[1].blow_counter > self.state.players[0].blow_counter:
                    sentence_win = "Player 1 has win."
                else:
                    sentence_win = "Equality"
                self.print_sentence_on_surface_printer(sentence_win)
                self.refresh()
                self.wait(2000)
            if self.state.next_state or self.state.state_go_back:
                self.close()
                self.init(1)

    def game_traitment(self):
        """Print on the screen the numbers of strokes and the "impossible movement" message
        if the movement the player want to do is impossible"""
        for player in self.state.players:
            if player.wanted_move and player.had_moved or player.restarted:
                if player.entity_mapper.position == 0:
                    self.clean_printer_left()
                    self.print_sentence_on_printer_left(str(player.blow_counter) + " stroke(s)", 80, 0)
                else:
                    self.clean_printer_right()
                    self.print_sentence_on_printer_right(str(player.blow_counter) + " stroke(s)", 80, 0)
            elif player.wanted_move and not player.had_moved:
                if player.entity_mapper.position == 0:
                    self.print_sentence_on_printer_left("impossible movement", 240, 0)
                else:
                    self.print_sentence_on_printer_right("impossible movement", 240, 0)
            self.draw_sprites_on_surface_game(player.entity_mapper.sprites)
            self.refresh()

    def keep_fps(self):
        """A limit to force the computer staying at a refresh rate <= 20 fps"""
        self.clock.tick(config.constants.FPS)