import os
import re
from dataclasses import dataclass
from typing import List, Optional, Callable

from rdflib import Graph

from generate_namespace import generate_namespace
from generate_xsd_namespace import generate_xsd_namespace
from prefixcc import PrefixCCMap
from tests import cwd


@dataclass
class GenEntry:
    pfx: str                       # Prefix
    url: str                       # Source of data
    fmt: Optional[str] = "turtle"  # Source format
    uri: Optional[str] = None      # URI if not in prefix.cc
    addl: Optional[Callable[[Graph], Graph]] = None    # Additional processing
    title: Optional[str] = None     # Title.  If present, use XSD processor


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
    GenEntry('QB', 'http://purl.org/linked-data/cube#'),
    GenEntry('RDF', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
    GenEntry('RDFS', 'http://www.w3.org/2000/01/rdf-schema#'),
    GenEntry('SDO', 'http://schema.org/version/latest/schema.ttl'),
    GenEntry('SH', 'https://www.w3.org/ns/shacl.ttl'),
    GenEntry('SKOS', 'https://www.w3.org/2009/08/skos-reference/skos.rdf', 'xml'),
    GenEntry('SOSA', 'http://www.w3.org/ns/sosa/'),
    GenEntry('SSN', 'http://www.w3.org/ns/ssn/'),
    GenEntry('TIME', 'http://www.w3.org/2006/time#'),
    GenEntry('VOID', 'http://rdfs.org/ns/void#'),
    GenEntry('XSD', '../schemas/datatypes.xsd', 'xsd', 'http://www.w3.org/2001/XMLSchema#',
             title='W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes'),
    GenEntry('VANN', 'https://vocab.org/vann/vann-vocab-20100607.rdf', 'xml')
]

base = os.path.relpath(os.path.abspath(os.path.join(cwd, '..', 'definednamespace')), os.getcwd())


def gen(prefix: Optional[str] = None) -> int:
    def adjust(txt: str) -> str:
        return re.sub(r'Date: .*\n', 'Date: \n', txt)

    def changed(file_name: str, expected_text: str) -> bool:
        if os.path.exists(file_name):
            with open(file_name) as current_file:
                current_text = current_file.read()
            return adjust(current_text) != adjust(expected_text)
        return True

    def generate_entry(entry: GenEntry) -> bool:
        if not entry.url:
            return False
        target = os.path.join(base, entry.pfx.upper() + ".py")
        python = generate_namespace(entry.pfx, entry.uri if entry.uri else prefixes[entry.pfx], entry.url, entry.fmt) \
            if entry.fmt != 'xsd' else generate_xsd_namespace(entry.pfx, entry.uri, entry.url, entry.title)
        if changed(target, python):
            with open(target, 'w') as output_file:
                output_file.write(python)
            print(f"{target} written")
        else:
            print(f"{target} already exists and has not changed")
        return True

    ngenerated = 0
    for entry in generate:
        if (not prefix or prefix == entry.pfx) and generate_entry(entry):
            ngenerated += 1
    return ngenerated


print(f"{gen('')} files written")