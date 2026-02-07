import random
import time

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
                        return
                    
def checkFullWin(gameWon):
    #checks rows
    for i in range(3):
            if fullBoardDict[i+1].winner == fullBoardDict[i+1].winner == fullBoardDict[i+1].winner != " " and fullBoardDict[i+1].winner != "TIE":
                gameWon = True
                print(f"{fullBoardDict[i+1].winner} wins the game!")
                return gameWon
    
    #checks columns
    for j in range(3):
        if fullBoardDict[j+1].winner == fullBoardDict[j+4].winner == fullBoardDict[j+7].winner != " " and fullBoardDict[j+1].winner != "TIE":
            gameWon = True
            print(f"{fullBoardDict[j+1].winner} wins the game!")
            return gameWon
    
    #checks diagonals
    if fullBoardDict[1].winner == fullBoardDict[5].winner == fullBoardDict[9].winner != " " and fullBoardDict[1].winner != "TIE":
        gameWon = True
        print(f"{fullBoardDict[1].winner} wins the game!")
        return gameWon
    
    if fullBoardDict[3].winner == fullBoardDict[5].winner == fullBoardDict[7].winner != " " and fullBoardDict[3].winner != "TIE":
        gameWon = True
        print(f"{fullBoardDict[3].winner} wins the game!")
        return gameWon
                





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
            # Add separator lines within each grid (between rows)
            if rowIndex < 2:
                print("---------" + " # " + "---------" + " # " + "---------")
        
        # Only print hashtag separator between sections, not after the last one
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



def makeFirstMove(currentPlayer):
    fullBoard = int(input("What board would you like to place on? (1-9) >> "))
    while fullBoard < 1 or fullBoard > 9 or len(str(fullBoard)) != 1:
        fullBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    currentBoard = fullBoardDict[fullBoard]
    
    individualBoard = int(input("What tile would you like to place on? (1-9) >> "))
    while individualBoard < 1 or individualBoard > 9 or len(str(individualBoard)) != 1:
        individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    individualBoard = individualBoard - 1
    row = (individualBoard // 3)
    columb = (individualBoard % 3)
    currentBoard.layout[row][columb] = currentPlayer
    
    # Check if this move won the board
    currentBoard.checkWin()

    currentBoard = fullBoardDict[(row * 3) + (columb)+1]
    
    return currentBoard


    
def makeMove(currentPlayer, currentBoard):
    if currentBoard.complete == True:
        printFullBoards()
        currentBoard = makeFirstMove(currentPlayer)
    else:
        individualBoard = int(input("What tile would you like to place on? (1-9) >> "))
        while individualBoard < 1 or individualBoard > 9 or len(str(individualBoard)) != 1:
            individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
        individualBoard = individualBoard - 1
        row = (individualBoard // 3)
        columb = (individualBoard % 3)
        while currentBoard.layout[row][columb] != " ":
            individualBoard = int(input("Invalid! Tile already in use >> "))
            while individualBoard < 1 or individualBoard > 9 or len(str(individualBoard)) != 1:
                individualBoard = int(input("Invalid! Enter between 1 and 9 >> "))
            individualBoard = individualBoard - 1
            row = individualBoard // 3
            columb = individualBoard % 3
        currentBoard.layout[row][columb] = currentPlayer
    
    currentBoard.checkWin()

    currentBoard = fullBoardDict[(row * 3) + (columb)+1]

    return currentBoard
    
    
#playerToken = "X"
#computerToken = "O"
#firstMove = True

playerToken, computerToken, firstMove = setup()
setupOutput(playerToken, computerToken, firstMove)
if firstMove == True:
    currentPlayer = playerToken
else:
    currentPlayer = computerToken

printFullBoards()
currentBoard = makeFirstMove(currentPlayer)

while not(gameWon):
    if currentPlayer == playerToken:
        currentPlayer = computerToken
    else:
        currentPlayer = playerToken
    printFullBoards()
    currentBoard = makeMove(currentPlayer, currentBoard)
    if currentBoard.complete == True:
        printFullBoards()
        currentBoard = makeFirstMove(currentPlayer)
    gameWon = checkFullWin(gameWon)