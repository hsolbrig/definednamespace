import warnings
from typing import List

from rdflib import Namespace


class DefinedNamespaceMeta(type):
    __doc__ = """
    Utility metaclass for generating URIRefs with a common prefix

    >>> from rdflib import DefinedNamespaceMeta
    >>>
    >>> class FOO(metaclass=DefinedNamespaceMeta):
    >>>     bar: URIRef
    >>>     fum: URIRef
    >>>     _NS = Namespace("http://example.org/")
    >>>
    >>> FOO.bar # as attribute
    rdflib.term.URIRef('http://example.org/Person')
    >>> FOO['first-name'] # as item - for things that are not valid python identifiers
    rdflib.term.URIRef('http://example.org/first-name')

    """

    _NS: Namespace
    _warn: bool = True
    _extras: List[str] = []

    def __getitem__(cls, name, default=None):
        if cls._warn:
            if name not in cls.__annotations__ and name not in cls._extras:
                warnings.warn(f"Code: {name} is not defined in namespace {cls.__name__}", stacklevel=3)
        return cls._NS[name]

    def __getattr__(cls, name):
        return cls.__getitem__(name)

    def __repr__(cls):
        return f'Namespace("{cls._NS}")'


class DefinedNamespace(metaclass=DefinedNamespaceMeta):
    def __init__(self):
        raise TypeError("DefinedNamespace may not be instantiated")
