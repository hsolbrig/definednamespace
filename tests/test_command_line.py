import argparse
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import Optional

from generate_namespace import main


class ArgParseExitException(Exception):
    ...


def _parser_exit(_: argparse.ArgumentParser,  __=0, message: Optional[str]=None) -> None:
    raise ArgParseExitException(message)


help_text = """usage: generate_namespace [-h]
                          [-f {n3,nquads,nt,nt11,ntriples,trig,trix,ttl,turtle,xml}]
                          prefix uri rdf_file

Generate a DefinedNamespace

positional arguments:
  prefix                Prefix to generate namespace for (example: skos)
  uri                   Prefix URI (example:
                        http://www.w3.org/2004/02/skos/core#)
  rdf_file              Location or URL of RDF file to parse

optional arguments:
  -h, --help            show this help message and exit
  -f {n3,nquads,nt,nt11,ntriples,trig,trix,ttl,turtle,xml}, --format {n3,nquads,nt,nt11,ntriples,trig,trix,ttl,turtle,xml}
                        RDF file format"""


class CommandLineTestCase(unittest.TestCase):
    def test_help(self):
        # argparse does a sys exit 1.  We catch it here
        old_exit = argparse.ArgumentParser.exit
        argparse.ArgumentParser.exit = _parser_exit
        msg = StringIO()
        with redirect_stdout(msg):
            try:
                main(["-h"])
            except ArgParseExitException:
                ...
        argparse.ArgumentParser.exit = old_exit
        self.assertEqual(help_text, msg.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
