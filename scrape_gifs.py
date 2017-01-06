from pyquery import PyQuery as pq
import sys
import codecs
import re
import os
import urllib

storeDir = '/Users/adrianoesch/Documents/opendata/slf/gifs/' ## change dir

for year in range(2002,2017):
    d = pq(url="http://www.slf.ch/schneeinfo/Archiv/lwdarchiv/"+str(year)+"/hn1/de/png")
    d.make_links_absolute(base_url="http://www.slf.ch/")
    links = d('a')
    print len(links)
    for l in links.items():
        print l.text().encode('utf16')
        if 'hn1_de_c.png' in l.text():
            print l.attr.href
            urllib.urlretrieve(l.attr.href,storeDir+l.text())
