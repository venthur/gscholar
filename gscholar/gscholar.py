#!/usr/bin/env python

"""
Library to query Google Scholar.

Call the method query with a string which contains the full search
string. Query will return a list of citations.

"""

from urllib.request import Request, urlopen, quote
from html.entities import name2codepoint
import re
import os
import subprocess
import logging
from time import sleep


GOOGLE_SCHOLAR_URL = "https://scholar.google.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Accept-Language': 'en-US',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept' : 'text/html',
    'Referer' : 'https://scholar.google.com/'
}

FORMAT_BIBTEX = 4
FORMAT_ENDNOTE = 3
FORMAT_REFMAN = 2
FORMAT_WENXIANWANG = 5


logger = logging.getLogger(__name__)


def query(searchstr, outformat=FORMAT_BIBTEX, delay=0.1, allresults=False, start_year='', end_year=''):
    """Query google scholar.

    This method queries google scholar and returns a list of citations.

    Parameters
    ----------
    searchstr : str
        the query
    outformat : int, optional
        the output format of the citations. Default is bibtex.
    allresults : bool, optional
        return all results or only the first (i.e. best one)
    delay: float, optional
        delay for requesting, to not getting banned by google for to much requests in a short time
    start_year: str, optional
        4 number integer representing the start year of papers like 2020
    end_year: str, optional
        4 number integer representing the end year of papers like 2022

    Returns
    -------
    result : list of strings
        the list with citations

    """
    logger.debug("Query: {sstring}".format(sstring=searchstr))
    # searchstr = '/scholar?q='+quote(searchstr)
    searchstr = f'/scholar?q={quote(searchstr)}&as_ylo={quote(start_year)}&as_yhi={quote(end_year)}'
    url = GOOGLE_SCHOLAR_URL + searchstr
    header = HEADERS
    header['Cookie'] = "GSP=CF=%d" % outformat
    request = Request(url, headers=header)
    response = urlopen(request)
    # add set_cookie in header in request header!
    set_cookie = response.headers['Set-Cookie']
    header['Cookie'] += set_cookie
    html = response.read()
    html = html.decode('utf8')
    # grab the links
    tmp = get_links(html, outformat)

    # follow the bibtex links to get the bibtex entries
    result = list()
    if not allresults:
        tmp = tmp[:1]
    for link in tmp:
        sleep(delay)
        url = GOOGLE_SCHOLAR_URL+link
        request = Request(url, headers=header)
        response = urlopen(request)
        bib = response.read()
        bib = bib.decode('utf8')
        result.append(bib)
    return result


def get_links(html, outformat):
    """Return a list of reference links from the html.

    Parameters
    ----------
    html : str
    outformat : int
        the output format of the citations

    Returns
    -------
    List[str]
        the links to the references

    """
    base_url = 'https://scholar.googleusercontent.com'
    if outformat == FORMAT_BIBTEX:
        refre = re.compile(fr'<a href="{base_url}(/scholar\.bib\?[^"]*)')
    elif outformat == FORMAT_ENDNOTE:
        refre = re.compile(fr'<a href="{base_url}(/scholar\.enw\?[^"]*)"')
    elif outformat == FORMAT_REFMAN:
        refre = re.compile(fr'<a href="{base_url}(/scholar\.ris\?[^"]*)"')
    elif outformat == FORMAT_WENXIANWANG:
        refre = re.compile(fr'<a href="{base_url}(/scholar\.ral\?[^"]*)"')
    reflist = refre.findall(html)
    # escape html entities
    reflist = [re.sub('&(%s);' % '|'.join(name2codepoint), lambda m:
                      chr(name2codepoint[m.group(1)]), s) for s in reflist]
    return reflist


def convert_pdf_to_txt(pdf, startpage=None):
    """Convert a pdf file to text and return the text.

    This method requires pdftotext to be installed.

    Parameters
    ----------
    pdf : str
        path to pdf file
    startpage : int, optional
        the first page we try to convert

    Returns
    -------
    str
        the converted text

    """
    if startpage is not None:
        startpageargs = ['-f', str(startpage)]
    else:
        startpageargs = []
    stdout = subprocess.Popen(["pdftotext", "-q"] + startpageargs + [pdf, "-"],
                              stdout=subprocess.PIPE).communicate()[0]
    # python2 and 3
    if not isinstance(stdout, str):
        stdout = stdout.decode()
    return stdout


def pdflookup(pdf, allresults, outformat, startpage=None):
    """Look a pdf up on google scholar and return bibtex items.

    Paramters
    ---------
    pdf : str
        path to the pdf file
    allresults : bool
        return all results or only the first (i.e. best one)
    outformat : int
        the output format of the citations
    startpage : int
        first page to start reading from

    Returns
    -------
    List[str]
        the list with citations

    """
    txt = convert_pdf_to_txt(pdf, startpage)
    # remove all non alphanumeric characters
    txt = re.sub(r"\W", " ", txt)
    words = txt.strip().split()[:20]
    gsquery = " ".join(words)
    bibtexlist = query(gsquery, outformat, allresults)
    return bibtexlist


def _get_bib_element(bibitem, element):
    """Return element from bibitem or None.

    Paramteters
    -----------
    bibitem :
    element :

    Returns
    -------

    """
    lst = [i.strip() for i in bibitem.split("\n")]
    for i in lst:
        if i.startswith(element):
            value = i.split("=", 1)[-1]
            value = value.strip()
            while value.endswith(','):
                value = value[:-1]
            while value.startswith('{') or value.startswith('"'):
                value = value[1:-1]
            return value
    return None


def rename_file(pdf, bibitem):
    """Attempt to rename pdf according to bibitem.

    """
    year = _get_bib_element(bibitem, "year")
    author = _get_bib_element(bibitem, "author")
    if author:
        author = author.split(",")[0]
    title = _get_bib_element(bibitem, "title")
    elem = [i for i in (year, author, title) if i]
    filename = "-".join(elem) + ".pdf"
    newfile = pdf.replace(os.path.basename(pdf), filename)
    logger.info('Renaming {in_} to {out}'.format(in_=pdf, out=newfile))
    os.rename(pdf, newfile)
