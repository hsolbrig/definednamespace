

def fill_template(namespace: str, header: str, body: str) -> str:
    return f"""from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class {namespace.upper()}(DefinedNamespace):
    {header}
    {body}
"""
