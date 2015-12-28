import player as p
import board as b 
def main():
    board = b.Board()
    player = p.Player(board)
    print(board) 
    print(board.addWordToBoard("START", (7, 7)))
    print(board.addWordToBoard("TARTING", (7, 8), False, True))
    print(str(board))
    turn = raw_input("First or second? 0-First, 1-Second\n")
    if turn == '0':
        player.inputNewTiles()
        player.initializeConstraintsWithBoard(board, player.domain)
        player.enforceConstraints()
main()
