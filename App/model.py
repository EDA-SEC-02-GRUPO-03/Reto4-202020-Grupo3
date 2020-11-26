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
import config
import math
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    try:
        citibike = {'graph': None,
                    'stops': None,
                    #'components': None,
                    #'paths': None
                    }

        citibike['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)

        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    latitude1 = float(trip['start station latitude'])
    longitude1 = float(trip['start station longitude'])
    latitude2 = float(trip['end station latitude'])
    longitude2 = float(trip['end station longitude'])
    edad = 2020 - int(trip['birth year'])
    type = trip['usertype']
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addStop(citibike, origin, latitude1, longitude1, edad, 's', type)
    addStop(citibike, destination, latitude2, longitude2, edad, 'll', type)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['graph'], stationid):
            gr.insertVertex(citibike ['graph'], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike['graph'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['graph'], origin, destination, duration)
    return citibike

def addStop(citibike, stationid, latitude, longitude, edad, s_ll, type):
    if m.contains(citibike['stops'], stationid):
        retorno = m.get(citibike['stops'], stationid)['value']
        m.remove(citibike['stops'], stationid)
    else:
        retorno = [latitude,longitude,{'0-10':0,
                                '11-20':0,
                                '21-30':0,
                                '31-40':0,
                                '41-50':0,
                                '51-60':0,
                                '60+':0,
                                'total':0}, {'0-10':0,
                                        '11-20':0,
                                        '21-30':0,
                                        '31-40':0,
                                        '41-50':0,
                                        '51-60':0,
                                        '60+':0,
                                        'total':0}, type]
    if s_ll == 's':
        a = 2
    else:
        a = 3   

    if edad in range(0,11):
        nuevo = retorno[a].get('0-10') + 1
        retorno[a]['0-10'] = nuevo
    elif edad in range(11,21):
        nuevo = retorno[a].get('11-20') + 1
        retorno[a]['11-20'] = nuevo
    elif edad in range(21,31):
        nuevo = retorno[a].get('21-30') + 1
        retorno[a]['21-30'] = nuevo
    elif edad in range(31,41):
        nuevo = retorno[a].get('31-40') + 1
        retorno[a]['31-40'] = nuevo
    elif edad in range(41,51):
        nuevo = retorno[a].get('41-50') + 1
        retorno[a]['41-50'] = nuevo
    elif edad in range(51,61):
        nuevo = retorno[a].get('51-60') + 1
        retorno[a]['51-60'] = nuevo
    else: 
        nuevo = retorno[a].get('60+') + 1
        retorno[a]['60+'] = nuevo

    nuevo = retorno[a].get('total') + 1
    retorno[a]['total'] = nuevo

    m.put(citibike['stops'], stationid, retorno)

    return citibike

# ==============================
# Funciones de consulta
# ==============================

def req1 (citibike, station1, station2):
    sc = scc.KosarajuSCC(citibike['graph'])
    num = scc.connectedComponents(sc)
    strongly = scc.stronglyConnected(sc, station1, station2)
    return (num,strongly)

def req3 (citibike):
    lstArrival = []
    lstDeparture = []
    lstLeast = []

    iterador = it.newIterator(m.keySet(citibike['stops']))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(citibike['stops'],element)
        salida = dicc['value'][2]['total']
        llegada = dicc['value'][3]['total']
        ambas = salida + llegada

        if len(lstArrival) < 3:
                lstArrival.append({'key':dicc['key'], 'value':salida})
                lstDeparture.append({'key':dicc['key'], 'value':llegada})
                lstLeast.append({'key':dicc['key'], 'value':ambas})
        else:
            for j in lstArrival:
                if salida > j['value']:
                    lstArrival.append({'key':dicc['key'], 'value':salida})
                    lstArrival.remove(j)
                    break
            for j in lstDeparture:
                if llegada > j['value']:
                    lstDeparture.append({'key':dicc['key'], 'value':llegada})
                    lstDeparture.remove(j)
                    break
            for j in lstLeast:
                if ambas < j['value']:
                    lstLeast.append({'key':dicc['key'], 'value':ambas})
                    lstLeast.remove(j)
  
    return (lstArrival,lstDeparture,lstLeast)



def req5 (citibike, edad):

    if edad in range(0,11):
        key = '0-10'
    elif edad in range(11,21):
        key = '11-20'
    elif edad in range(21,31):
        key = '21-30'
    elif edad in range(31,41):
        key = '31-40'
    elif edad in range(41,51):
        key = '41-50'
    elif edad in range(51,61):
        key = '51-60'
    else:
        key = '60+'

    iterador = it.newIterator(m.keySet(citibike['stops']))
    estacion_salida = 'Ninguna'
    max_salida = 0
    estacion_llegada = 'Ninguna'
    llegada_2 = 'Ninguna'
    max_llegada = 0
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(citibike['stops'],element)
        salida = dicc['value'][2]
        llegada = dicc['value'][3]
        if salida[key] > max_salida:
            max_salida = salida[key]
            estacion_salida = dicc['key']
        if llegada[key] > max_llegada:
            llegada_2 = estacion_llegada
            max_llegada = llegada[key]
            estacion_llegada = dicc['key']

    if estacion_llegada == estacion_salida:
        estacion_llegada = llegada_2

    ruta = []
    dijsktra = djk.Dijkstra(citibike['graph'],str(estacion_salida))
    if djk.hasPathTo(dijsktra, estacion_llegada):
        if djk.hasPathTo(dijsktra, estacion_llegada):
            ruta_lt = djk.pathTo(dijsktra, estacion_llegada)
            iterador = it.newIterator(ruta_lt)
            ruta.append(estacion_salida)
            while it.hasNext(iterador):
                element = it.next(iterador)
                ruta.append(element['vertexB'])
    else:
        ruta = 'No hay ruta'
    return (estacion_salida, estacion_llegada, ruta)

def req6(citibike, lat1, lon1, lat2, lon2):
    iterador = it.newIterator(m.keySet(citibike['stops']))
    radio_salida = 10000
    radio_llegada = 10000
    estacion_salida = ''
    estacion_llegada = ''
    while it.hasNext(iterador):
        llave = it.next(iterador)
        diccCoord = m.get(citibike['stops'],llave)
        lat = diccCoord['value'][0]
        lon = diccCoord['value'][1]
        haver_salida = (math.sin(math.radians((lat - lat1)) / 2))**2 \
                        + math.cos(math.radians(lat)) \
                        * math.cos(math.radians(lat)) \
                        * (math.sin(math.radians((lon - lon1)) / 2))**2
        d_s = 2*6371*math.asin(math.sqrt(haver_salida))
        if d_s <= radio_salida:
            radio_salida = d_s
            estacion_salida = diccCoord['key']

        haver_llegada = (math.sin(math.radians((lat - lat2)) / 2))**2 \
                        + math.cos(math.radians(lat)) \
                        * math.cos(math.radians(lat)) \
                        * (math.sin(math.radians((lon - lon2)) / 2))**2
        d_ll = 2*6371*math.asin(math.sqrt(haver_llegada))
        if d_ll <= radio_llegada:
            radio_llegada = d_ll
            estacion_llegada = diccCoord['key']


    if estacion_llegada != '' and estacion_salida != '':
        ruta = []
        dijsktra = djk.Dijkstra(citibike['graph'],str(estacion_salida))
        if djk.hasPathTo(dijsktra, estacion_llegada):
            ruta_lt = djk.pathTo(dijsktra, estacion_llegada)
            iterador = it.newIterator(ruta_lt)
            ruta.append(estacion_salida)
            while it.hasNext(iterador):
                element = it.next(iterador)
                ruta.append(element['vertexB'])
    else: 
        ruta = 'No hay ruta'
        
    return (estacion_salida, estacion_llegada, ruta)

def req7 (citibike, rango):
    lista = gr.edges(citibike['graph'])
    iterador = it.newIterator(lista)
    maximo = 0
    pareja = 'No hay'
    while it.hasNext(iterador):
        elemento = it.next(iterador)
        diccA = m.get(citibike['stops'],elemento['vertexA'])
        diccB = m.get(citibike['stops'],elemento['vertexB'])
        if diccA['value'][4] == 'Customer' and diccB['value'][4] == 'Customer':
            suma = diccA['value'][2].get(rango) + diccB['value'][3].get(rango)
            if suma > maximo:
                pareja = elemento
    
    return (pareja)



    
def numSCC(graph):
    sc = scc.KosarajuSCC(graph['graph'])
    return scc.connectedComponents(sc)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
