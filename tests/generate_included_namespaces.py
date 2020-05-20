import os
from dataclasses import dataclass
from typing import Tuple, List, Optional, Callable

from rdflib import Graph

from generate_namespace import generate_namespace
from prefixcc import PrefixCCMap
from tests import cwd

@dataclass
class GenEntry:
    pfx: str                       # Prefix
    url: str                       # Source of data
    fmt: Optional[str] = "turtle"  # Source format
    uri: Optional[str] = None      # URI if not in prefix.cc
    addl: Optional[Callable[[Graph], Graph]] = None    # Additional processing


prefixes = PrefixCCMap()

generate: List[GenEntry] = [
    GenEntry('CSVW', 'http://www.w3.org/ns/csvw'),
    GenEntry('DC', 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_elements.ttl'),
    GenEntry('DCMITYPE', 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_type.ttl'),
    GenEntry('DCAT', 'https://www.w3.org/ns/dcat2.ttl'),
    GenEntry('DCTERMS', 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl'),
    GenEntry('DCAM', 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_abstract_model.ttl'),
    GenEntry('DOAP', 'http://usefulinc.com/ns/doap', 'xml'),
    GenEntry('FOAF', 'http://xmlns.com/foaf/spec/index.rdf', 'xml'),
    GenEntry('ODRL2', 'https://www.w3.org/ns/odrl/2/ODRL22.ttl', uri='http://www.w3.org/ns/odrl/2/'),
    GenEntry('ORG', 'http://www.w3.org/ns/org#'),
    GenEntry('OWL', 'http://www.w3.org/2002/07/owl#'),
    GenEntry('PROF', 'https://www.w3.org/ns/dx/prof/profilesont.ttl'),
    GenEntry('PROV', 'http://www.w3.org/ns/prov', 'manual'),
    GenEntry('RDF', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
    GenEntry('RDFS', 'http://www.w3.org/2000/01/rdf-schema#'),
    GenEntry('SDO', 'https://schema.org/docs/jsonldcontext.json', 'json-ld'),
    GenEntry('SH', 'https://www.w3.org/ns/shacl.ttl'),
    GenEntry('SKOS', 'https://www.w3.org/2009/08/skos-reference/skos.rdf', 'xml'),
    GenEntry('SOSA', 'http://www.w3.org/ns/sosa/'),
    GenEntry('SSN', 'http://www.w3.org/ns/ssn/'),
    GenEntry('TIME', 'http://www.w3.org/2006/time#'),
    GenEntry('VOID', 'http://rdfs.org/ns/void#'),
    GenEntry('XMLNS', '', ''),
    # GenEntry('XSD', 'http://www.w3.org/2001/XMLSchema#'),
    GenEntry('VANN', 'file:///Users/solbrig/Downloads/vann-vocab-20100607.rdf', 'xml')
]

base = os.path.relpath(os.path.abspath(os.path.join(cwd, '..', 'definednamespace')), os.getcwd())


def gen():
    for entry in generate:
        if not entry.url:
            continue
        target = os.path.join(base, entry.pfx.upper() + ".py")
        with open(target, 'w') as output_file:
            output_file.write(generate_namespace(entry.pfx, entry.uri if entry.uri else prefixes[entry.pfx], entry.url, entry.fmt ))
        print(f"{target} written")


gen()