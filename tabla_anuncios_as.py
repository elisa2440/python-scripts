#!/usr/bin/python

from netaddr import *
from collections import defaultdict
import json
import time
from network_adding import add_nets

antes = time.time()

v4_afrinic = add_nets("afrinic")
v4_apnic = add_nets("apnic")
v4_lacnic = add_nets("lacnic")
v4_arin = add_nets("arin")
v4_ripe = add_nets("ripencc")

todos = []
for item in v4_afrinic:
    todos.append((item, "afrinic"))
for item in v4_arin:
    todos.append((item, "arin"))
for item in v4_apnic:
    todos.append((item, "apnic"))
for item in v4_ripe:
    todos.append((item, "ripe"))
for item in v4_lacnic:
    todos.append((item, "lacnic"))

print "Cargo todos los bloques de los RIRs"

# del v4_afrinic,v4_apnic,v4_arin,v4_lacnic,v4_ripe
f = open("ris_whois.txt", "r")
lines = f.readlines()
dict_asns = []
for l in lines:
    lineParts = l.split(" ")
    tupla = (lineParts[0], lineParts[1].split("\n")[0])
    dict_asns.append(tupla)
# print dict_asns

def getKey(item):
    return item[0]

dict_asns = sorted(dict_asns, key=getKey, reverse=True)
# print dict_asns

def merge_final_values(values):
    mergeddict = defaultdict(list)
    for group in values:
        mergeddict[group[:-1]].append(group[-1])
    return [(k + (tuple(v),) if len(v) > 1 else k + tuple(v))
                for k, v in mergeddict.iteritems()]

as_pfx = merge_final_values(dict_asns)
print len(as_pfx)
open("as_pfx.txt", "w").write(str(as_pfx))

as_pfx1 = as_pfx[0:1001]
as_pfx2 = as_pfx[1001:22501]
as_pfx3 = as_pfx[22501:33751]
as_pfx4 = as_pfx[33751:45001]
as_pfx5 = as_pfx[45001:56252]
# print dict_asns



st = {}
st['asn'] = ['AFRINIC', 'APNIC', 'LACNIC', 'RIPE', 'ARIN']
print "Empieza a contar"

def contar_por_rir(data):
    cant_afrinic = 0
    cant_apnic = 0
    cant_arin = 0
    cant_lacnic = 0
    cant_ripe = 0
    count = 0
    for item in data:
        # print count
        # print item[0]
        pfxs = item[1]
        if type(pfxs) == type(""):
            # print pfxs
            for i in todos:
                pfx = i[0]
                rir = i[1]
                if IPNetwork(str(pfxs)) in IPNetwork(pfx):
                    if str(rir) == "lacnic":
                        cant_lacnic = cant_lacnic + 1

                    if str(rir) == "apnic":
                        cant_apnic = cant_apnic + 1

                    if str(rir) == "afrinic":
                        cant_afrinic = cant_afrinic + 1

                    if str(rir) == "ripe":
                        cant_ripe = cant_ripe + 1

                    if str(rir) == "arin":
                        cant_arin = cant_arin + 1
                    break
        else:
            for j in range(0, len(pfxs)):
                one = pfxs[j]
                # print pfx
                for i in todos:
                    pfx = i[0]
                    rir = i[1]
                    if IPNetwork(str(one)) in IPNetwork(pfx):
                        if str(rir) == "lacnic":
                            cant_lacnic = cant_lacnic + 1

                        if str(rir) == "apnic":
                            cant_apnic = cant_apnic + 1

                        if str(rir) == "afrinic":
                            cant_afrinic = cant_afrinic + 1

                        if str(rir) == "ripe":
                            cant_ripe = cant_ripe + 1

                        if str(rir) == "arin":
                            cant_arin = cant_arin + 1
                        break
        st[item[0]] = [cant_afrinic,cant_apnic,cant_lacnic,cant_ripe,cant_arin]
        cant_arin = 0
        cant_lacnic = 0
        cant_ripe = 0
        cant_afrinic = 0
        cant_apnic = 0
        count = count + 1


i = 0
while i <= len(as_pfx):
    temp = as_pfx[i:i+1001]
    t1 = time.time()
    contar_por_rir(temp)
    t2 = time.time()
    print t2 - t1
    i = i + 1001
    print i

contar_por_rir(as_pfx[i-1001:len(as_pfx)+1])

print "Termino de contar"
# print st
dump = json.dumps(st)
t = open("anuncios_as.json", "w")
t.write(dump)
t.close()

despues = time.time()
print despues-antes


