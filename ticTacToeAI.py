import random
import time

SEARCH_DEPTH = None  # <-- Change this value to adjust AI strength

gameWon = False


class Board:
    def __init__(self, complete, winner, layout):
        self.complete  = complete
        self.winner = winner
        self.layout = layout

    def getRows(self):
        return [
        f"{self.layout[0][0]} | {self.layout[0][1]} | {self.layout[0][2]}",
        f"{self.layout[1][0]} | {self.layout[1][1]} | {self.layout[1][2]}",
        f"{self.layout[2][0]} | {self.layout[2][1]} | {self.layout[2][2]}",
        ]



    def printBoard(self):
        rows = self.getRows()
        for i in range(3):
            print(rows[i])
            if i < 2:
                print("---------")



    def checkWin(self):
        # Check rows
        for i in range(3):
            if self.layout[i][0] == self.layout[i][1] == self.layout[i][2] != " ":
                self.complete = True
                self.winner = self.layout[i][0]
                for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
                
                return
        
        # Check columns
        for j in range(3):
            if self.layout[0][j] == self.layout[1][j] == self.layout[2][j] != " ":
                self.complete = True
                self.winner = self.layout[0][j]
                for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
                return
        
        # Check diagonals
        if self.layout[0][0] == self.layout[1][1] == self.layout[2][2] != " ":
            self.complete = True
            self.winner = self.layout[0][0]
            for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
            return
        
        if self.layout[0][2] == self.layout[1][1] == self.layout[2][0] != " ":
            self.complete = True
            self.winner = self.layout[0][2]
            for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
            return
        
        count = 0
        if self.complete == False:
            for i in range(3):
                for j in range(3):
                    if self.layout[i][j] != " ":
                        count = count + 1
            if count == 9:
                self.complete = True
                self.winner = "TIE"
                for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner


def copyGameState(fullBoardDict):
    #creates a copy of all boards
    newDict = {}
    for key in fullBoardDict:
        board = fullBoardDict[key]
        newLayout = [row[:] for row in board.layout]
        newDict[key] = Board(board.complete, board.winner, newLayout)
    return newDict


def checkGameWinner(boardDict):
    #checks if the entire game has been won
    # Check rows
    for i in range(3):
        if (boardDict[i*3+1].winner == boardDict[i*3+2].winner == boardDict[i*3+3].winner != " " 
            and boardDict[i*3+1].winner != "TIE"):
            return boardDict[i*3+1].winner
    
    # Check columns
    for j in range(3):
        if (boardDict[j+1].winner == boardDict[j+4].winner == boardDict[j+7].winner != " " 
            and boardDict[j+1].winner != "TIE"):
            return boardDict[j+1].winner
    
    # Check diagonals
    if (boardDict[1].winner == boardDict[5].winner == boardDict[9].winner != " " 
        and boardDict[1].winner != "TIE"):
        return boardDict[1].winner
    
    if (boardDict[3].winner == boardDict[5].winner == boardDict[7].winner != " " 
        and boardDict[3].winner != "TIE"):
        return boardDict[3].winner
    
    # Check for full game tie
    if all(boardDict[i].complete for i in range(1, 10)):
        return "TIE"
    
    return None


def evaluateGameState(boardDict, computerToken, playerToken):
    #Computer boards = positive, Player boards = negative

    score = 0
    
    # Check if game is won
    winner = checkGameWinner(boardDict)
    if winner == computerToken:
        return 1000  # Computer wins!
    elif winner == playerToken:
        return -1000  # Player wins!
    elif winner == "TIE":
        return 0
    
    # Count board wins
    for boardNum in range(1, 10):
        if boardDict[boardNum].winner == computerToken:
            score += 10
        elif boardDict[boardNum].winner == playerToken:
            score -= 10
        elif boardDict[boardNum].winner == "TIE":
            score += 0
    
    # Bonus for center board
    if boardDict[5].winner == computerToken:
        score += 3
    elif boardDict[5].winner == playerToken:
        score -= 3
    
    # Bonus for corners
    for corner in [1, 3, 7, 9]:
        if boardDict[corner].winner == computerToken:
            score += 2
        elif boardDict[corner].winner == playerToken:
            score -= 2
    
    return score


