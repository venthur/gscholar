import argparse
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
    parser = argparse.ArgumentParser(usage)
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="show all bibtex results"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="show debugging output"
    )
    parser.add_argument(
        "-r", "--rename", action="store_true",
        help="rename file"
    )
    parser.add_argument(
        "-f", "--outputformat", dest='output', default="bibtex",
        help=(
            "Output format. Available formats are: bibtex, endnote, refman,"
            "wenxianwang [default: %(default)s]"))
    parser.add_argument(
        "-s", "--startpage",
        help="Page number to start parsing PDF file at."
    )
    parser.add_argument(
        '--version', action='version', version=gs.__VERSION__)
    parser.add_argument(
        'keyword', metavar='{pdf | "search terms"}',
        help='pdf | "search terms"')
    args = parser.parse_args()
    if args.debug is True:
        logger.setLevel(logging.DEBUG)
    if args.output == 'bibtex':
        outformat = gs.FORMAT_BIBTEX
    elif args.output == 'endnote':
        outformat = gs.FORMAT_ENDNOTE
    elif args.output == 'refman':
        outformat = gs.FORMAT_REFMAN
    elif args.output == 'wenxianwang':
        outformat = gs.FORMAT_WENXIANWANG
    pdfmode = False
    if os.path.exists(args.keyword):
        logger.debug(f"File exist, assuming you want me to lookup the pdf: "
                     f"{args}.")
        pdfmode = True
        biblist = gs.pdflookup(args.keyword, all, outformat, args.startpage)
    else:
        logger.debug(f"Assuming you want me to lookup the query: {args}")
        biblist = gs.query(args.keyword, outformat, args.all)
    if len(biblist) < 1:
        print("No results found, try again with a different query!")
        sys.exit(1)
    if args.all is True:
        logger.debug("All results:")
        for i in biblist:
            print(i)
    else:
        logger.debug("First result:")
        print(biblist[0])
    if args.rename is True:
        if not pdfmode:
            print("You asked me to rename the pdf but didn't tell me which "
                  "file to rename, aborting.")
            sys.exit(1)
        else:
            gs.rename_file(args.keyword, biblist[0])


if __name__ == '__main__':
    main()
