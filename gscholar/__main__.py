#!/usr/bin/env python

import optparse
import logging
import sys
import os

import gscholar as gs


logger = logging.getLogger('gscholar')
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING
)


def main():
    usage = 'Usage: %prog [options] {pdf | "search terms"}'
    parser = optparse.OptionParser(usage)
    parser.add_option("-a", "--all", action="store_true", dest="all",
                      default=False, help="show all bibtex results")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      default=False, help="show debugging output")
    parser.add_option("-r", "--rename", action="store_true", dest="rename",
                      default=False, help="rename file")
    parser.add_option("-f", "--outputformat", dest='output',
                      default="bibtex",
                      help="Output format. Available formats are: bibtex, endnote, refman, wenxianwang [default: %default]")
    parser.add_option("-s", "--startpage", dest='startpage',
                      help="Page number to start parsing PDF file at.")
    parser.add_option('-V', '--version', action='store_true',
                      help='Print version and quit.')

    (options, args) = parser.parse_args()
    if options.debug is True:
        logger.setLevel(logging.DEBUG)
    if options.version:
        print(gs.__VERSION__)
        return
    if options.output == 'bibtex':
        outformat = gs.FORMAT_BIBTEX
    elif options.output == 'endnote':
        outformat = gs.FORMAT_ENDNOTE
    elif options.output == 'refman':
        outformat = gs.FORMAT_REFMAN
    elif options.output == 'wenxianwang':
        outformat = gs.FORMAT_WENXIANWANG
    if len(args) != 1:
        parser.error("No argument given, nothing to do.")
        sys.exit(1)
    args = args[0]
    pdfmode = False
    if os.path.exists(args):
        logger.debug("File exist, assuming you want me to lookup the pdf: {filename}.".format(filename=args))
        pdfmode = True
        biblist = gs.pdflookup(args, all, outformat, options.startpage)
    else:
        logger.debug("Assuming you want me to lookup the query: {query}".format(query=args))
        biblist = gs.query(args, outformat, options.all)
    if len(biblist) < 1:
        print("No results found, try again with a different query!")
        sys.exit(1)
    if options.all is True:
        logger.debug("All results:")
        for i in biblist:
            print(i)
    else:
        logger.debug("First result:")
        print(biblist[0])
    if options.rename is True:
        if not pdfmode:
            print("You asked me to rename the pdf but didn't tell me which file to rename, aborting.")
            sys.exit(1)
        else:
            gs.rename_file(args, biblist[0])


if __name__ == '__main__':
    main()

# vim: set filetype=python
