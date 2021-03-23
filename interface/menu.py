import typing
import interface.screen


class Menu:
    def __init__(self):
        self.screen: typing.Type[interface.screen.Screen]
        self.difficulty = None
        self.map_file = None

    def get_difficulty(self):
        """Enable to show and choose a level difficulty"""
        self.screen.print_sentence_on_display(
            "Welcome to Sokoban !\nPlease select the game difficulty:\nB : Beginner\nC : Casual \nE : Elite\nA : Random\nG : Generate levels")

    def get_versus_mode(self):
        """Enable to choose your game mode (versus the computer or versus another player"""
        self.screen.print_sentence_on_display(
            "Choose your versus mode :\nA : Versus Computer\nB : Versus Player")

    def ask_exit(self):
        """A confirmation to close the program"""
        self.screen.print_sentence_on_display("Close the program ? (0/1) ")

    def get_map_file(self, difficulty: typing.Optional[str]):
        """Verify if the difficulty selected exists and then, depending on the difficulty selected, lead to the level selection"""
        if difficulty not in ("b", "c", "e", "a"):
            raise Exception("Unknown difficulty : " + difficulty)

        if difficulty == "b":
            self.screen.print_sentence_on_display("A newbie !\n Now select your level :"
                                      " \n1 : level 1 \n2 : level 2\n3 : level 3\n")
        if difficulty == "c":
            self.screen.print_sentence_on_display(
                "So that's not your first game....\n Now select your level :"
                " \n 4 : level 4 \n 5 : level 5\n 6 : level 6")
        if difficulty == "e":
            self.screen.print_sentence_on_display("Hell begins !\n Now select your level :"
                                      " \n7 : level 7 \n8 : level 8\n9 : level 9")
        if difficulty == "a":
            self.screen.print_sentence_on_display("Hell begins !\nChoose the number of box.\nEnter a number\nbeetween 1 and 9")