def getValidMoves(boardDict, currentBoardNum):
    #Get all valid moves from current position
    moves = []
    
    # If current board is complete, can play anywhere
    if currentBoardNum is None or boardDict[currentBoardNum].complete:
        for boardNum in range(1, 10):
            if not boardDict[boardNum].complete:
                board = boardDict[boardNum]
                for row in range(3):
                    for col in range(3):
                        if board.layout[row][col] == " ":
                            moves.append((boardNum, row, col))
    else:
        # Must play on current board
        board = boardDict[currentBoardNum]
        for row in range(3):
            for col in range(3):
                if board.layout[row][col] == " ":
                    moves.append((currentBoardNum, row, col))
    
    return moves


def applyMove(boardDict, boardNum, row, col, token):
    #Apply a move to the board state and return next board number
    boardDict[boardNum].layout[row][col] = token
    boardDict[boardNum].checkWin()
    nextBoardNum = row * 3 + col + 1
    return nextBoardNum


# Global variables for thought tree printing
thoughtTreeLines = []
nodesEvaluated = 0


def minimax(boardDict, currentBoardNum, depth, maxDepth, isMaximizing, 
            computerToken, playerToken):
    global thoughtTreeLines, nodesEvaluated
    nodesEvaluated += 1
    
    
    # Check if game is over
    winner = checkGameWinner(boardDict)
    if winner is not None:
        score = evaluateGameState(boardDict, computerToken, playerToken)
        return score, None
    
    # Check depth limit
    if depth >= maxDepth:
        score = evaluateGameState(boardDict, computerToken, playerToken)
        return score, None
    
    # Get all valid moves
    validMoves = getValidMoves(boardDict, currentBoardNum)
    
    if not validMoves:
        score = evaluateGameState(boardDict, computerToken, playerToken)
        return score, None
    
    bestMove = None
    
    if isMaximizing:  # Computer's turn
        maxScore = -float('inf')
        
        for move in validMoves:
            boardNum, row, col = move
            
            # Make move on a copy
            newBoardDict = copyGameState(boardDict)
            nextBoardNum = applyMove(newBoardDict, boardNum, row, col, computerToken)
            
            # Describe move
            tileNum = row * 3 + col + 1
            moveDesc = f"[D{depth}] Computer: Board {boardNum}, Tile {tileNum} → "
            
            # Recursive call
            score, _ = minimax(newBoardDict, nextBoardNum, depth + 1, maxDepth, 
                              False, computerToken, playerToken)
            
            if score > maxScore:
                maxScore = score
                bestMove = move
        
        return maxScore, bestMove
    
    else:  # Player's turn
        minScore = float('inf')
        
        for move in validMoves:
            boardNum, row, col = move
            
            # Make move on a copy
            newBoardDict = copyGameState(boardDict)
            nextBoardNum = applyMove(newBoardDict, boardNum, row, col, playerToken)
            
            # Describe move
            tileNum = row * 3 + col + 1
            moveDesc = f"[D{depth}] Player: Board {boardNum}, Tile {tileNum} → "
            
            # Recursive call
            score, _ = minimax(newBoardDict, nextBoardNum, depth + 1, maxDepth, 
                              True, computerToken, playerToken)
            
            if score < minScore:
                minScore = score
                bestMove = move
        
        return minScore, bestMove


def findBestMove(fullBoardDict, currentBoardNum, computerToken, playerToken):
    global thoughtTreeLines, nodesEvaluated
    
    thoughtTreeLines = []
    nodesEvaluated = 0
    startTime = time.time()
    
    score, bestMove = minimax(fullBoardDict, currentBoardNum, 0, SEARCH_DEPTH, 
                              True, computerToken, playerToken)
    return bestMove


def checkFullWin(gameWon):
    # Check rows
    for i in range(3):
        if (fullBoardDict[i*3+1].winner == fullBoardDict[i*3+2].winner == fullBoardDict[i*3+3].winner != " " 
            and fullBoardDict[i*3+1].winner != "TIE"):
            gameWon = True
            print(f"{fullBoardDict[i*3+1].winner} wins the game!")
            return gameWon
    
    # Check columns
    for j in range(3):
        if (fullBoardDict[j+1].winner == fullBoardDict[j+4].winner == fullBoardDict[j+7].winner != " " 
            and fullBoardDict[j+1].winner != "TIE"):
            gameWon = True
            print(f"{fullBoardDict[j+1].winner} wins the game!")
            return gameWon
    
    # Check diagonals
    if (fullBoardDict[1].winner == fullBoardDict[5].winner == fullBoardDict[9].winner != " " 
        and fullBoardDict[1].winner != "TIE"):
        gameWon = True
        print(f"{fullBoardDict[1].winner} wins the game!")
        return gameWon
    
    if (fullBoardDict[3].winner == fullBoardDict[5].winner == fullBoardDict[7].winner != " " 
        and fullBoardDict[3].winner != "TIE"):
        gameWon = True
        print(f"{fullBoardDict[3].winner} wins the game!")
        return gameWon
    
    return False

