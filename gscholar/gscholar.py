#!/usr/bin/env python

"""
Library to query Google Scholar.

Call the method query with a string which contains the full search
string. Query will return a list of citations.

"""

import logging
import os
import re
import subprocess
from html.entities import name2codepoint
from urllib.parse import quote
from urllib.request import Request, urlopen

GOOGLE_SCHOLAR_URL = "https://scholar.google.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

FORMAT_BIBTEX = 4
FORMAT_ENDNOTE = 3
FORMAT_REFMAN = 2
FORMAT_WENXIANWANG = 5


logger = logging.getLogger(__name__)


def query(
    searchstr: str,
    outformat: int = FORMAT_BIBTEX,
    allresults: bool = False
) -> list[str]:
    """Query google scholar.

    This method queries google scholar and returns a list of citations.

    Parameters
    ----------
    searchstr
        the query
    outformat
        the output format of the citations. Default is bibtex.
    allresults
        return all results or only the first (i.e. best one)

    Returns
    -------
    result
        the list with citations

    """
    logger.debug(f"Query: {searchstr}")
    searchstr = '/scholar?q='+quote(searchstr)
    url = GOOGLE_SCHOLAR_URL + searchstr
    header = HEADERS
    header['Cookie'] = f"GSP=CF={outformat}"
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
        url = GOOGLE_SCHOLAR_URL+link
        request = Request(url, headers=header)
        response = urlopen(request)
        bib = response.read()
        bib = bib.decode('utf8')
        result.append(bib)
    return result


def get_links(html: str, outformat: int) -> list[str]:
    """Return a list of reference links from the html.

    Parameters
    ----------
    html
    outformat
        the output format of the citations

    Returns
    -------
    reflist
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
    reflist = [
        re.sub(
            '&({});'.format('|'.join(name2codepoint)),
            lambda m: chr(name2codepoint[m.group(1)]),  # type: ignore[index]
            s
        )
        for s in reflist]
    return reflist


def convert_pdf_to_txt(pdf: str, startpage: int | None = None) -> str:
    """Convert a pdf file to text and return the text.

    This method requires pdftotext to be installed.

    Parameters
    ----------
    pdf
        path to pdf file
    startpage
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

    return stdout.decode()


def pdflookup(
        pdf: str,
        allresults: bool,
        outformat: int,
        startpage: int | None = None
) -> list[str]:
    """Look a pdf up on google scholar and return bibtex items.

    Paramters
    ---------
    pdf
        path to the pdf file
    allresults
        return all results or only the first (i.e. best one)
    outformat
        the output format of the citations
    startpage
        first page to start reading from

    Returns
    -------
    bibtexlist
        the list with citations

    """
    txt = convert_pdf_to_txt(pdf, startpage)
    # remove all non alphanumeric characters
    txt = re.sub(r"\W", " ", txt)
    words = txt.strip().split()[:20]
    gsquery = " ".join(words)
    bibtexlist = query(gsquery, outformat, allresults)
    return bibtexlist


def _get_bib_element(bibitem: str, element: str) -> str | None:
    """Return element from bibitem or None.

    Paramteters
    -----------
    bibitem :
    element :

    Returns
    -------
    Bibelement or None

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


def rename_file(pdf: str, bibitem: str) -> None:
    """Attempt to rename pdf according to bibitem."""
    year = _get_bib_element(bibitem, "year")
    author = _get_bib_element(bibitem, "author")
    if author:
        author = author.split(",")[0]
    title = _get_bib_element(bibitem, "title")
    elem = [i for i in (year, author, title) if i]
    filename = "-".join(elem) + ".pdf"
    newfile = pdf.replace(os.path.basename(pdf), filename)
    logger.info(f'Renaming {pdf} to {newfile}')
    os.rename(pdf, newfile)
