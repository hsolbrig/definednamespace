import re
import sys
from argparse import ArgumentParser
from keyword import kwlist
from typing import Dict, List, Union, Optional

from rdflib import Graph, URIRef, Namespace, SKOS, RDFS, RDF, OWL
from rdflib.plugin import plugins as rdflib_plugins, Parser as rdflib_Parser

COMMENT_COL = 24
descriptions = [
    SKOS.definition,
    SKOS.prefLabel,
    RDFS.comment,
    RDFS.label
]

TAB = "    "


def generate_namespace(namespace: str, uri: Union[str, URIRef, Namespace], rdf_loc: Union[str, URIRef, Namespace],
                       rdf_format: str = "turtle") -> str:
    """
    Return a Python module that represents the namespace
    :param namespace: Namespace to generate (e.g. "skos")
    :param uri: Namespace uri (e.g. "http://www.w3.org/2004/02/skos/core#")
    :param rdf_loc: file or URL of rdf
    :param rdf_format: format of RDF
    :return: text for resource
    """
    g = Graph()
    g.load(rdf_loc, format=rdf_format)

    return f"""from rdflib import URIRef, Namespace
from definednamespace import DefinedNamespace


class {namespace.upper()}(DefinedNamespace):
    {_hdr(g)}
    {_body(g, str(uri))}
"""


def _hdr(g: Graph) -> str:
    s = g.value(None, RDF.type, OWL.Ontology, any=False)
    if not s:
        lines = "No Ontology defined - no documentation available"
    g2 = Graph()
    g2.namespace_manager = g.namespace_manager
    for p, o in g.predicate_objects(s):
        g2.add((s, p, o))
    lines = '"""\n'
    for l in g2.serialize(format="turtle").decode().split('\n'):
        if l and not "@prefix" in l and "Ontology ;" not in l:
            lines += re.sub(r'^    ', TAB, l.rstrip()) + "\n"
    lines += TAB + '"""'
    return lines


def _longest_type(s: URIRef, default: URIRef, g: Graph) -> URIRef:
    """
    Return the longest value associated with s, p, the general notion being that the longest is probably the most
    specific
    :param s: subject
    :param default: default value
    :param g: Graph
    :return: Longest value or default
    """
    rval = ""
    for o in sorted(g.objects(s, RDF.type)):
        if len(str(o)) > len(rval):
            rval = str(o)
    return URIRef(rval) if rval else default


def _description_for(node: URIRef, g: Graph) -> str:
    for p in descriptions:
        desc = g.value(node, p)
        if desc:
            return str(desc)
    return ""


def _body(g: Graph, uri: str) -> str:
    """
    Create the body of a DefinedNamespace from standard RDF
    :param g: Graph
    :param uri: Prefix to generate
    :return: Body for a DefinedNamespace
    """
    contents: Dict[URIRef, List[URIRef]] = dict()
    rval = ""

    # Sort the subjects in the namespace by type
    for s in sorted(set(g.subjects())):
        if str(s).startswith(uri):
            contents.setdefault(_longest_type(s, RDFS.Resource, g), []).append(s)

    extras: List[URIRef] = []
    for k in sorted(contents.keys()):
        vs = contents[k]
        if len(vs) > 1 and str(vs[0])[len(uri):]:
            rval += f"\n{TAB}# {k}\n"
            for v in sorted(vs):
                ident = str(v)[len(uri):]
                if ident.isidentifier() and not ident in kwlist:
                    doc = _description_for(v, g).strip().replace('\n', ' ')
                    pad = max(COMMENT_COL - len(ident), 2) * " "
                    rval += f"{TAB}{ident}: URIRef{pad}# {doc}\n"
                else:
                    extras.append(ident)        # Identifiers that aren't valid python

    if extras:
        extra_list = ', '.join([f"'{e}'" for e in extras])
        rval += f"\n{TAB}# Valid non-python identifiers "
        rval += f"\n{TAB}_extras = [{extra_list}]\n"
    rval += f'\n{TAB}_NS = Namespace("{uri}")'
    return rval


def genargs() -> ArgumentParser:
    """
    Generate an input string parser
    :return: parser
    """
    possible_formats = sorted(list(set(x.name for x in rdflib_plugins(None, rdflib_Parser) if '/' not in str(x.name))))

    parser = ArgumentParser(prog="generate_namespace", description="Generate a DefinedNamespace")
    parser.add_argument("prefix", help='Prefix to generate namespace for (example: skos)')
    parser.add_argument("uri", help="Prefix URI (example: http://www.w3.org/2004/02/skos/core#)" )
    parser.add_argument("rdf_file", help="Location or URL of RDF file to parse")
    parser.add_argument("-f", "--format", help="RDF file format", choices=possible_formats, default="turtle")
    return parser


def main(argv: Optional[List[str]] = None):
    opts = genargs().parse_args(argv)
    print(generate_namespace(opts.prefix, URIRef(opts.uri), opts.rdf_file), opts.format)


if __name__ == '__main__':
    main(sys.argv[1:])
