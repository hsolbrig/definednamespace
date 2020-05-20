from rdflib import URIRef, Namespace
from definednamespace import DefinedNamespace


class DCAM(DefinedNamespace):
    """
    Metadata terms for vocabulary description
    
    Generated from: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_abstract_model.ttl
    Date: 2020-05-20 08:25:38.620024

    dcterms:modified "2012-06-14"^^xsd:date
    dcterms:publisher <http://purl.org/dc/aboutdcmi#DCMI>
    """
    
    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    domainIncludes: URIRef          # A suggested class for subjects of this property.
    memberOf: URIRef                # A relationship between a resource and a vocabulary encoding scheme which indicates that the resource is a member of a set.
    rangeIncludes: URIRef           # A suggested class for values of this property.

    _NS = Namespace("http://purl.org/dc/dcam/")
