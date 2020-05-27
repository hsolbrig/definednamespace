import re
import sys
import textwrap
from argparse import ArgumentParser
import datetime
from keyword import kwlist
from typing import Optional, List
from rdflib import XSD, URIRef

import xmlschema

from template import fill_template

COMMENT_COL = 24

# Indent level -- don't use "\t" in Python as it messes up other edits
TAB = "    "


def generate_xsd_namespace(namespace: str, uri: str, schema_loc: str, title: Optional[str] = None) -> str:
    """
    Return a Python module that represents the namespace
    :param namespace: Namespace to generate (e.g. "xsd")
    :param uri: Namespace uri (e.g. "http://www.w3.org/2001/XMLSchema#")
    :param schema_loc: file or URL of XML Schema
    :param title: Additional title for output file
    :return: python text for resource
    """
    xs = xmlschema.XMLSchema11('https://www.w3.org/2009/XMLSchema/XMLSchema.xsd')
    schema = xs.to_dict(schema_loc)
    return fill_template(namespace, _hdr(schema, uri, schema_loc, title), _body(schema, uri))


def _hdr(schema: dict, uri: str, schema_loc: str, title: Optional[str]) -> str:
    """
    Generate a class header for URI
    :param schema: XML Schema definition
    :param uri: Ontology base to use for entries w/o ontology header
    :param schema_loc: source file or URL for schema definition
    :param title: Primary title
    :return: String representation of class docstring
    """
    def wrap(s: str) -> str:
        return ('\n' + TAB).join(textwrap.wrap(s, width=110))

    outlines = ['"""']
    if title:
        outlines.append(title)
        outlines.append('')
    outlines.append(f"Generated from: {schema_loc}")
    outlines.append(f"Date: {datetime.datetime.now()}")

    for annotation in schema.get('xs:annotation', []):
        for documentation in annotation.get('xs:documentation', []):
            if '$' in documentation:
                outlines.append('')
                outlines.append(documentation['$'])
    return f'\n{TAB}'.join(outlines) + f'\n{TAB}"""'


def _body(schema: dict, uri: str) -> str:
    """
    Generate the Python body for the schema
    :param schema: schema
    :param uri: namespace URI
    :return: Body text
    """
    outlines = []
    extras: List[URIRef] = []
    for st in schema['xs:simpleType']:
        if '@id' in st:             # No id means internal type
            id_name = st['@id']
            if id_name.isidentifier() and not id_name in kwlist:
                ident = f"{id_name}: URIRef"
                doc = ''
                annotations = st.get('xs:annotation')
                if annotations:
                    docs = annotations.get('xs:documentation', [])
                    doclist = [d['$'] if '$' in d else f"see: {d['@source']}" if '@source' in d else '' for d in docs]
                    doc = ''.join([re.sub('\n.*', '', e) for e in doclist if e])
                if doc:
                    pad = max(COMMENT_COL - len(ident), 2) * " "
                    ident += f"{pad}# {doc}"
                outlines.append(ident)
            else:
                extras.append(id_name)
    outlines = sorted(outlines)
    if extras:
        extra_list = ', '.join([f"'{e}'" for e in extras])
        outlines.append(f"\n{TAB}# Valid non-python identifiers ")
        outlines.append(f"\n{TAB}_extras = [{extra_list}]\n")
    outlines.append(f'\n{TAB}_NS = Namespace("{uri}")')
    return f'\n{TAB}'.join(outlines)


def genargs() -> ArgumentParser:
    """
    Generate an input string parser
    :return: parser
    """
    parser = ArgumentParser(prog="generate_xsd_namespace", description="Generate a DefinedNamespace from an XML Schema")
    parser.add_argument("prefix", help='Prefix to generate namespace for (example: xsd)')
    parser.add_argument("uri", help="Prefix URI (example: http://www.w3.org/2001/XMLSchema#)" )
    parser.add_argument("schema_file", help="Location or URL of XML Schema file to parse")
    parser.add_argument("-t", "--title", help="Title for schema documentation")
    return parser


def main(argv: Optional[List[str]] = None):
    opts = genargs().parse_args(argv)
    print(generate_xsd_namespace(opts.prefix, opts.uri, opts.schema_file, opts.title))
