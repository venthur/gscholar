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


"""Library to query Google Scholar.

Call the method query with a string which contains the full search string.
Query will return a list of bibtex items.
"""


import urllib2
import re
import hashlib
import random
import sys
import os
import subprocess
import optparse
import logging

from BeautifulSoup import BeautifulSoup


# fake google id (looks like it is a 16 elements hex)
google_id = hashlib.md5(str(random.random())).hexdigest()[:16] 

GOOGLE_SCHOLAR_URL = "http://scholar.google.com"
HEADERS = {'User-Agent' : 'Mozilla/5.0',
        'Cookie' : 'GSP=ID=%s:CF=4' % google_id }


def query(searchstr, allresults=False):
    """Return a list of bibtex items."""
    logging.debug("Query: %s" % searchstr)
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
    if allresults == False and len(tmp) != 0:
        tmp = [tmp[0]]
    for link in tmp:
        url = link["href"]
        url = GOOGLE_SCHOLAR_URL+url
        request = urllib2.Request(url, headers=HEADERS)
        response = urllib2.urlopen(request)
        bib = response.read()
        result.append(bib)
    return result


def convert_pdf_to_txt(pdf):
    """Convert a pdf file to txet and return the text.
    
    This method requires pdftotext to be installed.
    """
    stdout = subprocess.Popen(["pdftotext", "-q", pdf, "-"], stdout=subprocess.PIPE).communicate()[0]
    return stdout


def pdflookup(pdf, allresults):
    """Look a pdf up on google scholar and return bibtex items."""
    txt = convert_pdf_to_txt(pdf)
    # remove all non alphanumeric characters
    txt = re.sub("\W", " ", txt)
    words = txt.strip().split()[:20]
    gsquery = " ".join(words)
    bibtexlist = query(gsquery, allresults)
    return bibtexlist



if __name__ == "__main__":
    usage = 'Usage: %prog [options] {pdf | "search terms"}'
    parser = optparse.OptionParser(usage)
    parser.add_option("-a", "--all", action="store_true", dest="all", 
                      default="False", help="show all bibtex results")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      default="False", help="show debugging output")
    (options, args) = parser.parse_args()
    if options.debug == True:
        logging.basicConfig(level=logging.DEBUG)
    if len(args) != 1:
        parser.error("No argument given, nothing to do.")
        sys.exit(1)
    args = args[0]
    if os.path.exists(args):
        logging.debug("File exist, assuming you want me to lookup the pdf: %s." % args)
        biblist = pdflookup(args, all)
    else:
        logging.debug("Assuming you want me to lookup the query: %s." % args)
        biblist = query(args, options.all)
    if len(biblist) < 1:
        print "No results found, try again with a different query!"
        sys.exit(1)
    if options.all == True:
        logging.debug("All results:")
        for i in biblist:
            print i
    else:
        logging.debug("First result:")
        print biblist[0]

