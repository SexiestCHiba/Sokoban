import config.constants
import typing
import pygame

import logic.player
import logic.keyboardTools
import logic.generate
import logic.rewriter_sok

import solver.solver
import solver.pathNotFoundException

import map.entity_mapper as entity_mapper
import map.mapper as mapper

import interface.goback


class State:
    quit = False
    next_state = False
    state_go_back = False
    versus = None
    do_generate_levels = False
    dicGen = {"1": [8, 8, 2, 3, 1], "2": [9, 9, 3, 4, 2], "3": [10, 10, 4, 5, 2], "4": [15, 15, 6, 7, 2], "5": [
        17, 17, 7, 8, 2], "6": [18, 18, 8, 9, 1], "7": [20, 20, 6, 7, 2], "8": [25, 25, 7, 8, 3], "9": [30, 30, 7, 10, 4]}

    difficulty: typing.Union[str, None] = None
    level: typing.Union[int, str, None] = None
    players: typing.List[logic.player.Player] = []

    situations = ('select_difficult', 'select_level', 'select_versus_mode', 'game')
    situation = 0

    inputs = {
        "option_menu_difficulty": logic.keyboardTools.KeyboardTools.get_keys_event_from_choices(['g']),
        "difficulty": logic.keyboardTools.KeyboardTools.get_keys_event_from_choices(['a', 'b', 'c', 'e']),
        "levels": {
            'a': logic.keyboardTools.KeyboardTools.get_keys_event_from_range(1, 9),
            'b': logic.keyboardTools.KeyboardTools.get_keys_event_from_range(1, 3),
            'c': logic.keyboardTools.KeyboardTools.get_keys_event_from_range(4, 6),
            'e': logic.keyboardTools.KeyboardTools.get_keys_event_from_range(7, 9)
        },
        "versus": logic.keyboardTools.KeyboardTools.get_keys_event_from_choices(['a', 'b']),
    }

    @classmethod
    def inputs_checker(cls, event, valid_inputs):
        """Check if the key the player press is valid or not"""
        for valid_input in valid_inputs:
            if event.key == getattr(pygame, valid_input) \
                    or (getattr(event, "unicode", None) and event.unicode.lower() == logic.keyboardTools.KeyboardTools.get_str_from_keyboard_event(valid_input).lower()):
                return True
        return False

    @classmethod
    def analizer(cls, events: list, textes=None):
        """Analize the events and modify the state class's variables in consequence"""
        for event in events:
            if event.type == pygame.QUIT:
                cls.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cls.state_go_back = True
                else:
                    if not cls.analizer_menu(event):
                        cls.analizer_game(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                cls.analizer_menu_mouse(event, textes)
            elif event.type == config.constants.COMPUTER_EVENT:
                cls.analizer_game_from_computer()

    @classmethod
    def get_letter_pointed_from_mouse(cls, event, textes, attr):
        """Change the variables "state_go_back" and "next_state" according to what the mouse is pointing at"""
        for texte in textes:
            if texte.rect.collidepoint(event.pos):
                if isinstance(texte, interface.goback.GoBack):
                    cls.state_go_back = True
                    break
                elif ':' in texte.texte:
                    command = texte.texte.split(":")[0].lower().strip()
                    command_pygame_key = logic.keyboardTools.KeyboardTools.get_keys_event_from_choices([command])[0]
                    if command_pygame_key in cls.inputs["option_menu_difficulty"]:
                        cls.do_generate_levels = True
                    else:
                        setattr(cls, attr, command)
                        cls.next_state = True
                    break

    @classmethod
    def analizer_menu_mouse(cls, event, textes):
        """Enable the player to choose a level and a game difficulty in the menu with the mouse pointer"""
        if cls.situations[cls.situation][:6] != "select":
            return False

        if cls.difficulty is None:
            cls.get_letter_pointed_from_mouse(event, textes, "difficulty")
        elif cls.level is None:
            for texte in textes:
                if texte.rect.collidepoint(event.pos):
                    if isinstance(texte, interface.goback.GoBack):
                        cls.state_go_back = True
                        break
                    elif ':' in texte.texte:
                        try:
                            integer = int(texte.texte.split(":")[0].strip().lower()[-1])
                            cls.level = integer
                            cls.next_state = True
                        except ValueError:
                            pass
                        except IndexError:
                            pass
        elif cls.versus is None:
            cls.get_letter_pointed_from_mouse(event, textes, "versus")

        return True

    @classmethod
    def get_unicode_letter_for_situation(cls, event, input_sector, attr):
        """Return the unicode of a given letter and make the 'next_state' variable True """
        if cls.inputs_checker(event, cls.inputs[input_sector]):
            integer = logic.keyboardTools.KeyboardTools.check_integer_keyboard(
                event.unicode)
            if integer is None:
                if event.unicode.isalpha():
                    setattr(cls, attr, event.unicode.lower())
                    cls.next_state = True

    @classmethod
    def analizer_menu(cls, event):
        """Movidifed the State class considering what the player choose in the menu interface"""
        if cls.situations[cls.situation][:6] != "select":
            return False
        if cls.difficulty is None:
            if cls.inputs_checker(event, cls.inputs["option_menu_difficulty"]):
                cls.do_generate_levels = True
            else:
                cls.get_unicode_letter_for_situation(event, "difficulty", "difficulty")
        elif cls.level is None:
            if cls.inputs_checker(event, cls.inputs['levels'][cls.difficulty]):
                integer = logic.keyboardTools.KeyboardTools.check_integer_keyboard(
                    event.unicode)
                if integer is not None:
                    cls.level = integer
                    cls.next_state = True
        elif cls.versus is None:
            cls.get_unicode_letter_for_situation(event, "versus", "versus")
        return True

    @classmethod
    def generate_grids_for_levels(cls):
        """Call the Generate class to create a random level according to the parameters we
        decided for each level difficulty (in the dicGen dictionnary)"""
        i = 1
        while i <= 9:
            grid = logic.generate.Generate.gridGen(
                    cls.dicGen[str(i)][0],
                    cls.dicGen[str(i)][1],
                    cls.dicGen[str(i)][2],
                    cls.dicGen[str(i)][3],
                    cls.dicGen[str(i)][4])

            _mapper = mapper.Mapper("", grid)
            _player = logic.player.Player(entity_mapper.EntityMapper(_mapper, i, initsprites=False))
            _solver = solver.solver.Solver(_player)

            try:
                _solver.get_full_path()
                yield grid
            except solver.pathNotFoundException.Path_not_found_exception:
                i -= 1

            i += 1

    @classmethod
    def generate_levels(cls):
        """Call the Overwrite class to erase all the levels existing and replace them by random generated levels"""
        overwriter = logic.rewriter_sok.Overwrite()
        grids = [grid for grid in cls.generate_grids_for_levels()]
        for i, grid in enumerate(grids, start=1):
            overwriter.writer(grid, str(i))
        cls.do_generate_levels = False

    @classmethod
    def analizer_game(cls, event):
        """This fonction analize all the player's actions during a game and act consequently"""
        if cls.situations[cls.situation] != "game":
            return False

        for player in cls.players: 
            cls.game_traitment(player)
            if player.inputs:
                valid_inputs = logic.keyboardTools.KeyboardTools.get_keys_event_from_choices(
                    player.inputs)
                if cls.inputs_checker(event, valid_inputs):
                    player.player_analizer(event)
            if cls.versus == "a" and event.key == pygame.K_o and player.entity_mapper.position == 1:
                player.restart_player_game()

        if cls.versus == "a" and any((player.had_moved for player in cls.players)):
            cls.analizer_game_from_computer()
            if cls.players[0].interrupt and not cls.players[1].interrupt:
                pygame.time.set_timer(config.constants.COMPUTER_EVENT, 500)

        if all((player.interrupt for player in cls.players)):
            cls.next_state = True
        return True

    @classmethod
    def analizer_game_from_computer(cls):
        """All the computer to finish the game alone if the player beats him"""
        if cls.situations[cls.situation] != "game":
            return False

        cls.game_traitment(cls.players[1])
        cls.players[1].move_from_full_path()

        if cls.players[0].interrupt:
            if all((player.interrupt for player in cls.players)):
                cls.next_state = True
        
        return True

    @classmethod
    def go_back(cls):
        """Make the game one step back """
        cls.leave_situation(-1)
        if cls.situation < 0:
            cls.situation = 0
            cls.quit = True
        
        if not cls.situations[cls.situation] == "select_versus_mode":
            cls.state_go_back = False

    @classmethod
    def leave_situation(cls, direction):
        """Change the situation variable 'situation' to change the 'cls.situations[cls.situations]' value.
        Also impact the 'level', 'difficulty', and 'versus' vraibles"""
        if cls.situations[cls.situation] == "select_level":
            if direction == -1:
                cls.level = None
                cls.difficulty = None
        elif cls.situations[cls.situation] == "select_versus_mode":
            if direction == -1:
                cls.versus = None
                cls.level = None
        elif cls.situations[cls.situation] == "game":
            for player in cls.players:
                player.entity_mapper.sprites.empty()
            cls.players.clear()

            if cls.versus == "a":
                pygame.time.set_timer(config.constants.COMPUTER_EVENT, 0)

            if direction == 1:
                cls.level = None
                cls.difficulty = None
                cls.versus = None

        if direction == -1:
            cls.situation -= 1
        else:
            cls.situation = (cls.situation + 1) % len(cls.situations)

    @classmethod
    def generate_players(cls):
        """"""
        for player in cls.players:
            player.entity_mapper.sprites.empty()
        cls.players.clear()

        if cls.difficulty == "a" and cls.level is not None:
            grid = logic.generate.Generate.gridGen(
                cls.dicGen[str(cls.level)][0],
                cls.dicGen[str(cls.level)][1],
                cls.dicGen[str(cls.level)][2],
                cls.dicGen[str(cls.level)][3],
                cls.dicGen[str(cls.level)][4]
            )

            _mapper = mapper.Mapper("", grid)
        elif cls.level is not None:
            _mapper = mapper.Mapper("level" + str(cls.level) + ".sok")

        if cls.level is not None:
            for i in range(2):
                _player = logic.player.Player(
                    entity_mapper.EntityMapper(_mapper, i))
                cls.players.append(_player)

    @classmethod
    def select_game_traitment(cls):
        """"""
        cls.generate_players()
        if cls.versus == "a" and cls.players:
            while True:
                cls.players[1].inputs = []
                _solver = solver.solver.Solver(cls.players[1])
                if cls.difficulty == "a":
                    try:
                        _solver.get_full_path()
                        break
                    except solver.pathNotFoundException.Path_not_found_exception:
                        cls.generate_players()
                        continue
                else:
                    try:
                        _solver.get_full_path()
                        break
                    except solver.pathNotFoundException.Path_not_found_exception:
                        cls.next_state = True

        cls.next_state = True

    @classmethod
    def game_traitment(cls, player):
        """Reset the player statuts"""
        if player.restarted:
            player.restarted = False
            if player.full_path_temoin:
                player.full_path = player.full_path_temoin[:]

        player.reset_status()
