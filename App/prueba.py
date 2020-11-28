archivo = open('Data\\201801-1-citibike-tripdata.csv')

linea = archivo.readline().replace("\n", "").split(',')
lista = {}
mayor = ('asdf', 0, '')
while len(linea) > 1:
    if linea[11] not in lista.keys():
        lista[linea[11]] = {linea[1][:11]: 1}
    else:
        if linea[1][:11] not in lista[linea[11]].keys():
           lista[linea[11]][linea[1][:11]] = 1
        else:
           lista[linea[11]][linea[1][:11]] += 1
    if lista[linea[11]][linea[1][:11]] >= mayor[1]:
        mayor= (linea[11], lista[linea[11]][linea[1][:11]], linea[1][:11])
    print(mayor)
    linea = archivo.readline().replace("\n", "").split(',')

