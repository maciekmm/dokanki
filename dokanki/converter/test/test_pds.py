import unittest
import dokanki.converter.pds


class TestPDS(unittest.TestCase):
    pds_converter = dokanki.converter.pds.PDSConverter()

    def test_support(self):
        self.assertTrue(self.pds_converter.supports('test.pds'))
        self.assertFalse(self.pds_converter.supports('pds.txt'))
        self.assertFalse(self.pds_converter.supports('test/pds'))
