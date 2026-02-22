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

pygame.display.set_caption('Ultimate Tic Tac Toe')


class interactiveBoard:
    def __init__(self, boardNum, x, y):
        self.boardNum = boardNum
        self.x = x
        self.y = y

    def clicked(self, clickPos, currentPlayer):
        if self.x < clickPos[0] < self.x + MAX_SIZE and self.y < clickPos[1] < self.y + MAX_SIZE:
            cx = self.x + SMALL_SIZE // 2
            cy = self.y + SMALL_SIZE // 2
            if currentPlayer == "X":
                drawX(cx, cy)
            else:
                drawO(cx, cy)


class Board:
    def __init__(self, complete, winner, layout):
        self.complete = complete
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
        for i in range(3):
            if self.layout[i][0] == self.layout[i][1] == self.layout[i][2] != " ":
                self.complete = True
                self.winner = self.layout[i][0]
                for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
                return

        for j in range(3):
            if self.layout[0][j] == self.layout[1][j] == self.layout[2][j] != " ":
                self.complete = True
                self.winner = self.layout[0][j]
                for x in range(3):
                    for y in range(3):
                        self.layout[x][y] = self.winner
                return

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

        if self.complete == False:
            count = sum(1 for i in range(3) for j in range(3) if self.layout[i][j] != " ")
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


fullBoardDict = {
    1: boardTL,
    2: boardTM,
    3: boardTR,
    4: boardML,
    5: boardMM,
    6: boardMR,
    7: boardBL,
    8: boardBM,
    9: boardBR
}


def startUp():
    completeStartUp = False
    chosenDifficulty = None
    chosenToken = None
    diffBoxes = []
    tokenBoxes = []
    diffLabels = ["1", "2", "3", "4", "5"]

    def drawScreen():
        screen.fill("Grey")

        title, titleRect = write("Welcome to Ultimate Tic Tac Toe!", 20, 20, "Black")
        screen.blit(title, titleRect)

        diffLabel, diffLabelRect = write("Choose Difficulty:", 100, HEIGHT - 270, "Black")
        screen.blit(diffLabel, diffLabelRect)

        for i in range(5):
            r = pygame.Rect(165 + (150 * i), HEIGHT - 200, 150, 150)
            diffBoxes.append(r)
            pygame.draw.rect(screen, "Grey", r, 0)
            pygame.draw.rect(screen, (0, 0, 0), r, 2)
            numText, numRect = write(diffLabels[i], r.x + 65, r.y + 60, "Black")
            screen.blit(numText, numRect)

        tokenLabel, tokenLabelRect = write("Choose X or O:", 100, 100, "Black")
        screen.blit(tokenLabel, tokenLabelRect)

        for i, token in enumerate(["X", "O"]):
            r = pygame.Rect(400 + i * 160, 150, 120, 120)
            tokenBoxes.append(r)
            pygame.draw.rect(screen, "Grey", r, 0)
            pygame.draw.rect(screen, (0, 0, 0), r, 2)
            t, tr = write(token, r.x + 48, r.y + 45, "Black")
            screen.blit(t, tr)

        pygame.display.flip()

    drawScreen()

    while not completeStartUp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos

                for i in range(5):
                    rect = diffBoxes[i]
                    if rect.x < mouseX < rect.x + rect.width and rect.y < mouseY < rect.y + rect.height:
                        chosenDifficulty = i + 1
                        for j, r in enumerate(diffBoxes):
                            boxColor = (255, 30, 30) if j == i else "Grey"
                            pygame.draw.rect(screen, boxColor, r, 0)
                            pygame.draw.rect(screen, (0, 0, 0), r, 2)
                            numText, numRect = write(diffLabels[j], r.x + 65, r.y + 60, "Black")
                            screen.blit(numText, numRect)
                        print(f"Difficulty: {chosenDifficulty}")

                for i, token in enumerate(["X", "O"]):
                    rect = tokenBoxes[i]
                    if rect.x < mouseX < rect.x + rect.width and rect.y < mouseY < rect.y + rect.height:
                        chosenToken = token
                        for j, r in enumerate(tokenBoxes):
                            boxColor = (255, 30, 30) if j == i else "Grey"
                            pygame.draw.rect(screen, boxColor, r, 0)
                            pygame.draw.rect(screen, (0, 0, 0), r, 2)
                            t, tr = write(["X", "O"][j], r.x + 48, r.y + 45, "Black")
                            screen.blit(t, tr)
                        print(f"Token: {chosenToken}")

                pygame.display.flip()

                if chosenDifficulty and chosenToken:
                    completeStartUp = True

    return chosenDifficulty, chosenToken