boardTL = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardTM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardTR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardML = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardMM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardMR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBL = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])

fullBoardDict = {
    1 : boardTL,
    2 : boardTM,
    3 : boardTR,
    4 : boardML,
    5 : boardMM,
    6 : boardMR,
    7 : boardBL,
    8 : boardBM,
    9 : boardBR
}

def beginning():
    print("Welcome to Ultimate Tic Tac Toe!")
    rules = str(input("Would you like to read the rules? (y/n) >> "))
    while rules.lower() != "y" and rules.lower() != "n":
        rules = str(input("Invalid input. Please enter 'y' for yes or 'n' for no: >> "))
    if rules.lower() == "y":
        print("\nRules:")
        print("1. The game is played on a 3x3 grid of tic tac toe boards (9 boards total).")
        print("2. Each small board is a regular tic tac toe game.")
        print("3. To win a small board, get 3 in a row on that board.")
        print("4. To win the overall game, win 3 small boards in a row (horizontally, vertically, or diagonally).")
        print("5. On your turn, you must play on the board corresponding to your opponent's last move.")
        print("   For example, if your opponent played in the top right corner of their board, you must play on the top right board.")
        print("6. If you are sent to a board that is already won or full, you can play on any other board.")
        print("7. The first player to win 3 boards in a row wins the game!")
        print("\nGood luck and have fun playing!\n")
    
    difficulty = int(input("Choose AI difficulty (1-5, higher is harder): >> "))
    while difficulty < 1 or difficulty > 5:
        difficulty = int(input("Invalid input. Please enter a number between 1 and 5: >> "))
    
    print()
    
    return difficulty
    


def printFullBoards():
    top    = [boardTL.getRows(), boardTM.getRows(), boardTR.getRows()]
    middle = [boardML.getRows(), boardMM.getRows(), boardMR.getRows()]
    bottom = [boardBL.getRows(), boardBM.getRows(), boardBR.getRows()]

    allSections = [top, middle, bottom]

    print()
    for sectionIndex, section in enumerate(allSections):
        for rowIndex in range(3):
            print(
                section[0][rowIndex]
                + " # "
                + section[1][rowIndex]
                + " # "
                + section[2][rowIndex]
            )
            if rowIndex < 2:
                print("---------" + " # " + "---------" + " # " + "---------")
        
        if sectionIndex < 2:
            print("# # # # # # # # # # # # # # # # #")
    print("\n\n")


def setup():
    playerToken = int(input("Would you rather be X or O? (1,2): >> "))
    while playerToken != 1 and playerToken != 2:
        playerToken = int(input("Invalid input. Please enter 1 for X or 2 for O: >> "))
    if playerToken == 1:
        playerToken = "X"
        computerToken = "O"
    else:
        playerToken = "O"
        computerToken = "X"
    
    coinFlip = random.randint(1,2)
    if coinFlip == 1:
        return playerToken, computerToken, True
    else:
        return playerToken, computerToken, False


def setupOutput(playerToken, computerToken, firstMove):
    print(f"You are playing as: {playerToken}")
    print(f"Computer is playing as: {computerToken}")

    print()

    print("Flipping a coin to see who goes first.",end='')
    for wait in range(5):
        time.sleep(0.5)
        print(".",end='')

    print()

    if firstMove:
        print("You are playing first!")
    else:
        print("Computer is playing first!")

    time.sleep(1)
    print("\n\n")


