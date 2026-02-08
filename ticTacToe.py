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
        print("\nGood luck and have fun playing!")

def setup():
    print()
    player1Token = int(input("Would you rather be X or O? (1,2): >> "))
    while player1Token != 1 and player1Token != 2:
        player1Token = int(input("Invalid input. Please enter 1 for X or 2 for O: >> "))
    if player1Token == 1:
        player1Token = "X"
        player2Token = "O"
    else:
        player1Token = "O"
        player2Token = "X"
    
    coinFlip = random.randint(1,2)
    if coinFlip == 1:
        return player1Token, player2Token, True
    else:
        return player1Token, player2Token, False


    
def setupOutput(player1Token, player2Token, firstMove):
    print(f"player 1 is playing as: {player1Token}")
    print(f"player 2 is playing as: {player2Token}")

    print()

    print("Flipping a coin to see who goes first.",end='')
    for wait in range(5):
        time.sleep(0.5)
        print(".",end='')

    print()

    if firstMove:
        print("player 1 is playing first!")
    else:
        print("player 2 is playing first!")

    time.sleep(1)
    print("\n\n")



def makeFirstMove(currentPlayer):
    fullBoard = int(input("What board would you like to place on? (1-9) >> "))
    while fullBoard < 1 or fullBoard > 9 or len(str(fullBoard)) != 1:
        fullBoard = int(input("Invalid! Enter between 1 and 9 >> "))
    currentBoard = fullBoardDict[fullBoard]
    while currentBoard.complete == True:
        fullBoard = int(input("Invalid! Board already won or full. Enter between 1 and 9 >> "))
        while fullBoard < 1 or fullBoard > 9 or len(str(fullBoard)) != 1:
            fullBoard = int(input("Invalid! Enter between 1 and 9 >> "))
        currentBoard = fullBoardDict[fullBoard]
    
    currentBoard, row, columb = makeMove(currentPlayer, currentBoard)

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

    return currentBoard, row, columb
    
beginning()

player1Token, player2Token, firstMove = setup()

setupOutput(player1Token, player2Token, firstMove)

if firstMove == True:
    currentPlayer = player1Token
else:
    currentPlayer = player2Token

printFullBoards()
currentBoard = makeFirstMove(currentPlayer)

while not(gameWon):
    if currentPlayer == player1Token:
        currentPlayer = player2Token
    else:
        currentPlayer = player1Token

    printFullBoards()

    for num, board in fullBoardDict.items():
        if board is currentBoard:
            print(f">>> PLAYING ON BOARD {num} <<<")
            break
    print(f"Current player: {currentPlayer}\n")

    currentBoard, row, columb = makeMove(currentPlayer, currentBoard)
    