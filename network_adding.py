#!/usr/bin/python

import ipaddr
import math
import urllib2


def add_nets(rir):
    req = urllib2.Request("ftp://ftp.lacnic.net/pub/stats/"+str(rir)+"/delegated-"+str(rir)+"-extended-latest")
    response = urllib2.urlopen(req)
    page = response.readlines()
    net_inis = []
    v4 = []
    cantidades_pfx = {}
    for i in xrange(8,25):
        cantidades_pfx[i] = 2**(32-i)
    # print cantidades_pfx
    if rir == "apnic":
        n = 31
    else:
        n = 4
    for line in page[n:len(page)-1]:
        lineParts = line.split("|")
        tipo = lineParts[2]
        # print "tipo = "+str(tipo)
        if str(tipo) == str("ipv4"):
            net_ini = lineParts[3].split(".")[0]
            net_inis.append(net_ini)

    # print set(net_inis)

    for pfx in set(net_inis):
        lista = []
        for line in page[n:len(page)-1]:
            lineParts = line.split("|")
            tipo = lineParts[2]
            if str(tipo) == "ipv4":
                net = lineParts[3].split(".")[0]
                if str(net) == str(pfx):
                    ini = lineParts[3]
                    pref = 32 - math.log(int(lineParts[4]),2)
                    lista.append(ipaddr.IPNetwork(str(ini)+"/"+str(pref).split(".")[0]))
        collapsed = ipaddr.CollapseAddrList(lista)
        for item in collapsed:
            v4.append(item._explode_shorthand_ip_string())

    return v4

# af = open("RIRv4/Afrinic", "w")
# af.write(str(add_nets("afrinic")))
# ri = open("RIRv4/Ripe", "w")
# ri.write(str(add_nets("ripencc")))
# ar = open("RIRv4/Arin", "w")
# ar.write(str(add_nets("arin")))
# ap = open("RIRv4/Apnic", "w")
# ap.write(str(add_nets("apnic")))
# la = open("RIRv4/Lacnic", "w")
# la.write(str(add_nets("lacnic")))