def makeFirstMove(currentPlayer, playerToken, computerToken):
    """Handle first move when any board can be chosen"""
    if currentPlayer == computerToken:
        # Computer uses minimax
        bestMove = findBestMove(fullBoardDict, None, computerToken, playerToken)
        
        if bestMove:
            boardNum, row, col = bestMove
            currentBoard = fullBoardDict[boardNum]
            currentBoard.layout[row][col] = computerToken
            currentBoard.checkWin()
            
            tileNum = row * 3 + col + 1
            print(f"Computer chose board {boardNum}")
            print(f"Computer placed {computerToken} at tile {tileNum}")
            
            nextBoardNum = row * 3 + col + 1
            return fullBoardDict[nextBoardNum], nextBoardNum
        else:
            # Fallback to random
            boardNum = random.randint(1, 9)
            currentBoard = fullBoardDict[boardNum]
            availableSpots = [(r, c) for r in range(3) for c in range(3) if currentBoard.layout[r][c] == " "]
            row, col = random.choice(availableSpots)
            currentBoard.layout[row][col] = computerToken
            currentBoard.checkWin()
            print(f"Computer chose board {boardNum}")
            nextBoardNum = row * 3 + col + 1
            return fullBoardDict[nextBoardNum], nextBoardNum
    
    # Player's turn
    fullBoard = int(input("What board would you like to place on? (1-9) >> "))
    while fullBoard < 1 or fullBoard > 9:
        fullBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    
    currentBoard = fullBoardDict[fullBoard]
    
    individualBoard = int(input("What tile would you like to place on? (1-9) >> "))
    while individualBoard < 1 or individualBoard > 9:
        individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    
    individualBoard = individualBoard - 1
    row = (individualBoard // 3)
    col = (individualBoard % 3)
    
    while currentBoard.layout[row][col] != " ":
        print("That spot is taken!")
        individualBoard = int(input("What tile would you like to place on? (1-9) >> "))
        while individualBoard < 1 or individualBoard > 9:
            individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
        individualBoard = individualBoard - 1
        row = individualBoard // 3
        col = individualBoard % 3
    
    currentBoard.layout[row][col] = currentPlayer
    currentBoard.checkWin()
    
    nextBoardNum = (row * 3) + (col) + 1
    return fullBoardDict[nextBoardNum], nextBoardNum


def makeMove(currentPlayer, currentBoardNum, playerToken, computerToken):
    """Make a move on the specified board"""
    currentBoard = fullBoardDict[currentBoardNum]
    
    if currentBoard.complete:
        printFullBoards()
        return makeFirstMove(currentPlayer, playerToken, computerToken)
    
    if currentPlayer == computerToken:
        # Computer uses minimax
        bestMove = findBestMove(fullBoardDict, currentBoardNum, computerToken, playerToken)
        
        if bestMove:
            boardNum, row, col = bestMove
            currentBoard = fullBoardDict[boardNum]
            currentBoard.layout[row][col] = computerToken
            currentBoard.checkWin()
            
            tileNum = row * 3 + col + 1
            print(f"Computer placed {computerToken} at tile {tileNum}")
            
            nextBoardNum = row * 3 + col + 1
            return fullBoardDict[nextBoardNum], nextBoardNum
        else:
            print("Error: No valid move found")
            return currentBoard, currentBoardNum
    
    # Player's turn
    individualBoard = int(input("What tile would you like to place on? (1-9) >> "))
    while individualBoard < 1 or individualBoard > 9:
        individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    
    individualBoard = individualBoard - 1
    row = (individualBoard // 3)
    col = (individualBoard % 3)
    
    while currentBoard.layout[row][col] != " ":
        individualBoard = int(input("Invalid! Tile already in use >> "))
        while individualBoard < 1 or individualBoard > 9:
            individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
        individualBoard = individualBoard - 1
        row = individualBoard // 3
        col = individualBoard % 3
    
    currentBoard.layout[row][col] = currentPlayer
    currentBoard.checkWin()
    
    nextBoardNum = (row * 3) + (col) + 1
    return fullBoardDict[nextBoardNum], nextBoardNum


SEARCH_DEPTH = beginning()
playerToken, computerToken, firstMove = setup()
setupOutput(playerToken, computerToken, firstMove)

if firstMove:
    currentPlayer = playerToken
else:
    currentPlayer = computerToken

printFullBoards()
currentBoard, currentBoardNum = makeFirstMove(currentPlayer, playerToken, computerToken)

while not gameWon:
    # Switch player
    if currentPlayer == playerToken:
        currentPlayer = computerToken
    else:
        currentPlayer = playerToken
    
    printFullBoards()
    
    # Find and print which board is active
    for num, board in fullBoardDict.items():
        if board is fullBoardDict[currentBoardNum]:
            print(f">>> PLAYING ON BOARD {num} <<<")
            break
    
    currentBoard, currentBoardNum = makeMove(currentPlayer, currentBoardNum, playerToken, computerToken)
    
    if currentBoard.complete:
        printFullBoards()
        currentBoard, currentBoardNum = makeFirstMove(currentPlayer, playerToken, computerToken)
    
    gameWon = checkFullWin(gameWon)