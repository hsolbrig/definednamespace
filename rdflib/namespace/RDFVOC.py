from definednamespace.RDF import RDF
from rdflib.term import URIRef


class RDFVOC(RDF):
    # http://www.w3.org/TR/rdf-syntax-grammar/#eventterm-attribute-URI
    # A mapping from unqualified terms to their qualified version.
    RDF: URIRef
    Description: URIRef
    ID: URIRef
    about: URIRef
    parseType: URIRef
    resource: URIRef
    li: URIRef
    nodeID: URIRef
    datatype: URIRef
