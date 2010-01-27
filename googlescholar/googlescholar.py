#!/usr/bin/env python

import urllib2
import re
import hashlib
import random

from BeautifulSoup import BeautifulSoup

GOOGLE_SCHOLAR_URL = "http://scholar.google.com"
HEADERS = {'User-Agent' : 'Mozilla/5.0',
        'Cookie' : 'GSP=ID=%s:CF=4' % hashlib.md5(str(random.random())).hexdigest()[:16]}


def query(searchstr):
    searchstr = '/scholar?q='+urllib2.quote(searchstr)
    url = GOOGLE_SCHOLAR_URL + searchstr
    request = urllib2.Request(url, headers=HEADERS)
    response = urllib2.urlopen(request)
    html = response.read()
    html.decode('ascii', 'ignore') 
    # grab the bibtex links
    soup = BeautifulSoup(html)
    tmp = soup.findAll('a', href=re.compile("^/scholar.bib"))
    tmp
    result = []
    # follow the bibtex links to get the bibtex entries
    for link in tmp:
        url = link["href"]
        url = GOOGLE_SCHOLAR_URL+url
        request = urllib2.Request(url, headers=HEADERS)
        response = urllib2.urlopen(request)
        bib = response.read()
        result.append(bib)
    return result


if __name__ == "__main__":
    for i in query("venthur"):
        print i

