#!/usr/bin/env python

# gscholar - Get bibtex entries from Goolge Scholar
# Copyright (C) 2010  Bastian Venthur <venthur at debian org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.



import urllib2
import re
import hashlib
import random
import sys


from BeautifulSoup import BeautifulSoup


# fake google id (looks like it is a 16 elements hex)
google_id = hashlib.md5(str(random.random())).hexdigest()[:16] 

GOOGLE_SCHOLAR_URL = "http://scholar.google.com"
HEADERS = {'User-Agent' : 'Mozilla/5.0',
        'Cookie' : 'GSP=ID=%s:CF=4' % google_id }


def query(searchstr):
    """Return a list of bibtex items."""
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
    if len(sys.argv) < 1:
        print 'Syntax: %s "your query terms"' % argv[0]
        sys.exit(1)
    for i in query(sys.argv[1]):
        print i

