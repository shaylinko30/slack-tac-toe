
firstPlayerValue = 'X'

secondPlayerValue = 'O'

untouchedValue = '-'

def getBaseGame():
    return [
        [untouchedValue,untouchedValue,untouchedValue],
        [untouchedValue,untouchedValue,untouchedValue],
        [untouchedValue,untouchedValue,untouchedValue]
    ]

def checkWinner(board):
    # X X X   - - -   - - -
    # - - -   X X X   - - -
    # - - -   - - -   X X X
    for row in range(0,3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != untouchedValue:
            return True

    # X - -   - X -   - - X
    # X - -   - X -   - - X
    # X - -   - X -   - - X
    for column in range(0,3):
        if board[0][column] == board[1][column] == board[2][column] and board[row][0] != untouchedValue:
            return True

    # X - -   - - X
    # - X -   - X -
    # - - X   X - - 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != untouchedValue:
        return True
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != untouchedValue:
        return True

    return False
    

def checkTie(board):
    for row in range(0,3):
        for column in range(0,3):
            if board[row][column] == untouchedValue:
                return False
    return True


def getOpposite(value):
    if value == firstPlayerValue:
        return secondPlayerValue
    return firstPlayerValue

