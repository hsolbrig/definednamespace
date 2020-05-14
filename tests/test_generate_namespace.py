import os
import unittest
from types import ModuleType
from typing import Union

from rdflib import RDF, Namespace, SKOS, RDFS

from generator.generate_namespace import generate_namespace
from tests import test_dir


class GenerateNamespaceTestCase(unittest.TestCase):
    def do_test(self, namespace: str, prefix: Namespace, loc: Union[Namespace, str], format: str="turtle") -> None:
        """
         Generate test and compare a test file
        :param namespace: namespace to generate
        :param prefix: URI Prefix
        :param loc: location of RDF input
        :param format: format of RDF input
        """
        python_text = generate_namespace(namespace, prefix, loc, rdf_format=format)

        # Make sure the python is valid
        spec = compile(python_text, 'test', 'exec')
        module = ModuleType('test')
        exec(spec, module.__dict__)

        # Compare the output to what we're expecting
        expected_fname = os.path.join(test_dir, namespace.upper()+ ".py")
        expected_exists = os.path.exists(expected_fname)
        if not expected_exists:
            with open(expected_fname, 'w') as f:
                f.write(python_text)
        with open(expected_fname) as f:
            expected = f.read()
        self.assertEqual(expected, python_text, f"Mismatch in {expected_fname}")
        self.assertTrue(expected_exists, f"{expected_fname} regenerated - run test again")

    def test_rdf(self):
        """ Test generating RDF from a web source """
        self.do_test('rdf', RDF, RDF)

    def test_skos(self):
        """ Test generating SKOS from a file """
        self.do_test('skos', SKOS, os.path.join(test_dir, 'skos.rdf'), 'xml')

    def test_non_identifiers(self):
        """ Test generation for non-python identifiers """
        self.do_test('rdfmod', RDFS, os.path.join(test_dir, 'rdf-schema_mod.ttl'))


if __name__ == '__main__':
    unittest.main()
