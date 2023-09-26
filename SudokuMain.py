from random import *
from tkinter import *
import tkinter.font as tkFont
import time
import tkinter.messagebox as messagebox

solucion = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]

juego = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]

botones = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]

cajas = [[0,0,0],
         [0,0,0],
         [0,0,0]]

posActual = None

errores = []

pistas = []

movimientos = []

movActual = -1

esPosible = True


# Rellenar cuadrantes diagonales
def generarDiagonal():
    key = [[0,1,2],[3,4,5],[6,7,8]]
    nums = [1,2,3,4,5,6,7,8,9]

    for k in range(0,3):                     # la variable key contiene grupos de cada cuadrante
        shuffle(nums)
        contador = 0
        for i in range(0,3):
            for j in range(0,3):
                solucion[key[k][i]][key[k][j]] = nums[contador]    # con key me aseguro de rellenar solo las diagonales (porque las diagonales no generan restricciones entre ellas)
                contador += 1


# Retorna true si el número se puede poner en una fila
# E: número de fila, valor
# S: un booleano
def chequearFila(fila, valor):
    for j in range(0,9):
        if valor == solucion[fila][j]:
            return False
    return True


# Retorna True si el valor se puede poner en una columna
# E: número de columna, valor
# S: un booleano
def chequearColumna(col,valor):
    for i in range(9):
        if valor == solucion[i][col]:
            return False
    return True

