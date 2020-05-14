import unittest
from contextlib import redirect_stderr
from io import StringIO

from rdflib import URIRef

from tests.data.RDFMOD import RDFMOD
from tests.data.SKOS import SKOS


class DefinedNamespaceUnitTest(unittest.TestCase):
    def test_functionality(self):
        """ Test the basic functionality of the DefinedNamespace class"""
        self.assertEqual(SKOS.prefLabel, URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"))
        self.assertEqual(SKOS['altLabel'], URIRef("http://www.w3.org/2004/02/skos/core#altLabel"))
        self.assertEqual(repr(SKOS), 'Namespace("http://www.w3.org/2004/02/skos/core#")')

        txt = StringIO()
        with redirect_stderr(txt):
            self.assertEqual(SKOS.foo, URIRef("http://www.w3.org/2004/02/skos/core#foo"))
        self.assertTrue('UserWarning: Code: foo is not defined in namespace SKOS' in txt.getvalue())

    def test_extras(self):
        """
        Test non-python identifiers
        :return:
        """
        self.assertEqual(RDFMOD['class'], URIRef("http://www.w3.org/2000/01/rdf-schema#class"))
        self.assertEqual(RDFMOD['12345'], URIRef("http://www.w3.org/2000/01/rdf-schema#12345"))
        txt = StringIO()
        with redirect_stderr(txt):
            self.assertEqual(RDFMOD['12346'], URIRef("http://www.w3.org/2000/01/rdf-schema#12346"))
        self.assertTrue('UserWarning: Code: 12346 is not defined in namespace RDFMOD' in txt.getvalue())


if __name__ == '__main__':
    unittest.main()
