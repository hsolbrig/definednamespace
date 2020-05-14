from keyword import kwlist
from typing import Dict, List, Union, Optional

from rdflib import Graph, URIRef, Namespace, SKOS, RDFS, RDF
from rdflib.term import Node

COMMENT_COL = 24
descriptions = [
    SKOS.definition,
    SKOS.prefLabel,
    RDFS.comment,
    RDFS.label
]


def generate_namespace(namespace: str, prefix: Union[str, URIRef, Namespace], rdf_loc: Union[str, URIRef, Namespace],
                       rdf_format: str = "turtle") -> str:
    """
    Return a Python module that represents the namespace
    :param namespace: Namespace to generate (e.g. "skos")
    :param prefix: Namespace prefix (e.g. "http://www.w3.org/2004/02/skos/core#")
    :param rdf_loc: file or URL of rdf
    :param rdf_format: format of RDF
    :return: text for resource
    """
    return f"""from rdflib import URIRef, Namespace
from definednamespace import DefinedNamespace


class {namespace.upper()}(DefinedNamespace):
    {_body(str(prefix), str(rdf_loc), rdf_format)}
"""


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

def _body(prefix: str, rdf_loc: str, rdf_format: str = "turtle") -> str:
    """
    Create the body of a DefinedNamespace from standard RDF
    :param prefix: Prefix to generate
    :param rdf_loc: the path to an RDF file.  Can be a URL or a file name
    :param rdf_format: format of rdf_loc
    :return: Body for a DefinedNamespace
    """
    contents: Dict[URIRef, List[URIRef]] = dict()
    rval = ""
    g = Graph()
    g.load(rdf_loc, format=rdf_format)

    # Sort the subjects in the namespace by type
    for s in sorted(set(g.subjects())):
        if str(s).startswith(prefix):
            contents.setdefault(_longest_type(s, RDFS.Resource, g), []).append(s)

    extras: List[URIRef] = []
    for k in sorted(contents.keys()):
        vs = contents[k]
        if len(vs) > 1 and str(vs[0])[len(prefix):]:
            rval += f"\n\t# {k}\n"
            for v in sorted(vs):
                ident = str(v)[len(prefix):]
                if ident.isidentifier() and not ident in kwlist:
                    doc = _description_for(v, g).strip().replace('\n', ' ')
                    pad = max(COMMENT_COL - len(ident), 2) * " "
                    rval += f"\t{ident}: URIRef{pad}# {doc}\n"
                else:
                    extras.append(ident)        # Identifiers that aren't valid python

    if extras:
        extra_list = ', '.join([f"'{e}'" for e in extras])
        rval += "\n\t# Valid non-python identifiers "
        rval += f"\n\t_extras = [{extra_list}]\n"
    rval += f'\n\t_NS = Namespace("{prefix}")'
    return rval



