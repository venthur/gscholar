#!/usr/bin/env python

import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup

GOOGLE_SCHOLAR_URL = "http://scholar.google.com/scholar?q="
HEADERS = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
           'Cookie' : 'GSP=ID=962a112b5c765732:CF=4'}


def query(searchstr):
    searchstr = urllib2.quote(searchstr)
    url = GOOGLE_SCHOLAR_URL + searchstr
    cj = cookielib.CookieJar()
    # first request to get the cookies
    request = urllib2.Request(url, headers=HEADERS)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #response = opener.open(request)
    # modify cookie to see bibtex entries
    #for c in cj:
    #    print c
    #    if c.domain == ".scholar.google.com":
    #        c.value += ":CF=4"
   # new request
    response = opener.open(request)
    html = response.read()
    html.decode('ascii', 'ignore') 
    # grab the bibtex links
    soup = BeautifulSoup(html)
    tmp = soup.findAll('a', href=re.compile("^/scholar.bib"))
    result = []
    # follow the bibtex links to get the bibtex entries
    for link in tmp:
        url = link["href"]
        url = "http://scholar.google.com"+url
        request = urllib2.Request(url, headers=HEADERS)
        response = opener.open(request)
        bib = response.read()
        result.append(bib)
    return result


if __name__ == "__main__":
    for i in query("venthur"):
        print i

