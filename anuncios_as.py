#!/usr/bin/python

import urllib2
from lacnic_commons import get_file
import gzip
import collections
import time


antes = time.time()
# uh = urllib2.urlopen("http://www.ris.ripe.net/dumps/riswhoisdump.IPv4.gz")
# print uh.read(10*1024)
get_file.get_file("http://www.ris.ripe.net/dumps/riswhoisdump.IPv4.gz", "data/riswhois.IPv4.gz", 9600)
whoisf = gzip.open("data/riswhois.IPv4.gz", "r")
line = whoisf.readlines()
whoisf.close()
f = open("ris_whois.txt", "w")
asns = []
for l in line:
    # print "this is a line: %s" % str(l)
    lineParts = l.split()
    if l.strip() and str(lineParts[0]) != "%":
        varios = lineParts[0].split(",")
        if len(varios) == 1:
            asns.append(lineParts[0])
            f.write(str(lineParts[0]).replace("}", "").lstrip("{")+" "+str(lineParts[1])+"\n")


print len(line)
f.close()
despues = time.time()

print despues-antes
