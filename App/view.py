"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from App import model
from DISClib.ADT import stack
import timeit
assert config
#Borrar
from DISClib.ADT.graph import gr

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

citibike1 = 'Data\\201801-1-citibike-tripdata.csv'
citibike2 = 'Data\\201801-1-citibike-tripdata.csv'
citibike3 = 'Data\\201801-1-citibike-tripdata.csv'
citibike4 = 'Data\\201801-1-citibike-tripdata.csv'
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("------------------------------------------------------")
    print("Bienvenido al analizador de datos de CitiBike")
    print("------------------------------------------------------\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información CitiBike")
    print("3- Cantidad de clusters de viajes")
    print("4- Ruta turística cirular")
    print("5- Estaciones críticas")
    print("6- Ruta turística por resistencia")
    print("7- Recomendador de rutas")
    print("8- Ruta de interés turístico")
    print("9- Identificación de estaciones para publicidad")
    print("10- Identificación de bicicletas para mantenimiento")
    print("0- Salir")
    print("------------------------------------------------------")


def optionTwo():
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Número de vértices: ' + str(numvertex))
    print('Número de arcos: ' + str(numedges))
    print('Límite de recursión actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El límite de recursión se ajusta a: ' + str(recursionLimit))

def optionThree():
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    scc = controller.numSCC(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('Número de elementos fuertemente conectados: ' + str(scc))

def optionFour():
    disponible = 0
    station1 = 0
    controller.ejecutarreq2(cont, disponible, station1)

def optionFive():
    controller.ejecutarreq3(cont)


def optionSix():
    resis = int(input('⏳ Ingrese el tiempo disponible en minutos: '))
    inicio = input('🛑 Ingrese la estación inicial: ')
    try:
        resul = controller.req4(cont, resis, inicio)
        print('las estaciones a las que se puede llegar desde', inicio, 'con',
            resis, 'minutos son:')
        for i in resul.keys():
            print(i, 'desde', resul[i][0], '\n\t⬆', resul[i][1], 'minutos')
    except:
        print('datos no válidos')

def optionSeven():
    edad = int(input('Edad del usuario: '))
    controller.ejecutarreq5(cont, edad)


def optionEight():
    lat1 = float(input('Ingrese la latitud del punto de salida: '))
    lon1 = float(input('Ingrese la longitud del punto de salida: '))
    lat2 = float(input('Ingrese la latitud del punto de llegada: '))
    lon2 = float(input('Ingrese la longitud del punto de llegada: '))
    controller.ejecutarreq6(cont, lat1, lon1, lat2, lon2)

def optionNine():
    rango = str(input('Ingrese el rango de edad (por ejemplo: 21-30): '))
    controller.ejecutarreq7(cont, rango)

def optionTen():
    print('Ejemplos: 14580, 2018-01-24 \n\t 26701, 2018-01-13')
    date = input('📅 Ingrese la fecha a consultar (AAAA-MM-DD): ')
    id = input('🚲 Ingrese la id de la bicicleta a consultar: ')
    try:
        resul = controller.req8(cont, date, id)
        print('Los resultados para la bicicleta', id, 'el día',
            date, 'son:')
        print('⏲ Tiempo de uso:', resul[0], 'minutos')
        print('🚦 Tiempo estacionada:', resul[1], 'minutos')
        print('🚩 Estaciones visitadas:')
        for i in resul[2]:
            print('\t-', i)
    except:
        print('Datos no válidos')

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:

        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
