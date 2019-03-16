import tempfile
import shutil
import unittest
import dokanki.converter.gdocs


class TestDocs(unittest.TestCase):
    docs_outliner = dokanki.converter.gdocs.GDocsConverter()

    def test_supports(self):
        self.assertTrue(self.docs_outliner.supports(
            "https://docs.google.com/document/d/1FJ_UmF86i_UBkQljC1ckblmNENh3gMNN6Lcl1psmfN8/edit#heading=h.a4n9hx8haown"))
        self.assertTrue(self.docs_outliner.supports(
            "https://docs.google.com/document/d/1CRANKa6MqfDt4jngnDMkbt_SDKthajGVqH9WWWXQb6Y/edit"))
        self.assertFalse(self.docs_outliner.supports(
            "https://mionskowski.pl/google.com/"
        ))
        self.assertFalse(self.docs_outliner.supports(
            "google.docx"
        ))

    def test_create_download_url(self):
        self.assertTrue(self.docs_outliner.create_download_url(
            "https://docs.google.com/document/d/1FJ_UmF86i_UBkQljC1ckblmNENh3gMNN6Lcl1psmfN8/edit#heading=h.a4n9hx8haown").index(
            "1FJ_UmF86i_UBkQljC1ckblmNENh3gMNN6Lcl1psmfN8") is not None)

    def test_unzip_entry(self):
        temp_dir = tempfile.mkdtemp(prefix="dokanki-test")
        if temp_dir is None:
            self.skipTest("Can't create temp dir")
            return
        self.assertTrue(self.docs_outliner._unzip_entry("./docs.zip", temp_dir).endswith(
            "PBDOpracowaniepytazegzaminu2016i2017.html"))
        shutil.rmtree(temp_dir)
