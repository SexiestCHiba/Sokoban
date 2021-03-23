from random import randrange as r
import map.air
import map.box
import map.dot
import map.player
import map.wall

class Generate:

    """Declaring variables that will be used several times in the Generate class"""
    grid = []
    coordb = {}
    coordh = {}
    coordp = {}
    size = 0

    @classmethod
    def base(cls,minsize,maxsize):
        """Create an empty grid"""

        cls.grid = []
        cls.coordb = {}
        cls.coordh = {}
        cls.coordp = {}
        cls.size = r(minsize,maxsize+1)

        for i in range(cls.size):
            cls.grid.append([])

        for i in range(cls.size):
            cls.grid[0].insert(i,map.wall.Wall._character)
            cls.grid[cls.size-1].insert(i,map.wall.Wall._character)

        for i in range(1,cls.size-1):
            for z in range(1,cls.size-1):
                cls.grid[i].insert(z,map.air.Air._character)

        for i in range(1,cls.size-1):
            cls.grid[i].insert(0,map.wall.Wall._character)
            cls.grid[i].insert(cls.size-1,map.wall.Wall._character)


    @classmethod
    def fill(cls,difficulty,minb,maxb):
        """Fill the empty grid created above with randoms probabilities"""
        holes = 0
        boxes = r(minb,maxb+1)
        size = len(cls.grid)

        x = r(2,size-3)
        y = r(2,size-3)
        cls.grid[x][y] = map.player.Player._character
        cls.coordp["player"] = [x,y]

        if size%2 == 0:
            wall = size/2
        else:
            wall = (size-1)/2
        wall = wall*difficulty

        while wall != 0:
            x = r(1,size-1)
            y = r(1,size-1)
            if cls.grid[x][y] != map.player.Player._character:
                cls.grid[x][y] = map.wall.Wall._character
                wall -= 1

        cpt = 0
        while boxes != 0:
            x = r(2,size-3)
            y = r(2,size-3)
            if cls.grid[x][y] != map.player.Player._character and cls.grid[x][y] != map.wall.Wall._character:
                cls.grid[x][y] = map.box.Box._character
                cpt +=1
                cls.dicFill(x,y,cpt,2)
                boxes -= 1
                holes += 1

        cpt = 0
        while holes != 0:
            x = r(2,size-3)
            y = r(2,size-3)
            if cls.grid[x][y] != map.player.Player._character and cls.grid[x][y] != map.wall.Wall._character and cls.grid[x][y] != map.box.Box._character:
                cls.grid[x][y] = map.dot.Dot._character
                cpt += 1
                cls.dicFill(x,y,cpt,3)
                holes -= 1

    @classmethod
    def dicFill(cls,x,y,cpt,a):
        """Fill the boxes and holes dictionnaries (easier to get their positions after)"""

        if a == 2:
            box = 'box'+str(cpt) 
            cls.coordb[box] = [x,y]
        if a == 3:
            hole = 'hole'+str(cpt) 
            cls.coordh[hole] = [x,y]

    @classmethod
    def verify(cls,minb):
        """Check if the grid is playable"""

        cptb = 0
        cpth = 0
        cptp = 0
        for i in range(len(cls.grid)):
            for y in range(len(cls.grid)):
                if cls.grid[i][y] == map.box.Box._character:
                    cptb += 1
                if cls.grid[i][y] == map.dot.Dot._character:
                    cpth += 1
                if cls.grid[i][y] == map.player.Player._character:
                    cptp += 1

        if cptp != 1:
            return False

        if cpth != cptb:
            return False

        if minb > cptb:
            return False

        if cls.verifAround(map.wall.Wall._character,cls.coordb) == False:
            return False

        if cls.verifAround(map.wall.Wall._character,cls.coordb,2) == False:
            return False

        if cls.verifAround(map.wall.Wall._character,cls.coordh) == False:
            return False
        
        if cls.verifAround(map.wall.Wall._character,cls.coordp) == False:
            return False
    
        cls.verifAir()

        return True

    @classmethod
    def verifAir(cls):
        """Check if there's an air place surrounded by walls"""
        for x in range(len(cls.grid)):
            for y in range(len(cls.grid[x])):
                if cls.grid[x][y] == map.air.Air._character:
                    cpt = 0
                    if cls.grid[x][y+1] == map.wall.Wall._character:
                        cpt += 1
                    if cls.grid[x][y-1] == map.wall.Wall._character:
                        cpt += 1
                    if cls.grid[x+1][y] == map.wall.Wall._character:
                        cpt += 1
                    if cls.grid[x-1][y] == map.wall.Wall._character:
                        cpt += 1
                    if cpt == 4:
                        cls.grid[x][y] = map.wall.Wall._character

    @classmethod
    def verifAround(cls,char,d,rng=1):
        """Check if a box or a hole is surrounded by walls"""

        cpt = 0
        for i in d.values():
            x = i[0]
            y = i[1]
            if cls.grid[x][y+rng] == char:
                cpt += 1
            if cls.grid[x][y-rng] == char:
                cpt += 1
            if cls.grid[x+rng][y] == char:
                cpt += 1
            if cls.grid[x+rng][y+rng] == char:
                    cpt += 1
            if cls.grid[x+rng][y-rng] == char:
                cpt += 1
            if cls.grid[x-rng][y] == char:
                cpt += 1
            if cls.grid[x-rng][y+rng] == char:
                    cpt += 1
            if cls.grid[x-rng][y-rng] == char:
                cpt += 1
            if cpt > 1 : 
                return False
        return True

    @classmethod
    def gridGen(cls,minsize,maxsize,minb,maxb,difficulty):
        """The main function of the class which return a random generated grid"""
        c = False
        while c == False:
            cls.base(minsize,maxsize)
            cls.fill(difficulty,minb,maxb)
            c = cls.verify(minb)
        return cls.grid

