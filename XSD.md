# XML Schema Data Types
The [XML Schema Datatypes](https://www.w3.org/TR/xmlschema-2/) present an interesting challenge.  While we would be 
happy to be corrected, there does not appear to be a definitive RDF representation of the XML Schema datatypes.  To
add insult to injury, while there _is_ a formal schema for XML Schema: https://www.w3.org/2009/XMLSchema/datatypes.xsd,
the schema itself appears to only be available [as text](https://www.w3.org/TR/xmlschema-2/#schema).  

For our purposes, we have copied the XSD form of the XML Schema Definition out of the standards document and created a
[local copy](schemas/datatypes.xsd.)

## Generating the XSD.py DefinedNamespace
```bash
> pip install definednamespace
> generate_xsd_namespace xsd http://www.w3.org/2001/XMLSchema# schemas/datatypes.xsd -t "XML Schema 1.1 Datatypes" > XSD.py
```