# Retorna True si el valor se puede poner en una caja
# E: número de fila, número de columna, valor
# S: un booleano
def chequearCaja(fila, col, valor):
    filaCentro = (fila // 3) * 3 + 1
    colCentro = (col // 3) * 3 + 1

    for i in [-1, 0 , 1]:
        for j in [-1, 0 ,1]:
            if valor == solucion[filaCentro + i][colCentro + j]:
                return False
    return True


# Retorna las coordenadas de una casilla sin asignar, -1, -1 si no existe
# S: una lista con dos números
def encontrarSiguiente():
    for i in range(0,9):
        for j in range(0,9):
            if solucion[i][j] == 0:
                return [i,j]
    return [-1,-1]


# Intenta solucionar el sudoku. Retorna True cuando todo se soluconó o se pudo poner un número, False si falta
# S: un booleano
def solucionarSudoku():
    coordenadas = encontrarSiguiente()   # Guarda las siguientes coordenadas a poner un número
    i = coordenadas[0]
    j = coordenadas[1]

    if i == -1 and j == -1:              # Si es -1 es porque ya se completó
        return True

    for num in [1,2,3,4,5,6,7,8,9]:        # Cicla por todos los números y chquea que se pueda poner
        if chequearFila(i, num) and chequearColumna(j, num) and chequearCaja(i, j, num):

            solucion[i][j] = num              # Si se puede poner, lo cambia

            if solucionarSudoku():         # Se llama recursivamente para el siguiente, si este no se puede poner entonces devuelve el valor
                return True                # a 0 e intenta el siguiente número

            solucion[i][j] = 0

    return False    # Significa que hubo un error antes y al poner False se devuelve


# Genera un sudoku
def generarSudoku():
    for i in range(0,9):
        for j in range(0,9):
            solucion[i][j] = 0

    generarDiagonal()

    solucionarSudoku()


# Crea un juego con dificultado determinada
# E: un string
def establecerDificultad(string):
    global juego
    global solucion

    if string == "facil":
        dificultad = 60
    elif string == "medio":
        dificultad = 45
    elif string == "dificil":
        dificultad = 30

    for i in range(0,9):
        for j in range(0,9):
            juego[i][j] = solucion[i][j]
            if randint(1,100) >= dificultad:
                juego[i][j] = 0


# Devuelve una lsita con las poisciones de los números iniciales
# S: una lista
def getPistas():
    global juego
    res = []
    for i in range(0,9):
        for j in range(0,9):
            if juego[i][j] != 0:
                res += [[i,j]]
    return res


# Pinta todos los botones de posiciones no iniciales de color gris
def pintarBotonesNoIniciales():
    global pistas
    for i in range(0,9):
        for j in range(0,9):
            if [i,j] not in pistas:
                botones[i][j].config(fg = "#0072e3")


# Actualiza el color del boton presionado y gurda la posición en una variable
# E: una lista con dos números
def botonPresionado(pos):
    global posActual
    posActual = pos
    pintarCasillas(pos)


# Pinta las casillas de acuardo a la posición actual
# E: una lista con dos números
def pintarCasillas(pos):
    pintarNoErrores()
    text = botones[pos[0]][pos[1]].cget("text")
    caja = [pos[0] // 3, pos[1] // 3]
    for i in range(0,9):
        for j in range(0,9):
            botones[i][j].config(bg = "white")                     # Devuelve todo a blanco


    for i in range(0,9):
        for j in range(0,9):
            if text != "":
                if botones[i][j].cget("text") == text:
                    botones[i][j].config(bg = "#c3d7ea")        # pinta los botones con el mismo número
            if i == pos[0] or j == pos[1]:
                botones[i][j].config(bg = "#e2ebf3")            # pinta fila y columna
            if [i//3,j//3] == caja:
                botones[i][j].config(bg = "#e2ebf3")            # pinta caja

    botones[pos[0]][pos[1]].config(bg = "#bbdefb")                  # pinta el boton presionado

    pintarErrores()


# Anota todas las casillas que tienen un error en una lista
def anotarErrores():
    global errores

    for i in range(0,9):
        for j in range(0,9):
            if isError([i,j]) and [i,j] not in errores:
                errores += [[i,j]]
            elif not isError([i,j]) and [i,j] in errores:
                errores.remove([i,j])
    updateErrores()


# Pinta los errores de rojo y devuelve los no errores a normal
def pintarErrores():
    global posActual
    global errores
    iPos = posActual[0]
    jPos = posActual[1]
    for i in range(0,9):
        for j in range(0,9):
            boton = botones[i][j]

            if [i,j] in errores:
                if i == iPos and j == jPos:
                    botones[iPos][jPos].config(fg = "#e06c7e")
                else:
                    boton.config(bg = "#f7cfd6")


# Devuelve a la normalidad los botones que no son errores
def pintarNoErrores():
    for i in range(0,9):
        for j in range(0,9):
            boton = botones[i][j]

            if [i,j] not in errores:
                boton.config(bg = "white")
                if [i,j] not in pistas:
                    boton.config(fg = "#0072e3")
                else:
                    boton.config(fg = "#344861")



# Retorna True si hay un error en la posición dada
# E: una lista con dos números
# S: un booleano
def isError(pos):
    text = botones[pos[0]][pos[1]].cget("text")

    if text == "":
        return False

    for i in range(0,9):
        for j in range(0,9):
            if i == pos[0] and j == pos[1]:
                continue

            boton = botones[i][j]

            if boton.cget("text") == text and i == pos[0]:       # Filas
                return True

            elif boton.cget("text") == text and j == pos[1]:       # Columnas
                return True

            elif boton.cget("text") == text and [i//3,j//3] == [pos[0]//3, pos[1]//3]:       # Cajas
                return True

    return False

# Mete un número en el sudoku
# E: un número
def setNum(num, event = None, redo = False):
    global posActual
    global movimientos
    global pistas
    global movActual
    if posActual == None:
        return
    i = posActual[0]
    j = posActual[1]
    if [i,j] not in pistas:
        textoAnterior = botones[i][j].cget("text")
        textoNuevo = str(num)

        botones[i][j].config(text = textoNuevo)
        juego[i][j] = num

        if not redo:
            if movActual < len(movimientos) - 1:
                movimientos = movimientos[:movActual + 1]
            movimientos.append([i, j, textoAnterior, textoNuevo])
            movActual += 1

    anotarErrores()
    pintarCasillas(posActual)

    checkWin()


# Deshace el último movimiento
def deshacer():
    global movimientos
    global movActual
    global posActual
    if movActual != -1:
        i = movimientos[movActual][0]
        j = movimientos[movActual][1]
        textoAnterior = movimientos[movActual][2]

        posActual = [i,j]

        setNum(textoAnterior, None, True)

        movActual -= 1


# Rehae el último movimiento deshecho
def rehacer():
    global movimientos
    global movActual
    global posActual
    if movActual != len(movimientos) - 1:
        movActual += 1
        i = movimientos[movActual][0]
        j = movimientos[movActual][1]
        textoNuevo = movimientos[movActual][3]

        posActual = [i,j]

        setNum(textoNuevo, None, True)


# Crea un nuevo sudoku
# E: un string
def newSudoku(dificultad):
    global juego
    global solucion
    global pistas
    global errores
    global ultimoMov
    global posActual
    global movActual
    global movimientos
    global esPosible
    generarSudoku()
    establecerDificultad(dificultad)
    pistas = getPistas()

    errores = []
    ultimoMov = None
    posActual = [0,0]
    movActual = -1
    movimientos = []
    esPosible = True
    btnSolucionar.config(state = DISABLED)
    strSoluciones.config(text = "")

    for i in range(0,9):
        for j in range(0,9):
            if juego[i][j] == 0:
                botones[i][j].config(text = "")
            else:
                botones[i][j].config(text = str(juego[i][j]))

    pintarCasillas([0,0])
    pintarBotonesNoIniciales()
    verificarSoluciones()


# Guarda una partida
def guardarPartida():
    global juego
    file = open("Proyecto 2\sdk.txt", "w")
    for i in range(0,9):
        for j in range(0,9):
            file.write(str(juego[i][j]))


# Carga una partida del archivo "sdk.txt"
def cargarPartida():
    global juego

    try:
        file = open("Proyecto 2\sdk.txt", "r")
    except:
        return

    file = open("Proyecto 2\sdk.txt", "r")

    str = file.read()
    contador = 0

    for i in range(0,9):
        for j in range(0,9):
            char = str[contador]

            try:
                num = int(char)
            except:
                return

            num = int(char)
            juego[i][j] = num
            contador += 1
    file.close()
    newSudokuCarga()

# Crea el nuevo sudoku cargado
def newSudokuCarga():
    global juego
    global solucion
    global pistas
    global errores
    global ultimoMov
    global posActual
    global movActual
    global movimientos
    global esPosible
    pistas = getPistas()

    errores = []
    ultimoMov = None
    posActual = [0,0]
    movActual = -1
    movimientos = []
    esPosible = False
    btnSolucionar.config(state = DISABLED)
    strSoluciones.config(text = "")

    for i in range(0,9):
        for j in range(0,9):
            if juego[i][j] == 0:
                botones[i][j].config(text = "")
            else:
                botones[i][j].config(text = str(juego[i][j]))
            solucion[i][j] = juego[i][j]

    pintarCasillas([0,0])
    pintarBotonesNoIniciales()
    verificarSoluciones()


# Retorna la cantidad de soluciones de un sudoku
# S: un numero
def verificarSoluciones():
    solucionarSudoku()

    if isValid():
        btnSolucionar.config(state = NORMAL)
        strSoluciones.config(text = "El Sudoku tiene solución 😁")

    else:
        btnSolucionar.config(state = DISABLED)
        strSoluciones.config(text = "El Sudoku no tiene solución 😔")


# Retorna True si todas las casillas de la solución, no son 0
# S: un booleano
def isValid():
    for i in range(0,9):
        for j in range(0,9):
            if solucion[i][j] == 0:
                return False
    return True


# Soluciona el sudoku
def solucionar():
    global solucion
    global pistas
    for i in range(0,9):
        for j in range(0,9):
            if [i,j] not in pistas:
                botones[i][j].config(text = str(solucion[i][j]))
                juego[i][j] = solucion[i][j]
                ventana.update()
                time.sleep(0.02)
    anotarErrores()
    pintarNoErrores()
    checkWin()


# Retorna True si ya se ganó el juego
# S: un booleano
def isWin():
    for i in range(0,9):
        for j in range(0,9):
            if juego[i][j] != solucion[i][j]:
                return False
    return True


# Produce una ventana con mensaje de victoria
def showWin():
    messagebox.showinfo("Victoria", "¡Felicidades, ha ganado!")


# Chequea si hay una victoria
def checkWin():
    if isWin():
        for i in range(0,9):
            for j in range(0,9):
                botones[i][j].config(fg= "#83600d", bg= "#f5d560")
        showWin()


# Updatea el str de errores
def updateErrores():
    global errores
    cantidad = len(errores)
    strErrores.config(text = str(cantidad))



# Algoritmos de Interfaz =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Genera 9 subframes para las cajas del sudoku
def generarCajas():
    for i in range(0,3):
        for j in range(0,3):
            frame = Frame(framePrincipal, bg = "#344861", highlightbackground="#344861", highlightthickness=1)
            frame.grid(row = i, column = j)
            cajas[i][j] = frame


# Genera los botones de la interfaz
def generarMatriz():
    for i in range(0,9):
        for j in range(0,9):
            # obtiene el valor de la matriz lógica
            texto = str (juego[i][j])

            if texto == "0":
                texto = ""

            #crea el boton, con el color blanco, el texto anterior
            btn = Button(cajas[i//3][j//3], text=texto, fg = "#344861", bg="white", font = myFont, width= 2, height= 1, relief = FLAT,
                         command= lambda coord=[i,j]: botonPresionado(coord))

            # se coloca el boton en la matriz, en la posicion i,j
            btn.grid(row=(i % 3), column=(j % 3), ipadx=15, ipady= 15, padx = 1, pady = 1)
            botones[i][j] = btn


# Generar los botones de los números
def generarNumeros():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    contador = 0
    for i in range(0,3):
        for j in range(0,3):
            num = nums[contador]
            btn = Button(frameNumeros, text = num, fg = "#0072e3", bg="#eaeef4", font = myFont, width = 5, height= 1, relief = FLAT,
                         command= lambda num=num: setNum(num))
            btn.grid(row = i, column = j, padx= 2, pady = 2, ipadx = 15, ipady = 15)
            contador += 1
    btn = Button(frameNumeros, text = "Borrar", fg = "#0072e3", bg="#eaeef4", font = myFont, relief = FLAT, width = 5, height= 1,
                command= lambda num="": setNum(num))
    btn.grid(row = 1, column = 3, padx= 2, pady = 2, ipadx = 15, ipady = 20)

    btn = Button(frameNumeros, text = "Deshacer", fg = "#0072e3", bg="#eaeef4", font = myFont, relief = FLAT, width = 5, height= 1,         # Boton de deshacer
                command= deshacer)
    btn.grid(row = 0, column = 3, padx= 2, pady = 2, ipadx = 15, ipady = 20)

    btn = Button(frameNumeros, text = "Rehacer", fg = "#0072e3", bg="#eaeef4", font = myFont, relief = FLAT, width = 5, height= 1,         # Boton de deshacer
                command= rehacer)
    btn.grid(row = 2, column = 3, padx= 2, pady = 2, ipadx = 15, ipady = 20)


# GUI =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
ventana = Tk()
ventana.title("Mi primera ventana")
ventana.geometry("1500x800")

myFont = tkFont.Font(family='Bahnschrift', weight="bold", size=15)
myFont2 = tkFont.Font(family='Bahnschrift', size=12)
myFont3 = tkFont.Font(family='Bahnschrift', size=10)
myFont4 = tkFont.Font(family='Neo Sans', size=90, weight="bold", slant="italic")
myFont5 = tkFont.Font(family='Neo Sans', size=15, slant="italic")
myFont6 = tkFont.Font(family='Bahnschrift', size=30)

# Titulo
Label(ventana, text = "😲SUDOKU😨 ", font = myFont4, fg = "#344861", justify= "left").place(x = 700, y = 20)
Label(ventana, text = "Elaborado por Javier Carrillo", font = myFont5, fg = "#344861", justify= "left").place(x = 850, y = 160)


# Frame para casillas
framePrincipal = Frame(ventana)
framePrincipal.place(x = 100, y = 50)

# Frame para numeros
frameNumeros = Frame(ventana, bg = "#eaeef4", highlightbackground="#344861", highlightthickness=3)
frameNumeros.place(x = 900, y = 250)

# Frame para errores
frameErrores = Frame(ventana, bg = "#f9feff", highlightbackground="#344861", highlightthickness=2, width= 215, height= 62)
frameErrores.grid_propagate(False)
frameErrores.place(x = 467, y = 725)

Label(frameErrores, text = "Errores: ", font = myFont6, fg = "#504f55", bg="#f9feff").grid(row=0, column = 0)
strErrores = Label(frameErrores, text = "0", font = myFont6, fg = "#504f55", bg="#f9feff")
strErrores.grid(row=0, column = 1)

# Frame para dificultad
frameBotones = Frame(ventana, bg = "#f9feff", highlightbackground="#344861", highlightthickness=2)
frameBotones.place(x = 100, y = 725)

Label(frameBotones, text= "Crear Nuevo Sudoku:", fg = "#0072e3", bg="#f9feff", font = myFont2).grid(row=0, column = 1)
Button(frameBotones, text = "Fácil", fg = "#0072e3", bg="#f9feff", font = myFont2, width = 10, height= 1, relief = FLAT, command= lambda dificultad="facil": newSudoku(dificultad)).grid(row=1, column = 0)
Button(frameBotones, text = "Medio", fg = "#0072e3", bg="#f9feff", font = myFont2, width = 10, height= 1, relief = FLAT, command= lambda dificultad="medio": newSudoku(dificultad)).grid(row=1, column = 1)
Button(frameBotones, text = "Dificil", fg = "#0072e3", bg="#f9feff", font = myFont2, width = 10, height= 1, relief = FLAT, command= lambda dificultad="dificil": newSudoku(dificultad)).grid(row=1, column = 2)

# binds para los numeros
ventana.bind("1", lambda event, num = 1: setNum(num, event))
ventana.bind("2", lambda event, num = 2: setNum(num, event))
ventana.bind("3", lambda event, num = 3: setNum(num, event))
ventana.bind("4", lambda event, num = 4: setNum(num, event))
ventana.bind("5", lambda event, num = 5: setNum(num, event))
ventana.bind("6", lambda event, num = 6: setNum(num, event))
ventana.bind("7", lambda event, num = 7: setNum(num, event))
ventana.bind("8", lambda event, num = 8: setNum(num, event))
ventana.bind("9", lambda event, num = 9: setNum(num, event))
# bind para borrar
ventana.bind("<BackSpace>", lambda event, num = "": setNum(num, event))

# Frame para cargar y guardar
frameCargarGuardar = Frame(ventana, bg = "#eaeef4", highlightbackground="#344861", highlightthickness=3)
frameCargarGuardar.place(x = 900, y = 520)

Button(frameCargarGuardar, text = "Cargar", fg = "#E37100", bg="#eaeef4", font = myFont, width = 10, height= 1, relief = FLAT, command = cargarPartida).grid(row=0, column = 0)
Button(frameCargarGuardar, text = "Guardar", fg = "#E37100", bg="#eaeef4", font = myFont, width = 10, height= 1, relief = FLAT, command = guardarPartida).grid(row=0, column = 1)
Label(frameCargarGuardar, text= "Para cargar o guardar un \nsudoku se utiliza el archivo \n'sdk.txt'. Para cargar, el archivo debe \ncontener un string de 81 \ncarácteres del 0 al 9.", fg = "#4c4e55", bg="#eaeef4", font = myFont3).grid(row=1, column = 0, columnspan = 2)

# Frame para solucionar
frameSolucionar = Frame(ventana, bg = "#eaeef4", highlightbackground="#344861", highlightthickness=3)
frameSolucionar.place(x = 1176, y = 520)
btnVerificar = Button(frameSolucionar, text = "Verificar\nSoluciones", fg = "#3ac56c", bg="#eaeef4", font = myFont, width = 10, height= 2, relief = FLAT, command = verificarSoluciones)
btnVerificar.grid(row=1, column = 0)
btnSolucionar = Button(frameSolucionar, text = "Solucionar", fg = "#3ac56c", bg="#eaeef4", font = myFont, width = 10, height= 1, relief = FLAT, state = DISABLED, command = solucionar)
btnSolucionar.grid(row=3, column = 0)

strSoluciones = Label(ventana, text = "", fg = "#4c4e55", font = myFont3)
strSoluciones.place(x = 1176, y = 650)




generarCajas()
generarMatriz()
generarNumeros()


ventana.mainloop()
