
import urllib.request
import math
from datetime import date, datetime
import pymysql

hoy = datetime.today()

# Getting resurces from NRO delegated extended file

req = urllib.request.urlopen("https://www.nro.net/wp-content/uploads/apnic-uploads/delegated-extended")
nro = req.readlines()

legados = open("legadosSinRE.csv", "r").readlines()

# Connecting to LACNIC's DB

db = pymysql.connect("dbint.lacnic.net.uy","rpki","RpK1%;.","lacnic" )
cursor = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()


blegados = []
for l in legados:
    if l.split(";")[0] == "IP":
        b = l.split(";")[1]
        blegados.append(str(b))

lista_pocs = []

for n in nro[6:len(nro)+1]:
    lineParts = n.decode().split('|')
    if lineParts[0] == "lacnic":
        if lineParts[2] == "ipv4" and lineParts[1] != "ZZ":
            bloque = str(lineParts[3])+"/"+str(int(32 - math.log(int(lineParts[4]),2)))
            ipParts = lineParts[3].split(".")
            #print ipParts
            ip_inicial = int(ipParts[0])*(256**3)+int(ipParts[1])*(256**2)+int(ipParts[2])*256+int(ipParts[3])
            ip_final = int(ip_inicial) + int(lineParts[4]) - 1
            #print ip_inicial, ip_final
            cursor.execute("select adm_handle, sec_handle from blocosip where ip_inicial = %s and ip_final = %s " % (str(int(ip_inicial)), str(int(ip_final))))
            all = cursor.fetchall()
            if len(all) > 0:
                lista_pocs.append(all[-1][0])
                lista_pocs.append(all[-1][1])


lista_sin_dup = set(lista_pocs)
lista_sin_dup.remove('')

tiempos_hace = []

info_actual = {}

for poc in lista_sin_dup:
    cursor2.execute("select data_ultalt, nome, email, tel_numero from usuario where handle_usuario = '%s' " % str(poc))
    all = cursor2.fetchall()
    if len(all) > 0:
        ultima_actualizacion = all[-1][0]
        hace = (hoy - ultima_actualizacion).days/365.0
        print (hace)
        tiempos_hace.append(hace)
        if hace < 5:
            info_actual[poc] = set([all[-1][1], all[-1][2], all[-1][3]])

info_anterior = {}

for poc in lista_sin_dup:
    cursor2.execute("select nome, email, tel_numero from usuario_historico where handle_usuario = '%s' " % str(poc))
    all = cursor2.fetchall()
    if len(all) > 0:
        info_anterior[poc] = set([all[-1][0], all[-1][1], all[-1][2]])

print(lista_sin_dup)
print(info_actual.keys())
print(info_anterior.keys())

cant_pocs_current = []
for poc in lista_sin_dup:
    if poc in info_anterior.keys() and poc in info_actual.keys():
        print(info_actual[poc], info_anterior[poc])
        diff = info_actual[poc].difference(info_anterior[poc])
        if len(diff) > 0:
            cant_pocs_current.append(poc)

print(len(lista_sin_dup), len(cant_pocs_current))

menos_5 = []
menos_10 = []
mas_10 = []

for a in tiempos_hace:
    if a < 5:
        menos_5.append(a)
    elif a > 5 and a < 10:
        menos_10.append(a)
    elif a > 10:
        mas_10.append(a)

print (len(menos_5), len(menos_10), len(mas_10))

