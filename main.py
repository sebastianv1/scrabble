import player as p
import board as b 
def main():
    board = b.Board()
    player = p.Player(board)
    
    board.addWordToBoard("start", (7, 7)) 
    board.addWordToBoard("to", (1, 7))
    print(str(board))
    turn = raw_input("First or second? 0-First, 1-Second\n")
    if turn == '0':
        player.inputNewTiles()
        player.initializeConstraintsWithBoard(board, player.domain)
        player.enforceConstraints()
main()
