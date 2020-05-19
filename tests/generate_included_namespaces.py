import os
from dataclasses import dataclass
from typing import Tuple, List

from generate_namespace import generate_namespace
from tests import cwd

@dataclass
class GenEntry:
    pfx: str
    uri: str
    url: str
    fmt: str


generate: List[GenEntry] = [
    GenEntry('CSVW', 'http://www.w3.org/ns/csvw#', 'http://www.w3.org/ns/csvw', 'turtle'),
    GenEntry('DC', '', '', ''),
    GenEntry('DCAT', '', '', ''),
    GenEntry('DCTERMS', '', '', ''),
    GenEntry('DOAP', '', '', ''),
    GenEntry('FOAF', '', '', ''),
    GenEntry('ODRL2', '', '', ''),
    GenEntry('ORG', '', '', ''),
    GenEntry('OWL', '', '', ''),
    GenEntry('PROF', '', '', ''),
    GenEntry('PROV', '', '', ''),
    GenEntry('RDF', '', '', ''),
    GenEntry('RDFS', '', '', ''),
    GenEntry('SDO', '', '', ''),
    GenEntry('SH', '', '', ''),
    GenEntry('SKOS','http://www.w3.org/2004/02/skos/core#', 'https://www.w3.org/2009/08/skos-reference/skos.rdf', 'xml'),
    GenEntry('SOSA', '', '', ''),
    GenEntry('SSN', '', '', ''),
    GenEntry('TIME', '', '', ''),
    GenEntry('VOID', '', '', ''),
    GenEntry('XMLNS', '', '', ''),
    GenEntry('XSD', '', '', '')
]

base = os.path.relpath(os.path.abspath(os.path.join(cwd, '..', 'definednamespace')), os.getcwd())

for entry in generate:
    if not entry.uri:
        continue
    target = os.path.join(base, entry.pfx.upper() + ".py")
    with open(target, 'w') as output_file:
        output_file.write(generate_namespace(entry.pfx, entry.uri, entry.url, entry.fmt ))
    print(f"{target} written")
