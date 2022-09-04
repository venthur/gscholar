import argparse
import logging
import sys
import os

import gscholar as gs

try:
    import shtab
except ImportError:
    from . import _shtab as shtab


logger = logging.getLogger('gscholar')
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING
)

# https://github.com/iterative/shtab/blob/master/examples/customcomplete.py#L11-L22
PDF_FILE = {
    "bash": "_shtab_greeter_compgen_pdf_files",
    "zsh": "_files -g '*.pdf'",
    "tcsh": "f:*.pdf"
}
PREAMBLE = {
    "bash": """\
# $1=COMP_WORDS[1]
_shtab_greeter_compgen_pdf_files() {
  compgen -d -- $1  # recurse into subdirs
  compgen -f -X '!*?.pdf' -- $1
}
"""
}


def main():
    parser = argparse.ArgumentParser('gscholar')
    shtab.add_argument_to(parser, preamble=PREAMBLE)
    parser.add_argument("-a", "--all", action="store_true", dest="all",
                        default=False, help="show all bibtex results")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug",
                        default=False, help="show debugging output")
    parser.add_argument("-r", "--rename", action="store_true", dest="rename",
                        default=False, help="rename file")
    parser.add_argument("-f", "--outputformat", dest='output',
                        default="bibtex",
                        choices=["bibtex", "endnote", "refman", "wenxianwang"],
                        help=("Output format. Available formats are: %(choices)s"
                              "[default: %(default)s]"))
    parser.add_argument("-s", "--startpage", dest='startpage',
                        help="Page number to start parsing PDF file at.")
    parser.add_argument('-V', '--version', action='version',
                        version=gs.__VERSION__,
                        help='Print version and quit.')
    parser.add_argument('keyword', metavar='{pdf | "search terms"}',
                        help='pdf | "search terms"'
                        ).complete = PDF_FILE

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

    keyword = args.keyword
    pdfmode = False
    if os.path.exists(keyword):
        logger.debug(f"File exist, assuming you want me to lookup the pdf: "
                     f"{keyword}.")
        pdfmode = True
        biblist = gs.pdflookup(keyword, all, outformat, args.startpage)
    else:
        logger.debug(f"Assuming you want me to lookup the query: {keyword}")
        biblist = gs.query(keyword, outformat, args.all)
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
            gs.rename_file(keyword, biblist[0])


if __name__ == '__main__':
    main()
