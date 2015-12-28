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
            
    def getVerticalWord(self, loc, char):
        x, y = loc
        lowerHalf = []
        upperHalf = []
        upper_y = y + 1
        lower_y = y - 1
        while upper_y < self.height and self.getTile(x, upper_y) is not None:
            upperHalf.append(self.getTile(x, upper_y))
            upper_y += 1
        while lower_y >= 0 and self.getTile(x, lower_y) is not None:
            lowerHalf.insert(0, self.getTile(x, lower_y))
            lower_y -= 1
        if len(lowerHalf) == 0 and len(upperHalf) == 0:
            return (None, None, None)
        return (''.join(lowerHalf + [char] + upperHalf), lowerHalf, upperHalf)

    def getHorizontalWord(self, loc, char):
        x, y = loc
        leftHalf = []
        rightHalf = []
        right_x = x + 1
        left_x = x - 1
        while right_x < self.width and self.getTile(right_x, y) is not None:
            rightHalf.append(self.getTile(right_x, y))
            right_x += 1
        while left_x >= 0 and self.getTile(left_x, y) is not None:
            leftHalf.insert(0, self.getTile(left_x, y))
            left_x -= 1
        if len(rightHalf) == 0 and len(leftHalf) == 0:
            return (None, None, None)
        return (''.join(leftHalf + [char] + rightHalf), leftHalf, rightHalf)

    def getPredecessingString(self, loc, horizontal=True):
        x, y = loc
        previousStrArr = []
        if horizontal:
            previous_x = x - 1
            while previous_x >= 0 and self.getTile(previous_x, y) is not None: 
                previousStrArr.insert(0, self.getTile(previous_x, y))
                previous_x -= 1
        else:
            previous_y = y - 1
            while previous_y >= 0 and self.getTile(x, previous_y) is not None:
                previousStrArr.insert(0, self.getTile(x, previous_y))
                previous_y -= 1
        return ''.join(previousStrArr)

    # points_flag is a flag where we don't actually add the word to the board but retrieve the # of pts if we did
    def addWordToBoard(self, word, starting_coord, horizontal=True, points_flag=False):
        word_dict = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10 }
        x, y = starting_coord
        char_i = 0
        total_points = 0
        constraint_points = 0
        word_multiplier = 1

        previous_str = self.getPredecessingString((x,y), horizontal)
        # Calculate previous_str points
        for prev_char in previous_str:
            total_points += word_dict[prev_char]


        if horizontal:
            # Calculate laid out word
            while char_i < len(word) or (x < self.width and self.getTile(x, y) is not None):
                print "(" + str(x) + "," + str(y) + ")"
                if self.getTile(x, y) is not None:
                    total_points += word_dict[self.getTile(x, y)]
                    x += 1
                    continue

                char = word[char_i]
                word_multiplier = max(self.board[x][y].word_multiplier, word_multiplier)
                letter_multiplier = self.board[x][y].letter_multiplier
                char_points = letter_multiplier * word_dict[char]
                total_points += char_points

                # Generate vertical constraints
                v_word, lowerHalf, upperHalf = self.getVerticalWord((x,y), char)
                if v_word is not None:
                    vertical_points = 0
                    for v_char in lowerHalf:
                        vertical_points += word_dict[v_char]
                    for v_char in upperHalf:
                        vertical_points += word_dict[v_char]
                    vertical_points += char_points
                    vertical_points *= word_multiplier
                    constraint_points += vertical_points

                if not points_flag:
                    self.board[x][y].setTileLetter(char)

                x += 1
                char_i += 1

            total_points *= word_multiplier
            return total_points + constraint_points
        else:
            while char_i < len(word) or (y < self.height and self.getTile(x, y) is not None):
                if self.getTile(x, y) is not None:
                    total_points += word_dict[self.getTile(x, y)]
                    y += 1
                    continue

                char = word[char_i]
                word_multiplier = max(self.board[x][y].word_multiplier, word_multiplier)
                letter_multiplier = self.board[x][y].letter_multiplier
                char_points = letter_multiplier * word_dict[char]
                total_points += char_points


                # Generate vertical constraints
                h_word, lowerHalf, upperHalf = self.getHorizontalWord((x,y), char)
                if h_word is not None:
                    horizontal_points = 0
                    for h_char in lowerHalf:
                        horizontal_points += word_dict[h_char]
                    for h_char in upperHalf:
                        horizontal_points += word_dict[h_char]
                    horizontal_points += char_points
                    horizontal_points *= word_multiplier
                    constraint_points += horizontal_points

                if not points_flag:
                    self.board[x][y].setTileLetter(char)

                y += 1
                char_i += 1

            total_points *= word_multiplier
            return total_points + constraint_points


    def getTile(self, x, y):
        return self.board[x][y].tile

    def __repr__(self):
        output = ""
        for y in range(self.height):
            if y != 0:
                output += "|\n"
            for x in range(self.width):
                output += str(self.board[x][y])
        return output + "|"
