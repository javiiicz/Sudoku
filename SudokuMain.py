from random import *
from tkinter import *
import tkinter.font as tkFont
import time
import tkinter.messagebox as messagebox

# Initialize the solution, game, and button matrices
solution = [[0,0,0,0,0,0,0,0,0] for _ in range(9)]
game = [[0,0,0,0,0,0,0,0,0] for _ in range(9)]
buttons = [[0,0,0,0,0,0,0,0,0] for _ in range(9)]
boxes = [[0,0,0] for _ in range(3)]

currentPos = None
errors = []
hints = []
moves = []
currentMove = -1
isPossible = True

# Fill diagonal sub-grids
def generateDiagonal():
    key = [[0,1,2],[3,4,5],[6,7,8]]
    nums = [1,2,3,4,5,6,7,8,9]
    for k in range(3):
        shuffle(nums)
        counter = 0
        for i in range(3):
            for j in range(3):
                solution[key[k][i]][key[k][j]] = nums[counter]
                counter += 1

# Check if a value can be placed in a row
def checkRow(row, value):
    return value not in solution[row]

# Check if a value can be placed in a column
def checkColumn(col, value):
    return value not in [solution[i][col] for i in range(9)]

# Check if a value can be placed in a sub-grid
def checkBox(row, col, value):
    rowCenter = (row // 3) * 3 + 1
    colCenter = (col // 3) * 3 + 1
    for i in range(-1, 2):
        for j in range(-1, 2):
            if solution[rowCenter + i][colCenter + j] == value:
                return False
    return True

# Find the next empty cell
def findNext():
    for i in range(9):
        for j in range(9):
            if solution[i][j] == 0:
                return [i, j]
    return [-1, -1]

# Solve the Sudoku using backtracking
def solveSudoku():
    coords = findNext()
    i, j = coords
    if i == -1 and j == -1:
        return True
    for num in range(1, 10):
        if checkRow(i, num) and checkColumn(j, num) and checkBox(i, j, num):
            solution[i][j] = num
            if solveSudoku():
                return True
            solution[i][j] = 0
    return False

# Generate a Sudoku puzzle
def generateSudoku():
    for i in range(9):
        for j in range(9):
            solution[i][j] = 0
    generateDiagonal()
    solveSudoku()

# Set the difficulty level by removing some cells
def setDifficulty(level):
    global game, solution
    if level == "easy":
        difficulty = 60
    elif level == "medium":
        difficulty = 45
    elif level == "hard":
        difficulty = 30
    for i in range(9):
        for j in range(9):
            game[i][j] = solution[i][j]
            if randint(1, 100) >= difficulty:
                game[i][j] = 0

# Get the positions of the initial numbers
def getHints():
    global game
    res = []
    for i in range(9):
        for j in range(9):
            if game[i][j] != 0:
                res.append([i, j])
    return res

# Color non-initial buttons gray
def colorNonInitialButtons():
    global hints
    for i in range(9):
        for j in range(9):
            if [i, j] not in hints:
                buttons[i][j].config(fg="#0072e3")

# Update the color of the pressed button and save the position
def buttonPressed(pos):
    global currentPos
    currentPos = pos
    paintCells(pos)

# Paint the cells according to the current position
def paintCells(pos):
    paintNoErrors()
    text = buttons[pos[0]][pos[1]].cget("text")
    box = [pos[0] // 3, pos[1] // 3]
    for i in range(9):
        for j in range(9):
            buttons[i][j].config(bg="white")
    for i in range(9):
        for j in range(9):
            if text:
                if buttons[i][j].cget("text") == text:
                    buttons[i][j].config(bg="#c3d7ea")
            if i == pos[0] or j == pos[1]:
                buttons[i][j].config(bg="#e2ebf3")
            if [i//3, j//3] == box:
                buttons[i][j].config(bg="#e2ebf3")
    buttons[pos[0]][pos[1]].config(bg="#bbdefb")
    paintErrors()

# Record all cells with errors in a list
def recordErrors():
    global errors
    for i in range(9):
        for j in range(9):
            if isError([i, j]) and [i, j] not in errors:
                errors.append([i, j])
            elif not isError([i, j]) and [i, j] in errors:
                errors.remove([i, j])
    updateErrors()

# Paint errors red and reset non-errors
def paintErrors():
    global currentPos, errors
    iPos, jPos = currentPos
    for i in range(9):
        for j in range(9):
            button = buttons[i][j]
            if [i, j] in errors:
                if i == iPos and j == jPos:
                    buttons[iPos][jPos].config(fg="#e06c7e")
                else:
                    button.config(bg="#f7cfd6")

# Reset buttons without errors
def paintNoErrors():
    for i in range(9):
        for j in range(9):
            button = buttons[i][j]
            if [i, j] not in errors:
                button.config(bg="white")
                if [i, j] not in hints:
                    button.config(fg="#0072e3")
                else:
                    button.config(fg="#344861")

# Check if there is an error in the given position
def isError(pos):
    text = buttons[pos[0]][pos[1]].cget("text")
    if not text:
        return False
    for i in range(9):
        for j in range(9):
            if i == pos[0] and j == pos[1]:
                continue
            button = buttons[i][j]
            if button.cget("text") == text and (i == pos[0] or j == pos[1] or [i//3, j//3] == [pos[0]//3, pos[1]//3]):
                return True
    return False

# Set a number in the Sudoku
def setNum(num, event=None, redo=False):
    global currentPos, moves, hints, currentMove
    if currentPos is None:
        return
    i, j = currentPos
    if [i, j] not in hints:
        previousText = buttons[i][j].cget("text")
        newText = str(num)
        buttons[i][j].config(text=newText)
        game[i][j] = num
        if not redo:
            if currentMove < len(moves) - 1:
                moves = moves[:currentMove + 1]
            moves.append([i, j, previousText, newText])
            currentMove += 1
    recordErrors()
    paintCells(currentPos)
    checkWin()

# Undo the last move
def undo():
    global moves, currentMove, currentPos
    if currentMove != -1:
        i, j = moves[currentMove][:2]
        previousText = moves[currentMove][2]
        currentPos = [i, j]
        setNum(previousText, None, True)
        currentMove -= 1

# Redo the last undone move
def redo():
    global moves, currentMove, currentPos
    if currentMove != len(moves) - 1:
        currentMove += 1
        i, j = moves[currentMove][:2]
        newText = moves[currentMove][3]
        currentPos = [i, j]
        setNum(newText, None, True)

# Create a new Sudoku puzzle
def newSudoku(difficulty):
    global game, solution, hints, errors, currentPos, currentMove, moves, isPossible
    generateSudoku()
    setDifficulty(difficulty)
    hints = getHints()
    errors = []
    currentPos = [0, 0]
    currentMove = -1
    moves = []
    isPossible = True
    btnSolve.config(state=DISABLED)
    strSolutions.config(text="")
    for i in range(9):
        for j in range(9):
            buttons[i][j].config(text=str(game[i][j]) if game[i][j] != 0 else "")
    paintCells([0, 0])
    colorNonInitialButtons()
    recordErrors()

# Save a game
def saveGame():
    global game
    file = open("Project 2/sdk.txt", "w")
    for i in range(9):
        for j in range(9):
            file.write(str(game[i][j]))

# Load a game from the "sdk.txt" file
def loadGame():
    global game

    try:
        file = open("Project 2/sdk.txt", "r")
    except:
        return

    file = open("Project 2/sdk.txt", "r")

    content = file.read()
    counter = 0

    for i in range(9):
        for j in range(9):
            char = content[counter]

            try:
                num = int(char)
            except:
                return

            num = int(char)
            game[i][j] = num
            counter += 1
    file.close()
    loadNewSudoku()

# Create the new loaded Sudoku
def loadNewSudoku():
    global game
    global solution
    global hints
    global errors
    global lastMove
    global currentPos
    global currentMove
    global moves
    global isPossible

    hints = getHints()
    errors = []
    lastMove = None
    currentPos = [0, 0]
    currentMove = -1
    moves = []
    isPossible = False
    btnSolve.config(state=DISABLED)
    strSolutions.config(text="")

    for i in range(9):
        for j in range(9):
            if game[i][j] == 0:
                buttons[i][j].config(text="")
            else:
                buttons[i][j].config(text=str(game[i][j]))
            solution[i][j] = game[i][j]

    paintCells([0, 0])
    colorNonInitialButtons()
    checkSolutions()

# Return the number of solutions for a Sudoku
# Returns: a number
def checkSolutions():
    solveSudoku()

    if isValid():
        btnSolve.config(state=NORMAL)
        strSolutions.config(text="The Sudoku has a solution 😁")
    else:
        btnSolve.config(state=DISABLED)
        strSolutions.config(text="The Sudoku has no solution 😔")

# Return True if all cells in the solution are not 0
# Returns: a boolean
def isValid():
    for i in range(9):
        for j in range(9):
            if solution[i][j] == 0:
                return False
    return True

# Solve the Sudoku
def solve():
    global solution
    global hints
    for i in range(9):
        for j in range(9):
            if [i, j] not in hints:
                buttons[i][j].config(text=str(solution[i][j]))
                game[i][j] = solution[i][j]
                window.update()
                time.sleep(0.02)
    recordErrors()
    paintNoErrors()
    checkWin()

# Return True if the game is won
# Returns: a boolean
def isWin():
    for i in range(9):
        for j in range(9):
            if game[i][j] != solution[i][j]:
                return False
    return True

# Display a victory message window
def showWin():
    messagebox.showinfo("Victory", "Congratulations, you won!")

# Check if there is a victory
def checkWin():
    if isWin():
        for i in range(9):
            for j in range(9):
                buttons[i][j].config(fg="#83600d", bg="#f5d560")
        showWin()

# Update the error count display
def updateErrors():
    global errors
    count = len(errors)
    strErrors.config(text=str(count))

# Interface Algorithms =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Generate 9 subframes for the Sudoku boxes
def generateBoxes():
    for i in range(3):
        for j in range(3):
            frame = Frame(mainFrame, bg="#344861", highlightbackground="#344861", highlightthickness=1)
            frame.grid(row=i, column=j)
            boxes[i][j] = frame

# Generate the buttons for the interface
def generateMatrix():
    for i in range(9):
        for j in range(9):
            # Get the value from the logical matrix
            text = str(game[i][j])

            if text == "0":
                text = ""

            # Create the button with white color and the previous text
            btn = Button(boxes[i//3][j//3], text=text, fg="#344861", bg="white", font=myFont, width=2, height=1, relief=FLAT,
                         command=lambda coord=[i,j]: buttonPressed(coord))

            # Place the button in the matrix at position i,j
            btn.grid(row=(i % 3), column=(j % 3), ipadx=15, ipady=15, padx=1, pady=1)
            buttons[i][j] = btn

# Generate the number buttons
def generateNumbers():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    counter = 0
    for i in range(3):
        for j in range(3):
            num = nums[counter]
            btn = Button(numbersFrame, text=num, fg="#0072e3", bg="#eaeef4", font=myFont, width=5, height=1, relief=FLAT,
                         command=lambda num=num: setNum(num))
            btn.grid(row=i, column=j, padx=2, pady=2, ipadx=15, ipady=15)
            counter += 1
    btn = Button(numbersFrame, text="Delete", fg="#0072e3", bg="#eaeef4", font=myFont, relief=FLAT, width=5, height=1,
                 command=lambda num="": setNum(num))
    btn.grid(row=1, column=3, padx=2, pady=2, ipadx=15, ipady=20)

    btn = Button(numbersFrame, text="Undo", fg="#0072e3", bg="#eaeef4", font=myFont, relief=FLAT, width=5, height=1,         # Undo button
                 command=undo)
    btn.grid(row=0, column=3, padx=2, pady=2, ipadx=15, ipady=20)

    btn = Button(numbersFrame, text="Redo", fg="#0072e3", bg="#eaeef4", font=myFont, relief=FLAT, width=5, height=1,         # Redo button
                 command=redo)
    btn.grid(row=2, column=3, padx=2, pady=2, ipadx=15, ipady=20)

# GUI =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
window = Tk()
window.title("My First Window")
window.geometry("1550x800")

myFont = tkFont.Font(family='Bahnschrift', weight="bold", size=15)
myFont2 = tkFont.Font(family='Bahnschrift', size=12)
myFont3 = tkFont.Font(family='Bahnschrift', size=10)
myFont4 = tkFont.Font(family='Neo Sans', size=90, weight="bold", slant="italic")
myFont5 = tkFont.Font(family='Neo Sans', size=15, slant="italic")
myFont6 = tkFont.Font(family='Bahnschrift', size=30)

# Title
Label(window, text="😲SUDOKU😨", font=myFont4, fg="#344861", justify="left").place(x=700, y=20)
Label(window, text="Created by Javier Carrillo", font=myFont5, fg="#344861", justify="left").place(x=850, y=160)

# Frame for cells
mainFrame = Frame(window)
mainFrame.place(x=100, y=50)

# Frame for numbers
numbersFrame = Frame(window, bg="#eaeef4", highlightbackground="#344861", highlightthickness=3)
numbersFrame.place(x=900, y=250)

# Frame for errors
errorsFrame = Frame(window, bg="#f9feff", highlightbackground="#344861", highlightthickness=2, width=215, height=62)
errorsFrame.grid_propagate(False)
errorsFrame.place(x=467, y=725)

Label(errorsFrame, text="Errors: ", font=myFont6, fg="#504f55", bg="#f9feff").grid(row=0, column=0)
strErrors = Label(errorsFrame, text="0", font=myFont6, fg="#504f55", bg="#f9feff")
strErrors.grid(row=0, column=1)

# Frame for difficulty
buttonsFrame = Frame(window, bg="#f9feff", highlightbackground="#344861", highlightthickness=2)
buttonsFrame.place(x=100, y=725)

Label(buttonsFrame, text="Create New Sudoku:", fg="#0072e3", bg="#f9feff", font=myFont2).grid(row=0, column=1)
Button(buttonsFrame, text="Easy", fg="#0072e3", bg="#f9feff", font=myFont2, width=10, height=1, relief=FLAT, command=lambda difficulty="easy": newSudoku(difficulty)).grid(row=1, column=0)
Button(buttonsFrame, text="Medium", fg="#0072e3", bg="#f9feff", font=myFont2, width=10, height=1, relief=FLAT, command=lambda difficulty="medium": newSudoku(difficulty)).grid(row=1, column=1)
Button(buttonsFrame, text="Hard", fg="#0072e3", bg="#f9feff", font=myFont2, width=10, height=1, relief=FLAT, command=lambda difficulty="hard": newSudoku(difficulty)).grid(row=1, column=2)

# Binds for the numbers
window.bind("1", lambda event, num=1: setNum(num, event))
window.bind("2", lambda event, num=2: setNum(num, event))
window.bind("3", lambda event, num=3: setNum(num, event))
window.bind("4", lambda event, num=4: setNum(num, event))
window.bind("5", lambda event, num=5: setNum(num, event))
window.bind("6", lambda event, num=6: setNum(num, event))
window.bind("7", lambda event, num=7: setNum(num, event))
window.bind("8", lambda event, num=8: setNum(num, event))
window.bind("9", lambda event, num=9: setNum(num, event))
# Bind for delete
window.bind("<BackSpace>", lambda event, num="": setNum(num, event))

# Frame for load and save
loadSaveFrame = Frame(window, bg="#eaeef4", highlightbackground="#344861", highlightthickness=3)
loadSaveFrame.place(x=900, y=520)

Button(loadSaveFrame, text="Load", fg="#E37100", bg="#eaeef4", font=myFont, width=10, height=1, relief=FLAT, command=loadGame).grid(row=0, column=0)
Button(loadSaveFrame, text="Save", fg="#E37100", bg="#eaeef4", font=myFont, width=10, height=1, relief=FLAT, command=saveGame).grid(row=0, column=1)
Label(loadSaveFrame, text="To load or save a \nSudoku, use the file \n'sdk.txt'. To load, the file must \ncontain a string of 81 \ncharacters from 0 to 9.", fg="#4c4e55", bg="#eaeef4", font=myFont3).grid(row=1, column=0, columnspan=2)

# Frame for solving
solveFrame = Frame(window, bg="#eaeef4", highlightbackground="#344861", highlightthickness=3)
solveFrame.place(x=1176, y=520)
btnVerify = Button(solveFrame, text="Verify\nSolutions", fg="#3ac56c", bg="#eaeef4", font=myFont, width=10, height=2, relief=FLAT, command=checkSolutions)
btnVerify.grid(row=1, column=0)
btnSolve = Button(solveFrame, text="Solve", fg="#3ac56c", bg="#eaeef4", font=myFont, width=10, height=1, relief=FLAT, state=DISABLED, command=solve)
btnSolve.grid(row=3, column=0)

strSolutions = Label(window, text="", fg="#4c4e55", font=myFont3)
strSolutions.place(x=1176, y=650)

generateBoxes()
generateMatrix()
generateNumbers()

window.mainloop()
