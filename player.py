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
        dict_file = open("dictionary.txt", "r")
        lines = dict_file.readlines()
        for line in lines:
            self.dictionary.add(line.rstrip('\n').upper())

    def initializeConstraintsWithBoard(self, board):
        self.board = board  # Update board with new one
        for x in range(self.board.width):
            self.constraints[x] = list()
            for y in range(self.board.height):
                constraint = c.Constraint(x, y, self.domain, self.board.board[x][y].tile)
                self.constraints[x].append(constraint)

    def inputNewTiles(self):
        print("Enter each tile. Return when finished")
        temp_tiles = []
        while True:
            tile = raw_input("Letter:")
            if tile == "":
                if len(temp_tiles) + len(self.tiles) != 7:
                    print "incorrect # of tiles. Please re-enter. Your current tiles are " + str(self.tiles)
                    temp_tiles = []
                else:
                    break
            temp_tiles += [tile]
        self.addTiles(temp_tiles)
        self.generateAllPermutations()
        
    def addTiles(self, tile_list):
        self.tiles += tile_list

    def removeTiles(self, word):
        for char in word:
            self.tiles.remove(char)

    def generateAllPermutations(self):
        total = []
        for i in range(1, len(self.tiles) + 1):
            total += [''.join(p) for p in permutations(self.tiles, i) ]
        self.domain = list(set(total))


    # Constraints
    # 1. Lay out word horizontally
    #   1a. Check if length fits
    # 2. Check if laid out word connects with another word
    #   2a. Check if word connects and can be placed
    # 3. Check if liad out word in dict AND constrained words in dict
    #   3a. Check if all pass
    def _updateHorizontalConstraint(self, constraint):
        # Horizontal
        x, y = constraint.x, constraint.y
        domain_copy = constraint.h_domain[:]
        for d in domain_copy:
            # 1. Lay out word horizontally
            #   1a. Check if length fits
            # 2. Check if laid out word connects with another word
            #   2a. Check if word connects and can be placed
            # 3. Check if liad out word in dict AND constrained words in dict
            #   3a. Check if all pass
            board_x = x
            horizontal_word = self.board.getPredecessingString((x, y))
            valid_placement = False if horizontal_word == "" else True
            word_constraints = []
            char_i = 0
            while char_i < len(d) or (board_x < self.board.width and self.board.getTile(board_x, y) is not None):
                # Length check
                if board_x >= self.board.width:
                    valid_placement = False
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
                v_constraint = self.board.getVerticalWord((board_x, y), char)[0] 
                if v_constraint is not None:
                    valid_placement = True      # Makes d a valid placement 
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
                    constraint.removeValueFromDomain(d)
                    break

        return constraint 

    def _updateVerticalConstraint(self, constraint):
        # Vertical
        x, y = constraint.x, constraint.y
        domain_copy = constraint.v_domain[:]
        for d in domain_copy:
            board_y = y
            vertical_word = self.board.getPredecessingString((x, y), False)
            valid_placement = False if vertical_word == "" else True
            word_constraints = []
            char_i = 0
            #print "Domain:" + str(d)
            while char_i < len(d) or (board_y < self.board.height and self.board.getTile(x, board_y) is not None):
                # Length check
                if board_y >= self.board.height:
                    valid_placement = False
                    break
                
                # Check following vertical board locations
                board_tile_y = self.board.getTile(x, board_y)
                if board_tile_y is not None:
                    valid_placement = True  # Makes d valid with connecting horizontally
                    vertical_word += board_tile_y
                    board_y += 1
                    continue
                    
                char = d[char_i]
                if board_tile_y is None:
                    vertical_word += char
                    char_i += 1

                # Check for horizontal constraints
                lower_x = x - 1
                higher_x = x + 1
                h_constraint = self.board.getHorizontalWord((x, board_y), char)[0]
                if h_constraint is not None:
                    valid_placement = True      # Makes d a valid placement  
                    word_constraints += [h_constraint]

                # Increment board_y at end of loop
                board_y += 1

            if not valid_placement:
                constraint.removeValueFromDomain(d, False)
                continue
        
            # Check if word in dict AND constrained words in dict
            if vertical_word.upper() not in self.dictionary:
                constraint.removeValueFromDomain(d, False)
                continue    
            for v_constraint in word_constraints:
                if v_constraint.upper() not in self.dictionary:
                    constraint.removeValueFromDomain(d, False)
                    break
        return constraint 
        

    def _runRules(self, constraint):
        # Horizontal
        constraint = self._updateHorizontalConstraint(constraint)
        constraint = self._updateVerticalConstraint(constraint)    
        return constraint

    def getOptimalMove(self):
        optimal_move = (0, None, None, None)
        for x in xrange(self.board.width):
            for y in xrange(self.board.height):
                constraint = self.constraints[x][y]
                if constraint.tile is None:
                    for h in constraint.h_domain:
                        print h
                        print "(" + str(x) + "," + str(y) + ")"
                        points = self.board.addWordToBoard(h, (x, y), True, True)
                        if points >= optimal_move[0]:
                            optimal_move = (points, h, (x, y), True)
                    for v in constraint.v_domain:
                        points = self.board.addWordToBoard(h, (x, y), False, True)
                        if points >= optimal_move[0]:
                            optimal_move = (points, v, (x, y), False)
        print "OPTIMAL MOVE:"
        print optimal_move
        return optimal_move
            
    def enforceConstraints(self):
        for x in xrange(self.board.width):
            for y in xrange(self.board.height):
                constraint = self.constraints[x][y]
                if constraint.tile is None:
                    constraint = self._runRules(constraint)
                    print(constraint)
                    self.constraints[x][y] = constraint

    def getOptimalStartMove(self):
        optimal_move = (0, None, None, None)
        word_dict = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10 }
        for d in self.domain:
            if d in self.dictionary:
                points = self.board.addWordToBoard(d, (7, 7), True, True)
                if points >= optimal_move[0]:
                    optimal_move = (points, d, (7, 7))
        print "OPTIMAL MOVE:"
        print optimal_move
        return optimal_move



