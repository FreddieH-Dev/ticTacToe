import pygame
import random
import time

SEARCH_DEPTH = None
gameWon = False

HEIGHT = 720
WIDTH = 1080
MAX_SIZE = 210
SMALL_SIZE = MAX_SIZE // 3
SPREAD = (HEIGHT - (MAX_SIZE * 3)) // 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

pygame.font.init()
fontObj = pygame.font.Font('freesansbold.ttf', 32)

pygame.display.set_caption('Tic Tac Toe')

def startUp():
    completeStartUp = False
    chosenDifficulty = None
    chosenToken = None

    def drawScreen():
        screen.fill("Grey")

        title, titleRect = write("Welcome to Ultimate Tic Tac Toe!", 20, 20, "Black")
        screen.blit(title, titleRect)

        diffLabel, diffLabelRect = write("Choose Difficulty:", 100, HEIGHT-270, "Black")
        screen.blit(diffLabel, diffLabelRect)

        for i in range(5):
            r = pygame.Rect(165+(150*i), HEIGHT-200, 150, 150)
            diffBoxes.append(r)
            pygame.draw.rect(screen, "Grey", r, 0)
            pygame.draw.rect(screen, (0,0,0), r, 2)
            numText, numRect = write(str(i+1), r.x+65, r.y+60, "Black")
            screen.blit(numText, numRect)

        tokenLabel, tokenLabelRect = write("Choose X or O:", 100, 100, "Black")
        screen.blit(tokenLabel, tokenLabelRect)

        # X and O boxes
        for i in list(["X", "O"]):
            r = pygame.Rect(400 + list(["X", "O"]).index(i)*160, 150, 120, 120)
            tokenBoxes.append(r)
            pygame.draw.rect(screen, "Grey", r, 0)
            pygame.draw.rect(screen, (0,0,0), r, 2)
            t, tr = write(i, r.x+47, r.y+38, "Black")
            screen.blit(t, tr)

        pygame.display.flip()

    diffBoxes = []
    tokenBoxes = []
    drawScreen()

    while not completeStartUp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos

                # Check difficulty boxes
                for i in range(5):
                    rect = diffBoxes[i]
                    if rect.x < mouseX < rect.x + rect.width and rect.y < mouseY < rect.y + rect.height:
                        chosenDifficulty = i + 1
                        # Redraw all diff boxes, highlight chosen
                        for j, r in enumerate(diffBoxes):
                            color = (255, 30, 30) if j == i else "Grey"
                            pygame.draw.rect(screen, color, r, 0)
                            pygame.draw.rect(screen, (0,0,0), r, 2)
                            num, numRect = write(str(j+1), r.x+65, r.y+60, "Black")
                            screen.blit(num, numRect)
                        print(f"Difficulty: {chosenDifficulty}")

                # Check token boxes
                for i in range(2):
                    rect = tokenBoxes[i]
                    if rect.x < mouseX < rect.x + rect.width and rect.y < mouseY < rect.y + rect.height:
                        chosenToken = ["X", "O"][i]
                        # Redraw both token boxes, highlight chosen
                        for j, r in enumerate(tokenBoxes):
                            color = (255, 30, 30) if j == i else "Grey"
                            pygame.draw.rect(screen, color, r, 0)
                            pygame.draw.rect(screen, (0,0,0), r, 2)
                            t, tr = write(["X","O"][j], r.x+47, r.y+38, "Black")
                            screen.blit(t, tr)
                        print(f"Token: {chosenToken}")

                pygame.display.flip()

                if chosenDifficulty and chosenToken:
                    completeStartUp = True

    return chosenDifficulty, chosenToken


def drawBoard(MAX_SIZE):
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (0, 0, 0), (i*MAX_SIZE+SPREAD, j*MAX_SIZE+SPREAD, MAX_SIZE, MAX_SIZE), 2)
            
def drawX(x, y):
    pygame.draw.line(screen, (255, 0, 0), (x-50,y-50), (x+50, y+50), width=3)
    pygame.draw.line(screen, (255, 0, 0), (x-50,y+50), (x+50, y-50), width=3)

