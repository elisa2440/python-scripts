#!/usr/bin/python
# coding=utf-8

import urllib2
import json
import time

antes = time.time()

req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest")
response = urllib2.urlopen(req)
page = response.readlines()
LA = []

for i in page[4:len(page)-1]:
    tipo = i.split("|")[2]
    if str(tipo) == "asn":
        LA.append(str(i.split("|")[3]))

req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/afrinic/delegated-afrinic-extended-latest")
response = urllib2.urlopen(req)
page = response.readlines()
AF = []

for i in page[4:len(page)-1]:
    tipo = i.split("|")[2]
    if str(tipo) == "asn":
        AF.append(str(i.split("|")[3]))

req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/ripencc/delegated-ripencc-extended-latest")
response = urllib2.urlopen(req)
page = response.readlines()
RP = []

for i in page[4:len(page)-1]:
    tipo = i.split("|")[2]
    if str(tipo) == "asn":
        RP.append(str(i.split("|")[3]))

req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/arin/delegated-arin-extended-latest")
response = urllib2.urlopen(req)
page = response.readlines()
AR = []

for i in page[4:len(page)-1]:
    tipo = i.split("|")[2]
    if str(tipo) == "asn":
        AR.append(str(i.split("|")[3]))

req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/apnic/delegated-apnic-extended-latest")
response = urllib2.urlopen(req)
page = response.readlines()
AP = []

for i in page[30:len(page)-1]:
    tipo = i.split("|")[2]
    if str(tipo) == "asn":
        if i.split("|")[4] == 1:
            AP.append(str(i.split("|")[3]))
        else:
            for n in range(1,int(i.split("|")[4])+1):
                AP.append(str(int(i.split("|")[3])+n))

rir_asns = {}
rir_asns["LACNIC"]=LA
rir_asns["AFRINIC"]=AF
rir_asns["APNIC"]=AP
rir_asns["ARIN"]=AR
rir_asns["RIPENCC"]=RP
dump = json.dumps(rir_asns)
open("rir_asns.json", "w").write(dump)

despues = time.time()
print despues-antes
