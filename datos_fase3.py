
import urllib2
import requests
from datetime import date
import json

req = urllib2.Request('ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest')
response = urllib2.urlopen(req)
the_page = response.readlines()

sumaReservados = 0
sumaDisponibles = 0
sumaAsignados = 0
sumaAllocados = 0

# Fetch data from FTP file
for i in the_page[4:len(the_page)-1]:
    status = i.split("|")[6]
    tipo = i.split("|")[2]
    if str(status) == "reserved" and str(tipo)=="ipv4":
        sumaReservados = sumaReservados+int(i.split("|")[4])
    if str(status).split("\n")[0] == "available" and str(tipo)=="ipv4":
        sumaDisponibles = sumaDisponibles+int(i.split("|")[4])
    if str(status) == "assigned" and str(tipo)=="ipv4":
        fecha = i.split("|")[5]
        if int(fecha) >= 20170215:
            sumaAsignados = sumaAsignados+int(i.split("|")[4])
    if str(status) == "allocated" and str(tipo)=="ipv4":
        fecha = i.split("|")[5]
        if int(fecha) >= 20170215:
            sumaAllocados = sumaAllocados+int(i.split("|")[4])


# Total allocated blocks minus 40704 ips from fase 2
sumaAsigTot = sumaAsignados + sumaAllocados - 40704

sumaPreAprobados = 0

s = requests.get("http://lacnic.net/cgi-bin/lacnic/range_requests_data")
data = s.json()['preApproved']

# Fetch pre-approved blocks
for i in data:
    prefijo = i['size'][0]
    cantidad = 2**(32-int(prefijo.split("/")[1]))
    sumaPreAprobados = sumaPreAprobados + cantidad


# Revoked and returned blocks are reserved blocks minus /15 for Critical Infrastructures and pre-approved blocks
sumaDevRev = sumaReservados-2**(32-15)-sumaPreAprobados

print sumaReservados

# Available blocks are available blocks in FTP file plus pre-approved blocks plus revoked and reserved blocks (*)
sumaDisponibles = sumaDisponibles + sumaPreAprobados

f = open("new_pie.txt", "w")
f.write("alloc,assig,libres,rev_dev\n\n")
f.write(str(sumaAllocados)+","+str(sumaAsignados)+","+str(sumaDisponibles)+","+str(sumaDevRev))
f.close()

# (*)
sumaDisponibles = sumaDisponibles + sumaDevRev

# Total blocks for fase 3 are available plus allocated blocks
sumaTotal = sumaDisponibles + sumaAsigTot

hoy = date.today()

st = {
    "data" : {
        "asignadas" : sumaAsigTot,
        "disponibles" : sumaDisponibles,
        "totales" : sumaTotal,
        "devueltos/revocados" : sumaDevRev,
        "actualizado" : str(hoy)
    }
}

dump = json.dumps(st, indent=4, separators=(',', ':'))
t = open("datos_fase3.json", "w")
t.write(dump)
t.close()
