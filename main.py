import player as p
import board as b 


def printGameDetails(board, player_score, opponent_score, player):
	print(board)
	print "Player Score: " + str(player_score)
	print "Opponent Score: " + str(opponent_score)
	print "Player Current tiles: " + str(player.tiles)

def queryOpponentInput():
	word = raw_input("Opponent letter move:")
	x_start = raw_input("Starting X:")
	y_start = raw_input("Starting Y:")
	horizontal = raw_input("Horizontal? 1-T, 0-F:")
	if horizontal == '1':
		horizontal = True
	else:
		horizontal = False
	loc = ( int(x_start), int(y_start) )
	return (word, loc, horizontal)

def main():
    board = b.Board()
    player = p.Player(board)

    opponent_score = 0
    player_score = 0
    
    player_turn = False

    print(board) 
    turn = raw_input("First or second? 0-First, 1-Second\n")
    if turn == '0':
        player.inputNewTiles()
        score, word, loc = player.getOptimalStartMove()
        board.addWordToBoard(word, loc)
        player.removeTiles(word)
        player_score += score
        printGameDetails(board, player_score, opponent_score, player)
    elif turn == '1':
        word, loc, horizontal = queryOpponentInput()
        move_score = board.addWordToBoard(word, loc, horizontal)
        opponent_score += move_score
        player_turn = True
        printGameDetails(board, player_score, opponent_score, player)

    while True:
        if player_turn is True:
            player.inputNewTiles()
            
            player.initializeConstraintsWithBoard(board)
            player.enforceConstraints()

            score, word, loc, horizontal = player.getOptimalMove()
            move_score = board.addWordToBoard(word, loc, horizontal)

            player_score += score
            player.removeTiles(word)
           
            player_turn = False
            printGameDetails(board, player_score, opponent_score, player)
        else:
            word, loc, horizontal = queryOpponentInput()
            move_score = board.addWordToBoard(word, loc, horizontal)
            opponent_score += move_score
            player_turn = True
            printGameDetails(board, player_score, opponent_score, player)

main()
