# gscholar

Query Google Scholar using Python.


## Requirements

 * Python
 * pdftotext (command line tool)


### Note on Python2 and Python3

Gscholar is Python2 and Python3 compatible. No changes should be required to run
on either Python version.


## Installing

```bash
$ pip install gscholar
```

##Using gscholar as a command line tool

gscholar provides a command line tool, to use it, just call `gscholar` like:

```bash
$ gscholar "albert einstein"
```

or

```bash
$ python3 -m gscholar "albert einstein"
```

### Making a simple lookup:

```bash
$ gscholar "some author or title"
```

will return the first result from Google Scholar matching this query.


### Getting more results:

```bash
$ gscholar --all "some author or title"
```

Same as above but returns up to 10 bibtex items. (Use with caution Google will
assume you're a bot an ban you're IP temporarily)


### Querying using a pdf:

```bash
$ gscholar /path/to/pdf
```

Will read the pdf to generate a Google Scholar query. It uses this query to show
the first bibtex result as above.


### Renaming a pdf:

```bash
$ gscholar --rename /path/to/pdf
```

Will do the same as above but asks you if it should rename the file according
to the bibtex result. You have to answer with "y", default answer is no.


### Getting help:

```bash
$ gscholar --help
```


## Using gscholar as a python library

Install the gscholar package with `pip install` as described above or copy the
package somewhere Python can find it.

```python
import gscholar

gscholar.query("some author or title")
```

will return a list of bibtex items.