def write(text, x, y, color):
    surface = fontObj.render(text, True, pygame.Color(color))
    rect = surface.get_rect(topleft=(x, y))
    return surface, rect


def drawBoard():
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (0, 0, 0), (i * MAX_SIZE + SPREAD, j * MAX_SIZE + SPREAD, MAX_SIZE, MAX_SIZE), 2)


def drawX(cx, cy):
    pygame.draw.line(screen, (255, 0, 0), (cx - 20, cy - 20), (cx + 20, cy + 20), width=3)
    pygame.draw.line(screen, (255, 0, 0), (cx - 20, cy + 20), (cx + 20, cy - 20), width=3)


def drawO(cx, cy):
    pygame.draw.circle(screen, (0, 0, 255), (cx, cy), 20, width=3)


def drawBigX(bigNum):
    bigRow = (bigNum - 1) // 3
    bigCol = (bigNum - 1) % 3
    cx = SPREAD + bigCol * MAX_SIZE + MAX_SIZE // 2
    cy = SPREAD + bigRow * MAX_SIZE + MAX_SIZE // 2
    pygame.draw.line(screen, (255, 0, 0), (cx - 60, cy - 60), (cx + 60, cy + 60), width=4)
    pygame.draw.line(screen, (255, 0, 0), (cx - 60, cy + 60), (cx + 60, cy - 60), width=4)
    
    
def drawBigO(bigNum):
    bigRow = (bigNum - 1) // 3
    bigCol = (bigNum - 1) % 3
    cx = SPREAD + bigCol * MAX_SIZE + MAX_SIZE // 2
    cy = SPREAD + bigRow * MAX_SIZE + MAX_SIZE // 2
    pygame.draw.circle(screen, (0, 0, 255), (cx, cy), 60, width=4)