def drawO(x, y):
    pygame.draw.circle(screen, (0, 0, 255), (x + MAX_SIZE//2, y + MAX_SIZE//2), 50, width=3)

class interactiveBoard:
    def __init__(self, boardNum, x, y):
        self.boardNum = boardNum
        self.x = x
        self.y = y
        
    def clicked(self, clickPos, currentPlayer):
        if clickPos[0] > self.x and clickPos[0] < self.x + MAX_SIZE and clickPos[1] > self.y and clickPos[1] < self.y + MAX_SIZE:
            if currentPlayer == "X":
                drawX(self.x + SMALL_SIZE//2, self.y + SMALL_SIZE//2)
            else:
                drawO(self.x + SMALL_SIZE//2, self.y + SMALL_SIZE//2)
        


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
    
boardTL = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardTM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardTR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardML = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardMM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardMR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBL = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBM = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
boardBR = Board(False, " ", [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])


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


def minimax(boardDict, currentBoardNum, depth, maxDepth, isMaximizing, 
            computerToken, playerToken):
    
    
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


def write(onScreenText, x, y, color):
    surface = fontObj.render(onScreenText, True, pygame.Color(color))
    rect = surface.get_rect(topleft=(x, y))
    return surface, rect

def onScreenText(currentBoardNum):
    script = f"Current Board: {currentBoardNum}\nAI level: {SEARCH_DEPTH}\nWinner: {checkGameWinner(fullBoardDict)}\n"
    onScreenText, onScreenTextRect = write(script, (SPREAD*2) + (MAX_SIZE * 3), HEIGHT * 0.25, "Black")
    screen.blit(onScreenText, onScreenTextRect)
    

def renderBoards(currentBoardNum):
    screen.fill("Grey")
    onScreenText(currentBoardNum)
    drawBoard(MAX_SIZE)
    for bigNum in range(1, 10):
        board = fullBoardDict[bigNum]
        bigRow = (bigNum - 1) // 3
        bigCol = (bigNum - 1) % 3
        bigX = SPREAD + bigCol * MAX_SIZE
        bigY = SPREAD + bigRow * MAX_SIZE
        for row in range(3):
            for col in range(3):
                cellX = bigX + col * SMALL_SIZE
                cellY = bigY + row * SMALL_SIZE
                pygame.draw.rect(screen, (0, 0, 0), (cellX, cellY, SMALL_SIZE, SMALL_SIZE), 1)
                token = board.layout[row][col]
                cx = cellX + SMALL_SIZE // 2
                cy = cellY + SMALL_SIZE // 2
                if token == "X":
                    pygame.draw.line(screen, (255, 0, 0), (cx-20, cy-20), (cx+20, cy+20), width=3)
                    pygame.draw.line(screen, (255, 0, 0), (cx-20, cy+20), (cx+20, cy-20), width=3)
                elif token == "O":
                    pygame.draw.circle(screen, (0, 0, 255), (cx, cy), 20, width=3)
    pygame.display.flip()


def waitForPlayerClick(currentBoardNum):
    while True:
        renderBoards(currentBoardNum)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                if mouseX < SPREAD or mouseY < SPREAD:
                    continue
                if mouseX > SPREAD + MAX_SIZE * 3 or mouseY > SPREAD + MAX_SIZE * 3:
                    continue
                bigCol = (mouseX - SPREAD) // MAX_SIZE
                bigRow = (mouseY - SPREAD) // MAX_SIZE
                if bigCol > 2 or bigRow > 2:
                    continue
                bigNum = bigRow * 3 + bigCol + 1
                localX = (mouseX - SPREAD) % MAX_SIZE
                localY = (mouseY - SPREAD) % MAX_SIZE
                col = localX // SMALL_SIZE
                row = localY // SMALL_SIZE
                if col > 2 or row > 2:
                    continue
                # Validate the move
                if currentBoardNum is not None and not fullBoardDict[currentBoardNum].complete:
                    if bigNum != currentBoardNum:
                        print(f"You must play on board {currentBoardNum}!")
                        continue
                if fullBoardDict[bigNum].complete:
                    print("That board is already complete!")
                    continue
                if fullBoardDict[bigNum].layout[row][col] != " ":
                    print("That cell is already taken!")
                    continue
                return bigNum, row, col
        clock.tick(60)


def makeFirstMove(currentPlayer, playerToken, computerToken):
    if currentPlayer == computerToken:
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
            renderBoards(nextBoardNum)
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
            renderBoards(None)
            return fullBoardDict[nextBoardNum], nextBoardNum
    
    print("Click any cell for your first move.")
    bigNum, row, col = waitForPlayerClick(None)
    fullBoardDict[bigNum].layout[row][col] = currentPlayer
    fullBoardDict[bigNum].checkWin()
    nextBoardNum = row * 3 + col + 1
    renderBoards(None)
    return fullBoardDict[nextBoardNum], nextBoardNum


def makeMove(currentPlayer, currentBoardNum, playerToken, computerToken):
    """Make a move on the specified board"""
    currentBoard = fullBoardDict[currentBoardNum]
    
    if currentBoard.complete:
        #printFullBoards()
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
            renderBoards(nextBoardNum)
            return fullBoardDict[nextBoardNum], nextBoardNum
        else:
            print("Error: No valid move found")
            return currentBoard, currentBoardNum
    
    # Player's turn — click a valid cell on the current board
    print(f"Click a cell on board {currentBoardNum}.")
    bigNum, row, col = waitForPlayerClick(currentBoardNum)
    fullBoardDict[bigNum].layout[row][col] = currentPlayer
    fullBoardDict[bigNum].checkWin()
    nextBoardNum = row * 3 + col + 1
    renderBoards(nextBoardNum)
    return fullBoardDict[nextBoardNum], nextBoardNum


SEARCH_DEPTH = 3
playerToken = "X"
computerToken = "O"
firstMove = False




if firstMove:
    currentPlayer = playerToken
else:
    currentPlayer = computerToken

#printFullBoards()

SEARCH_DEPTH, playerToken = startUp()
if playerToken == "X":
    computerToken = "O"
else:    
    computerToken = "X"

renderBoards(None)
currentBoard, currentBoardNum = makeFirstMove(currentPlayer, playerToken, computerToken)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not gameWon:
        # Switch player
        if currentPlayer == playerToken:
            currentPlayer = computerToken
        else:
            currentPlayer = playerToken
        
        #printFullBoards()
        
        # Find and print which board is active
        for num, board in fullBoardDict.items():
            if board is fullBoardDict[currentBoardNum]:
                print(f">>> PLAYING ON BOARD {num} <<<")
                break
        
        currentBoard, currentBoardNum = makeMove(currentPlayer, currentBoardNum, playerToken, computerToken)
        
        if currentBoard.complete:
            #printFullBoards()
            currentBoard, currentBoardNum = makeFirstMove(currentPlayer, playerToken, computerToken)
        
        gameWon = checkFullWin(gameWon)

    renderBoards(currentBoardNum)
    clock.tick(60)

pygame.quit()