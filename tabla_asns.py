#!/usr/bin/python
# coding=utf-8

import json
from datetime import date

hoy=date.today()

f = json.load(open("anuncios_as_"+str(hoy)+".json"))
g = json.load(open("rir_asns.json"))
# h = open("asns_"+str(hoy)+".html", "w")
# h.write("<font face='verdana'>asn|rir|pfx_afrinic|pfx_apnic|pfx_lacnic|pfx_ripencc|pfx_arin</font><br>")
k = open("test_asns.html", "w")

tabla = '<table><tr><th>ASN</th><th>RIR</th><th>Afrinic prefix</th><th>Apnic prefix</th><th>LACNIC prefix</th><th>Ripe prefix</th><th>Arin prefix</th></tr>'

for i in f:
    afrinic = f[i][0]
    apnic = f[i][1]
    lacnic = f[i][2]
    ripe = f[i][3]
    arin = f[i][4]
    for j in g:
        if i in g[j]:
            rir = j
    # h.write("<font face='verdana'><a href='https://rdap.lacnic.net/bootstrap/autnum/"+str(i)+"' target='_blank'>"+str(i)+"</a>"+"|"+str(rir)+"|"+str(afrinic)+"|"+str(apnic)+"|"+str(lacnic)+"|"+str(ripe)+"|"+str(arin)+"</font><br>")
    tabla = tabla + '<tr><td><center><a href="https://rdap.lacnic.net/bootstrap/autnum/'+str(i)+'" target="_blank">'+str(i)+'</a></center></td><td><center>'+str(rir)+'</center></td><td><center>'+str(afrinic)+'</center></td><td><center>'+str(apnic)+'</center></td><td><center>'+str(lacnic)+'</center></td><td><center>'+str(ripe)+'</center></td><td><center>'+str(arin)+'</center></td></tr>'
    # print i, rir, afrinic, apnic, lacnic, ripe, arin

tabla = tabla + '</table>'

k.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title><style>table, th, td {border: 1px solid black; }</style></head><body><div>'+tabla+'</div></body></html>')
k.close()
