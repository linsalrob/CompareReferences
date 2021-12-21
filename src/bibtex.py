"""
Read a bibtex file as a string and create a bibtex object
"""

import re
import sys
import argparse

import pybtex.database


__author__ = 'Rob Edwards'
__copyright__ = 'Copyright 2020, Rob Edwards'
__credits__ = ['Rob Edwards']
__license__ = 'MIT'
__maintainer__ = 'Rob Edwards'
__email__ = 'raedwards@gmail.com'


def parse_bibtex_file(bibtexf, verbose=False):
    """
    Parse a bibtex file ignoring duplicates
    :param bibtexf: the bibtex file
    :param verbose: more output
    :return:
    """

    if verbose:
        sys.stderr.write(f"Checking for duplicate entries: {bibtexf}\n")
    entries = set()
    raw_bibtex = ""
    src = re.compile(r'@\w+{(.*?),')

    with open(bibtexf, 'r', encoding="utf8") as bibin:
        for line in bibin:
            if line.startswith('@'):
                m = src.match(line)
                if not m:
                    sys.stderr.write(f"ERROR: Did not get a match to the regexp with {line}\n")
                    continue
                title = m.groups()[0]
                while title in entries:
                    title += ".1"
                entries.add(title)
                if title != m.groups()[0]:
                    line = line.replace(m.groups()[0], title)
                    if verbose:
                        sys.stderr.write(f"Duplicate entry {m.groups()[0]} ignored\n")

            raw_bibtex += line

    bt = pybtex.database.parse_string(raw_bibtex, "bibtex")
    return bt


def bibtex_titles(bibds, verbose=False):
    """
    Convert the bibtex db to a list of titles
    :param bibds: the bibtex datastructure
    :type bibds: a pybbtex database
    :param verbose: more output
    :type verbose: bool
    :return: a dict of titles
    :rtype: dict
    """
    titlesds = {}
    if verbose:
        sys.stderr.write("Parsing bibtex\n")
    for e in bibds.entries:
        try:
            if 'title' in bibds.entries[e].fields:
                t = bibds.entries[e].fields['title'].lower()
                t = t.replace('{', '')
                t = t.replace('}', '')
                titlesds[t.lower()] = e
        except Exception as ex:
            sys.stderr.write(f"Error parsing entry: {e}\n")
            print(ex)
    return titlesds


def bibtexfile_to_titles(bibtexfile, verbose):
    """
    Convert a bibtex file to just some titles
    """
    bibds = parse_bibtex_file(bibtexfile, verbose)
    return bibtex_titles(bibds, verbose)


def bibtex_differences(google_bib, google_title, orcid_bib, orcid_title, verbose=False):
    """
    Define the differences
    """
    dg = set(google_title.keys()).difference(set(orcid_title.keys()))  # present in google but not in orcid
    do = set(orcid_title.keys()).difference(set(google_title.keys()))  # present in orcid but not google
    if verbose:
        sys.stderr.write(f"{len(dg)} references are unique to Google\n{len(do)} references are unique to ORCID\n")

    g_bib = pybtex.database.BibliographyData(entries={google_title[e]: google_bib.entries[google_title[e]] for e in dg})
    o_bib = pybtex.database.BibliographyData(entries={orcid_title[e]: orcid_bib.entries[orcid_title[e]] for e in do})

    return g_bib, o_bib


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse a bibtex file and ignore duplicates")
    parser.add_argument('-b', help='bibtex file', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    bib = parse_bibtex_file(args.b, args.v)
    titles = bibtex_titles(bib, args.v)

    sys.stderr.write(f"Found {len(titles)} references\n")
