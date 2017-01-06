from pyquery import PyQuery as pq
import sys
import codecs
import re
import os
from selenium import webdriver
import urllib

homeDir = "/Users/adrianoesch/Documents/opendata/slf/"
#
# profile = webdriver.FirefoxProfile()
# profile.set_preference('browser.download.folderList', 2)
# profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference('browser.download.dir', '/Users/adrianoesch/Downloads/')
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
# browser = webdriver.Firefox(profile)

for year in range(2016,2017):
    # browser.get("http://www.slf.ch/schneeinfo/Archiv/lwdarchiv/"+str(year)+"/hn1/de/gif")
    d = pq(url="http://www.slf.ch/schneeinfo/Archiv/lwdarchiv/"+str(year)+"/hn1/de/png")
    d.make_links_absolute(base_url="http://www.slf.ch/")
    links = d('a')
    print len(links)
    for l in links.items():
        print l.text().encode('utf16')
        if 'hn1_de_c.png' in l.text():
            print l.attr.href
            urllib.urlretrieve(l.attr.href,'/Users/adrianoesch/Documents/opendata/slf/gifs/'+l.text())
