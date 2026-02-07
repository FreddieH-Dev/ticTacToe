import random

board = [[" ", " ", " "], 
         [" ", " ", " "], 
         [" ", " ", " "]]

#Player is X
#Computer is O

gameComplete = False
gameWinner = None


def availableMoves(board):
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                moves.append((row, col))
    return moves



def printBoard():
    for i in range(3):
        print(board[i][0] + " | " + board[i][1] + " | " + board[i][2])
        if i != 2:
            print("---------")



def checkWin(board):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != " ":
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None


def isBoardFull(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


def miniMax(board, depth, isMaximizing):
    winner = checkWin(board)
    
    # Base cases
    if winner == "O":  # Computer wins
        return 10 - depth
    elif winner == "X":  # Player wins
        return depth - 10
    elif isBoardFull(board):  # Tie
        return 0
    
    if isMaximizing:  # Computer's turn (O)
        bestScore = -float('inf')
        for row, col in availableMoves(board):
            board[row][col] = "O"
            score = miniMax(board, depth + 1, False)
            board[row][col] = " "
            bestScore = max(score, bestScore)
        return bestScore
    else:  # Player's turn (X)
        bestScore = float('inf')
        for row, col in availableMoves(board):
            board[row][col] = "X"
            score = miniMax(board, depth + 1, True)
            board[row][col] = " "
            bestScore = min(score, bestScore)
        return bestScore


def findBestMove(board):
    bestScore = -float('inf')
    bestMove = None
    
    for row, col in availableMoves(board):
        board[row][col] = "O"
        score = miniMax(board, 0, False)
        board[row][col] = " "
        
        if score > bestScore:
            bestScore = score
            bestMove = (row, col)
    
    return bestMove


def playerMove():
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if move < 1 or move > 9:
                print("Invalid! Enter a number between 1 and 9.")
                continue
            
            move = move - 1
            row = move // 3
            col = move % 3
            
            if board[row][col] != " ":
                print("That spot is already taken!")
                continue
            
            board[row][col] = "X"
            break
        except ValueError:
            print("Invalid input! Enter a number.")


print("Tic-Tac-Toe: You are X, Computer is O")

currentPlayer = random.choice(["X", "O"])  # Player goes first

while not(gameComplete):
    printBoard()
    print()
    
    if currentPlayer == "X":
        print("Your turn!")
        playerMove()
        currentPlayer = "O"
    else:
        print("Computer's turn...")
        moves = availableMoves(board)
        if moves:
            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = "O"
            print(f"Computer placed O at position {bestMove[0] * 3 + bestMove[1] + 1}")
        currentPlayer = "X"
    
    print()
    
    winner = checkWin(board)
    if winner:
        printBoard()
        print()
        print(f"Winner: {winner}!")
        gameComplete = True
        gameWinner = winner
    elif isBoardFull(board):
        printBoard()
        print()
        print("It's a tie!")
        gameComplete = True