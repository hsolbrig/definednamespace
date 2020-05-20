from rdflib import URIRef, Namespace
from definednamespace import DefinedNamespace


class DCMITYPE(DefinedNamespace):
    """
    DCMI Type Vocabulary
    
    Generated from: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_type.ttl
    Date: 2020-05-20 08:25:37.040494

    dcterms:modified "2012-06-14"^^xsd:date
    dcterms:publisher <http://purl.org/dc/aboutdcmi#DCMI>
    """
    
    # http://www.w3.org/2000/01/rdf-schema#Class
    Collection: URIRef              # An aggregation of resources.
    Dataset: URIRef                 # Data encoded in a defined structure.
    Event: URIRef                   # A non-persistent, time-based occurrence.
    Image: URIRef                   # A visual representation other than text.
    InteractiveResource: URIRef     # A resource requiring interaction from the user to be understood, executed, or experienced.
    MovingImage: URIRef             # A series of visual representations imparting an impression of motion when shown in succession.
    PhysicalObject: URIRef          # An inanimate, three-dimensional object or substance.
    Service: URIRef                 # A system that provides one or more functions.
    Software: URIRef                # A computer program in source or compiled form.
    Sound: URIRef                   # A resource primarily intended to be heard.
    StillImage: URIRef              # A static visual representation.
    Text: URIRef                    # A resource consisting primarily of words for reading.

    _NS = Namespace("http://purl.org/dc/dcmitype/")
