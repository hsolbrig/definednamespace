# DefinedNamespace package
Proposed replacement for the current rdflib ClosedNamespace module.

The general notion is that, unless the warning flag (`_warn`) is set to false, a warning will be issued whenever an
element in a namsepace is referenced that isn't formally defined.

The definitions in the classes allow IDE's to do search and substitution.

See: [tests/data/RDF.py]() , [tests/data/SKOS.py]() and [tests/data/RDFMOD.py]() for examples. 