def winningLine(lineType, index):
    if lineType == "row":
        pygame.draw.line(screen, (0, 0, 0), (SPREAD + 10, SPREAD + index * MAX_SIZE + MAX_SIZE // 2), ((SPREAD + MAX_SIZE * 3) - 10, SPREAD + index * MAX_SIZE + MAX_SIZE // 2), width=8)
    
    elif lineType == "col":
        pygame.draw.line(screen, (0, 0, 0), (SPREAD + index * MAX_SIZE + MAX_SIZE // 2, SPREAD + 10), (SPREAD + index * MAX_SIZE + MAX_SIZE // 2, SPREAD + MAX_SIZE * 3 - 10), width=8)
    
    elif lineType == "diag":
        if index == 1:
            pygame.draw.line(screen, (0, 0, 0), (SPREAD+10, SPREAD+10), ((SPREAD + MAX_SIZE * 3) - 10, (SPREAD + MAX_SIZE * 3) - 10), width=8)
        else:
            pygame.draw.line(screen, (0, 0, 0), (SPREAD + MAX_SIZE * 3 - 10, SPREAD + 10), (SPREAD + 10, SPREAD + MAX_SIZE * 3 - 10), width=8)
            
    
    pygame.display.flip()


def drawSidePanel(currentBoardNum):
    panelX = (SPREAD * 2) + (MAX_SIZE * 3)
    diffText, diffRect = write(f"AI Level: {SEARCH_DEPTH}", panelX, int(HEIGHT * 0.25), "Black")
    screen.blit(diffText, diffRect)
    boardText, boardRect = write(f"Board: {currentBoardNum}", panelX, int(HEIGHT * 0.35), "Black")
    screen.blit(boardText, boardRect)
    gameWinner = checkGameWinner(fullBoardDict)
    if gameWinner:
        winText, winRect = write(f"Winner: {gameWinner}", panelX, int(HEIGHT * 0.45), "Black")
        screen.blit(winText, winRect)
    turnText, turnRect = write(f"{currentPlayer} is playing!", panelX, int(HEIGHT * 0.15), "Black")
    screen.blit(turnText, turnRect)


def renderBoards(currentBoardNum):
    screen.fill("Grey")
    drawSidePanel(currentBoardNum)
    drawBoard()

    for bigNum in range(1, 10):
        board = fullBoardDict[bigNum]
        bigRow = (bigNum - 1) // 3
        bigCol = (bigNum - 1) % 3
        bigX = SPREAD + bigCol * MAX_SIZE
        bigY = SPREAD + bigRow * MAX_SIZE
        
        if board.complete:
            if board.winner == "X":
                drawBigX(bigNum)
            else:
                drawBigO(bigNum)

        else:
            for row in range(3):
                for col in range(3):
                    cellX = bigX + col * SMALL_SIZE
                    cellY = bigY + row * SMALL_SIZE
                    pygame.draw.rect(screen, (0, 0, 0), (cellX, cellY, SMALL_SIZE, SMALL_SIZE), 1)
                    token = board.layout[row][col]
                    cx = cellX + SMALL_SIZE // 2
                    cy = cellY + SMALL_SIZE // 2
                    if token == "X":
                        drawX(cx, cy)
                    elif token == "O":
                        drawO(cx, cy)

    pygame.display.flip()



def copyGameState(fullBoardDict):
    newDict = {}
    for key in fullBoardDict:
        board = fullBoardDict[key]
        newLayout = [row[:] for row in board.layout]
        newDict[key] = Board(board.complete, board.winner, newLayout)
    return newDict


def checkGameWinner(boardDict):
    for i in range(3):
        if (boardDict[i*3+1].winner == boardDict[i*3+2].winner == boardDict[i*3+3].winner != " "
                and boardDict[i*3+1].winner != "TIE"):
            return boardDict[i*3+1].winner

    for j in range(3):
        if (boardDict[j+1].winner == boardDict[j+4].winner == boardDict[j+7].winner != " "
                and boardDict[j+1].winner != "TIE"):
            return boardDict[j+1].winner

    if (boardDict[1].winner == boardDict[5].winner == boardDict[9].winner != " "
            and boardDict[1].winner != "TIE"):
        return boardDict[1].winner

    if (boardDict[3].winner == boardDict[5].winner == boardDict[7].winner != " "
            and boardDict[3].winner != "TIE"):
        return boardDict[3].winner

    if all(boardDict[i].complete for i in range(1, 10)):
        return "TIE"

    return None


def getValidMoves(boardDict, currentBoardNum):
    moves = []

    if currentBoardNum is None or boardDict[currentBoardNum].complete:
        for boardNum in range(1, 10):
            if not boardDict[boardNum].complete:
                board = boardDict[boardNum]
                for bigRow in range(3):
                    for bigCol in range(3):
                        if board.layout[bigRow][bigCol] == " ":
                            moves.append((boardNum, bigRow, bigCol))
    else:
        board = boardDict[currentBoardNum]
        for bigRow in range(3):
            for bigCol in range(3):
                if board.layout[bigRow][bigCol] == " ":
                    moves.append((currentBoardNum, bigRow, bigCol))

    return moves


def evaluateGameState(boardDict, computerToken, playerToken):
    score = 0

    winner = checkGameWinner(boardDict)
    if winner == computerToken:
        return 1000
    elif winner == playerToken:
        return -1000
    elif winner == "TIE":
        return 0

    for boardNum in range(1, 10):
        if boardDict[boardNum].winner == computerToken:
            score += 10
        elif boardDict[boardNum].winner == playerToken:
            score -= 10

    if boardDict[5].winner == computerToken:
        score += 3
    elif boardDict[5].winner == playerToken:
        score -= 3

    for corner in [1, 3, 7, 9]:
        if boardDict[corner].winner == computerToken:
            score += 2
        elif boardDict[corner].winner == playerToken:
            score -= 2

    return score


def minimax(boardDict, currentBoardNum, depth, maxDepth, isMaximizing, computerToken, playerToken):
    winner = checkGameWinner(boardDict)
    if winner is not None:
        return evaluateGameState(boardDict, computerToken, playerToken), None

    if depth >= maxDepth:
        return evaluateGameState(boardDict, computerToken, playerToken), None

    validMoves = getValidMoves(boardDict, currentBoardNum)

    if not validMoves:
        return evaluateGameState(boardDict, computerToken, playerToken), None

    bestMove = None

    if isMaximizing:
        maxScore = -float('inf')
        for move in validMoves:
            boardNum, bigRow, bigCol = move
            newBoardDict = copyGameState(boardDict)
            nextBoardNum = applyMove(newBoardDict, boardNum, bigRow, bigCol, computerToken)
            score, _ = minimax(newBoardDict, nextBoardNum, depth + 1, maxDepth, False, computerToken, playerToken)
            if score > maxScore:
                maxScore = score
                bestMove = move
        return maxScore, bestMove

    else:
        minScore = float('inf')
        for move in validMoves:
            boardNum, bigRow, bigCol = move
            newBoardDict = copyGameState(boardDict)
            nextBoardNum = applyMove(newBoardDict, boardNum, bigRow, bigCol, playerToken)
            score, _ = minimax(newBoardDict, nextBoardNum, depth + 1, maxDepth, True, computerToken, playerToken)
            if score < minScore:
                minScore = score
                bestMove = move
        return minScore, bestMove


def findBestMove(fullBoardDict, currentBoardNum, computerToken, playerToken):
    score, bestMove = minimax(fullBoardDict, currentBoardNum, 0, SEARCH_DEPTH, True, computerToken, playerToken)
    return bestMove


def applyMove(boardDict, boardNum, bigRow, bigCol, token):
    boardDict[boardNum].layout[bigRow][bigCol] = token
    boardDict[boardNum].checkWin()
    nextBoardNum = bigRow * 3 + bigCol + 1
    return nextBoardNum


def checkFullWin(gameWon):
    for i in range(3):
        if (fullBoardDict[i*3+1].winner == fullBoardDict[i*3+2].winner == fullBoardDict[i*3+3].winner != " "
                and fullBoardDict[i*3+1].winner != "TIE"):
            print(f"{fullBoardDict[i*3+1].winner} wins the game!")
            winningLine("row", i)
            return True

    for j in range(3):
        if (fullBoardDict[j+1].winner == fullBoardDict[j+4].winner == fullBoardDict[j+7].winner != " "
                and fullBoardDict[j+1].winner != "TIE"):
            print(f"{fullBoardDict[j+1].winner} wins the game!")
            winningLine("col", j)
            return True

    if (fullBoardDict[1].winner == fullBoardDict[5].winner == fullBoardDict[9].winner != " "
            and fullBoardDict[1].winner != "TIE"):
        print(f"{fullBoardDict[1].winner} wins the game!")
        winningLine("diag", 1)
        return True

    if (fullBoardDict[3].winner == fullBoardDict[5].winner == fullBoardDict[7].winner != " "
            and fullBoardDict[3].winner != "TIE"):
        print(f"{fullBoardDict[3].winner} wins the game!")
        winningLine("diag", 2)
        return True

    return False


def printFullBoards():
    top    = [boardTL.getRows(), boardTM.getRows(), boardTR.getRows()]
    middle = [boardML.getRows(), boardMM.getRows(), boardMR.getRows()]
    bottom = [boardBL.getRows(), boardBM.getRows(), boardBR.getRows()]

    allSections = [top, middle, bottom]

    print()
    for sectionIndex, section in enumerate(allSections):
        for bigRow in range(3):
            print(section[0][bigRow] + " # " + section[1][bigRow] + " # " + section[2][bigRow])
            if bigRow < 2:
                print("---------" + " # " + "---------" + " # " + "---------")
        if sectionIndex < 2:
            print("# # # # # # # # # # # # # # # # #")
    print("\n\n")


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
            boardNum, bigRow, bigCol = bestMove
            currentBoard = fullBoardDict[boardNum]
            currentBoard.layout[bigRow][bigCol] = computerToken
            currentBoard.checkWin()
            nextBoardNum = bigRow * 3 + bigCol + 1
            print(f"Computer chose board {boardNum}, tile {nextBoardNum}")
            renderBoards(nextBoardNum)
            return fullBoardDict[nextBoardNum], nextBoardNum
        else:
            boardNum = random.choice([n for n in range(1, 10) if not fullBoardDict[n].complete])
            currentBoard = fullBoardDict[boardNum]
            availableSpots = [(r, c) for r in range(3) for c in range(3) if currentBoard.layout[r][c] == " "]
            bigRow, bigCol = random.choice(availableSpots)
            currentBoard.layout[bigRow][bigCol] = computerToken
            currentBoard.checkWin()
            nextBoardNum = bigRow * 3 + bigCol + 1
            renderBoards(nextBoardNum)
            return fullBoardDict[nextBoardNum], nextBoardNum

    print("Click any cell for your first move.")
    bigNum, bigRow, bigCol = waitForPlayerClick(None)
    fullBoardDict[bigNum].layout[bigRow][bigCol] = currentPlayer
    fullBoardDict[bigNum].checkWin()
    nextBoardNum = bigRow * 3 + bigCol + 1
    renderBoards(nextBoardNum)
    return fullBoardDict[nextBoardNum], nextBoardNum


def makeMove(currentPlayer, currentBoardNum, playerToken, computerToken):
    currentBoard = fullBoardDict[currentBoardNum]

    if currentBoard.complete:
        return makeFirstMove(currentPlayer, playerToken, computerToken)

    if currentPlayer == computerToken:
        bestMove = findBestMove(fullBoardDict, currentBoardNum, computerToken, playerToken)

        if bestMove:
            boardNum, bigRow, bigCol = bestMove
            currentBoard = fullBoardDict[boardNum]
            currentBoard.layout[bigRow][bigCol] = computerToken
            currentBoard.checkWin()
            nextBoardNum = bigRow * 3 + bigCol + 1
            print(f"Computer placed {computerToken} at tile {nextBoardNum}")
            renderBoards(nextBoardNum)
            return fullBoardDict[nextBoardNum], nextBoardNum
        else:
            print("Error: No valid move found")
            return currentBoard, currentBoardNum

    print(f"Click a cell on board {currentBoardNum}.")
    bigNum, bigRow, bigCol = waitForPlayerClick(currentBoardNum)
    fullBoardDict[bigNum].layout[bigRow][bigCol] = currentPlayer
    fullBoardDict[bigNum].checkWin()
    nextBoardNum = bigRow * 3 + bigCol + 1
    renderBoards(nextBoardNum)
    return fullBoardDict[nextBoardNum], nextBoardNum



SEARCH_DEPTH, playerToken = startUp()
if playerToken == "X":
    computerToken = "O"
else:
    computerToken = "X"

if SEARCH_DEPTH == 5:
    currentPlayer = playerToken
else:
    currentPlayer = random.choice([playerToken, computerToken])

renderBoards(None)
currentBoard, currentBoardNum = makeFirstMove(currentPlayer, playerToken, computerToken)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not gameWon:
        currentPlayer = computerToken if currentPlayer == playerToken else playerToken

        for num, board in fullBoardDict.items():
            if board is fullBoardDict[currentBoardNum]:
                print(f">>> PLAYING ON BOARD {num} <<<")
                break

        currentBoard, currentBoardNum = makeMove(currentPlayer, currentBoardNum, playerToken, computerToken)

    renderBoards(currentBoardNum)
    gameWon = checkFullWin(gameWon)
    if gameWon:
        running = False
time.sleep(30)

#test
print("test")