import constraint as c

class Location:
    def __init__(self, x, y, letter_multiplier, word_multiplier):
        self.letter_multiplier = letter_multiplier
        self.word_multiplier = word_multiplier
        self.x = x
        self.y = y
        self.tile = None
    
    def __repr__(self):
        if self.tile is None:
            if self.letter_multiplier == 2:
                return "|DL"
            elif self.letter_multiplier == 3:
                return "|TL"
            elif self.word_multiplier == 2:
                return "|DW"
            elif self.word_multiplier == 3:
                return "|TW"
            else:
                return "|  "
        else:
            return "|" + str(self.tile) + " "

    def setLetterMultiplier(self, val):
        self.letter_multiplier = val

    def setWordMultiplier(self, val):
        self.word_multiplier = val
    def copyLocation(self, otherLoc):
        self.word_multiplier = otherLoc.word_multiplier
        self.letter_multiplier = otherLoc.letter_multiplier
 
    def resetMultiplier(self, val):
        self.letter_multiplier = 1
        self.word_multiplier = 1
    
    def setTileLetter(self, tile):
        self.tile = tile

class Board:
    def __init__(self):
        self.width = 15
        self.height = 15
        self.board = []
        for _ in xrange(self.width):
            self.board += [ [] ]
        self._generateBoard()     
     
    def _generateBoard(self):
        for x in range(self.width):
            for y in range(self.height):
                letter_mul = 1
                word_mul = 1

                newLocation = Location(x, y, letter_mul, word_mul)
                self.board[x] += [newLocation]

        # Middle rows/columns
        mid = self.width // 2
        self.board[mid][0].setWordMultiplier(3)
        self.board[mid][3].setLetterMultiplier(2)
        self.board[mid][self.height - 1].setWordMultiplier(3)
        self.board[mid][self.height - 1 - 3].setLetterMultiplier(2)
        self.board[0][mid].setWordMultiplier(3)
        self.board[3][mid].setLetterMultiplier(2)
        self.board[self.width - 1][mid].setWordMultiplier(3)
        self.board[self.width - 1 - 3][mid].setLetterMultiplier(2)
    
        # Middle is double word
        self.board[mid][mid].setWordMultiplier(2)

        # Set first quadrant
        self.board[0][0].setWordMultiplier(3)
        self.board[3][0].setLetterMultiplier(2)
        self.board[1][1].setWordMultiplier(2)
        self.board[5][1].setLetterMultiplier(3)
        self.board[2][2].setWordMultiplier(2)
        self.board[6][2].setLetterMultiplier(2)
        self.board[0][3].setLetterMultiplier(2)
        self.board[3][3].setWordMultiplier(2)
        self.board[4][4].setWordMultiplier(2)
        self.board[1][5].setLetterMultiplier(3)
        self.board[5][5].setLetterMultiplier(3)
        self.board[2][6].setLetterMultiplier(2)
        self.board[6][6].setLetterMultiplier(2)
        
        # Copy to other quadrants
        # Quad 2
        for x in xrange(0, 7):
            for y in xrange(0, 7):
                # Quad 2
                self.board[self.width - 1 - x][y].copyLocation(self.board[x][y]) 
                # Quad 3
                self.board[x][self.height - 1 - y].copyLocation(self.board[x][y])
                # Quad 4
                self.board[self.width - 1 - x][self.height - 1 - y].copyLocation(self.board[x][y])
            
    def __repr__(self):
        output = ""
        for y in range(self.height):
            if y != 0:
                output += "|\n"
            for x in range(self.width):
                output += str(self.board[x][y])
        return output + "|"
   
    def addWordToBoard(self, word, starting_coord, horizontal=True):
        offset = 0
        for char in word:
            x, y = starting_coord
            if horizontal:
                self.board[x + offset][y].setTileLetter(char)
            else:
                self.board[x][y + offset].setTileLetter(char)
            offset += 1
    def getTile(self, x, y):
        return self.board[x][y].tile

