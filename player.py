from itertools import permutations
import constraint as c

class Player:
    def __init__(self, board):
        self.tiles = list()
        self.domain = list()
        self.score = 0
        self.dictionary = set()
        self.constraints = list()
        self.board = board
        # init functions
        self._generateDictionarySet()
    
        # Generate 2d constraint array
        for _ in range(self.board.width):
            self.constraints.append(list())
    
    def _generateDictionarySet(self):
        dict_file = open("words.txt", "r")
        lines = dict_file.readlines()
        for line in lines:
            self.dictionary.add(line.rstrip('\n'))

    def initializeConstraintsWithBoard(self, board, domain):
        self.board = board  # Update board with new one
        for x in range(self.board.width):
            self.constraints[x] = list()
            for y in range(self.board.height):
                constraint = c.Constraint(x, y, domain, self.board.board[x][y].tile)
                self.constraints[x].append(constraint)

    def inputNewTiles(self):
        print("Enter each tile. Return when finished")
        temp_tiles = []
        while True:
            tile = raw_input("Letter:")
            if tile == "":
                if len(temp_tiles) + len(self.tiles) != 3:
                    print "incorrect # of tiles. Please re-enter. Your current tiles are " + str(self.tiles)
                    temp_tiles = []
                else:
                    break
            temp_tiles += [tile]
        self.addTiles(temp_tiles)
        self.generateAllPermutations()
        
    def addTiles(self, tile_list):
        self.tiles += tile_list

    def removeTiles(self, tiles_list):
        for tile in tiles_list:
            self.tiles.remove(tile)

    def generateAllPermutations(self):
        total = []
        for i in range(1, len(self.tiles) + 1):
            total += [''.join(p) for p in permutations(self.tiles, i) ]
        self.domain = list(set(total))

    def getPointsForWord(self, word, blank_tile_letter=None):
        word_dict = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10 }
        total_points = 0
        for char in word:
            if char == blank_tile_letter:
                continue
            total_points += word_dict[char]
        return total_points

    # Constraints
    def _getVerticalWord(self, loc, char):
        x, y = loc
        lowerHalf = []
        upperHalf = []
        upper_y = y + 1
        lower_y = y - 1
        while upper_y < self.board.height and self.board.getTile(x, upper_y) is not None:
            upperHalf.append(self.board.getTile(x, upper_y))
            upper_y += 1
        while lower_y >= 0 and self.board.getTile(x, lower_y) is not None:
            lowerHalf.insert(0, self.board.getTile(x, lower_y))
            lower_y -= 1
        return ''.join(lowerHalf + [char] + upperHalf) 

    def _getPredecessingString(self, loc):
        x, y = loc
        previous_x = x - 1
        previousStrArr = []
        while previous_x >= 0 and self.board.getTile(previous_x, y) is not None: 
            previousStrArr.insert(0, self.board.getTile(previous_x, y))
            previous_x -= 1
        return ''.join(previousStrArr)

    def _runRules(self, constraint):
        # Horizontal
        x, y = constraint.x, constraint.y
        # Horizontal
        domain_copy = constraint.h_domain[:]
        for d in domain_copy:
            # 1. Lay out word horizontally
            #   1a. Check if length fits
            # 2. Check if laid out word connects with another word
            #   2a. Check if word connects and can be placed
            # 3. Check if liad out word in dict AND constrained words in dict
            #   3a. Check if all pass
            board_x = x
            horizontal_word = self._getPredecessingString((x, y))
            valid_placement = False if horizontal_word == "" else True
            word_constraints = []
            char_i = 0
            #print "Domain:" + str(d)
            while char_i < len(d) or (board_x < self.board.width and self.board.getTile(board_x, y) is not None):
                # Length check
                if board_x >= self.board.width:
                    break
                
                # Check following horizontal board locations
                board_tile_x = self.board.getTile(board_x, y)
                if board_tile_x is not None:
                    valid_placement = True  # Makes d valid with connecting horizontally
                    horizontal_word += board_tile_x 
                    board_x += 1
                    continue
                    
                char = d[char_i]
                if board_tile_x is None:
                    horizontal_word += char
                    char_i += 1

                # Check for vertical constraints
                lower_y = y - 1
                higher_y = y + 1
                if (lower_y >= 0 and self.board.getTile(board_x, lower_y) is not None) or (higher_y < self.board.height and self.board.getTile(board_x, higher_y) is not None):
                    valid_placement = True      # Makes d a valid placement       
                    v_constraint = self._getVerticalWord((board_x, y), char)             
                    #print "V Constraint:" + str(v_constraint)
                    word_constraints += [v_constraint]

                # Increment board_x at end of loop
                board_x += 1

            # Check if we continue look
            if not valid_placement:
                #print "Not Valid placement"
                constraint.removeValueFromDomain(d)
                continue
        
            # Check if word in dict AND constrained words in dict
            if horizontal_word.upper() not in self.dictionary:
                #print "Not valid word: " + str(horizontal_word.upper())
                constraint.removeValueFromDomain(d)
                continue    
            for v_constraint in word_constraints:
                if v_constraint.upper() not in self.dictionary:
                    #print "Not valid constraint: " + str(v_constraint.upper())
                    constraint.removeValueFromDomain(d)
                    break
        return constraint            
            
    def enforceConstraints(self):
        for x in xrange(self.board.width):
            for y in xrange(self.board.height):
                constraint = self.constraints[x][y]
                if constraint.tile is None:
                    constraint = self._runRules(constraint)
                    print(constraint)
                    self.constraints[x][y] = constraint
