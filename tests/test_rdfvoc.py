import unittest

from definednamespace.RDFVOC import RDFVOC


class RDFVOCTestCase(unittest.TestCase):
    def test_rdfvoc(self):
        """ Test an extended namespace (RDFVOC extends RDF) """
        self.assertEqual(RDFVOC.about, '')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
