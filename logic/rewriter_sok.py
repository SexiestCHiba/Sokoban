import os
import config.constants

class Overwrite:
    def writer(self, grid, a):
        """Overwrite a level consedering a giving grid and level number"""
        self.cpt = 0
        self.level = os.path.join(config.constants.BASE_DIR, "levels", f'level{a}.sok')
        with open(self.level, "w") as file:
            for i in range(len(grid)):
                for y in range(len(grid)):
                    file.write(grid[i][y])
                if i != len(grid) - 1:
                    file.write('\n')
