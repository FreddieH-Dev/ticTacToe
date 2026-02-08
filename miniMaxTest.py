import random

board = [[" ", " ", " "], 
         [" ", " ", " "], 
         [" ", " ", " "]]

gameComplete = False
gameWinner = None

MAX_DEPTH = 3


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
    
    # Check tie
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                count += 1
    if count == 0:
        return "Tie"
            
    return None


def evaluateBoard(board):
    def checkLine(a, b, c):
        line = [a, b, c]
        if line.count("O") == 2 and line.count(" ") == 1:
            return 5  # Computer almost wins
        elif line.count("X") == 2 and line.count(" ") == 1:
            return -5  # Player almost wins
        elif line.count("O") == 1 and line.count(" ") == 2:
            return 1  # Computer has potential
        elif line.count("X") == 1 and line.count(" ") == 2:
            return -1  # Player has potential
        return 0
    
    score = 0
    
    # Check rows
    for i in range(3):
        score += checkLine(board[i][0], board[i][1], board[i][2])
    
    # Check columns
    for j in range(3):
        score += checkLine(board[0][j], board[1][j], board[2][j])
    
    # Check diagonals
    score += checkLine(board[0][0], board[1][1], board[2][2])
    score += checkLine(board[0][2], board[1][1], board[2][0])
    
    return score


def playerMove():
    move = int(input("Enter your move (1-9): "))
    while move < 1 or move > 9:
        move = int(input("Invalid! Enter a number between 1 and 9: "))

    move = move - 1
    row = move // 3
    col = move % 3
        
    while board[row][col] != " ":
        print("That spot is already taken!")
        move = int(input("Enter your move (1-9): "))
        while move < 1 or move > 9:
            move = int(input("Invalid! Enter a number between 1 and 9: "))
        move = move - 1
        row = move // 3
        col = move % 3
        
    board[row][col] = "X"


def availableMoves(board):
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                moves.append((row, col))
    return moves


def computerMove(board):
    bestScore = -float('inf')
    bestMove = None
    
    moves = availableMoves(board)
    
    for move in moves:
        row, col = move
        board[row][col] = "O"
        score = minimize(board, 0)
        board[row][col] = " "
        
        if score > bestScore:
            bestScore = score
            bestMove = move
    
    if bestMove:
        row, col = bestMove
        board[row][col] = "O"
        print(f"Computer plays position {row * 3 + col + 1}")


def maximize(board, depth):
    # Check if game is over
    winner = checkWin(board)
    if winner == "O":
        return 10 - depth
    elif winner == "X":
        return -10 + depth
    elif winner == "Tie":
        return 0
    
    # Check if depth limit reached
    if depth >= MAX_DEPTH:
        return evaluateBoard(board)
    
    bestScore = -float('inf')
    moves = availableMoves(board)
    
    for move in moves:
        row, col = move
        board[row][col] = "O"
        score = minimize(board, depth + 1)
        board[row][col] = " "
        bestScore = max(bestScore, score)
    
    return bestScore


def minimize(board, depth):
    # Check if game is over
    winner = checkWin(board)
    if winner == "O":
        return 10 - depth
    elif winner == "X":
        return -10 + depth
    elif winner == "Tie":
        return 0
    
    # Check if depth limit reached
    if depth >= MAX_DEPTH:
        return evaluateBoard(board)
    
    bestScore = float('inf')
    moves = availableMoves(board)
    
    for move in moves:
        row, col = move
        board[row][col] = "X"
        score = maximize(board, depth + 1)
        board[row][col] = " "
        bestScore = min(bestScore, score)
    
    return bestScore


print("Tic-Tac-Toe: You are X, Computer is O")

currentPlayer = "X"

while not(gameComplete):
    printBoard()
    print()
    
    if currentPlayer == "X":
        print("Your turn!")
        playerMove()
        currentPlayer = "O"
    else:
        print("Computer's turn...")
        computerMove(board)
        currentPlayer = "X"

    gameWinner = checkWin(board)
    if gameWinner:
        gameComplete = True

printBoard()
print()
if gameWinner == "Tie":
    print("It's a tie!")
else:
    print("Game over! Winner: " + gameWinner)