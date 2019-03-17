import os
import re
import shutil
import tempfile
import zipfile

import requests

from dokanki.converter import converter
import dokanki


class GDocsConverter(converter.Converter):
    """
    Downloads and extracts Google Docs documents by requesting them in ZIP format.
    """
    _drive_url_pattern = re.compile("(?:http[s]?://)?(?:www\\.)?docs\\.google\\.com/document/d/([^/]+)/.*")
    _download_url = "https://docs.google.com/document/d/{}/export?format=zip"

    @staticmethod
    def _unzip_entry(zip_file, target):
        zip_ref = zipfile.ZipFile(zip_file, 'r')
        zip_ref.extractall(target)
        zip_ref.close()
        dokanki.logger.info("Unzipping {} to {}".format(zip_file, target))

        for file in os.listdir(target):
            if file.endswith("html"):
                return "{}/{}".format(target, file)
        return None

    def supports(self, url):
        return self._drive_url_pattern.match(url)

    def create_download_url(self, url):
        assert self.supports(url)
        return self._download_url.format(self._drive_url_pattern.search(url).groups(0)[0])

    def download(self, url, target):
        assert self.supports(url)

        response = requests.get(self.create_download_url(url), stream=True)

        if response.status_code != 200:
            del response
            raise ConnectionError("invalid status code {}".format(response.status_code))

        with open(target, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        dokanki.logger.info("Downloading file from {}".format(url))
        return target

    def convert(self, url):
        temp_dir = tempfile.mkdtemp(prefix="dokanki")

        zip_file = self.download(url, "{}/docs.zip".format(temp_dir))
        index_file = self._unzip_entry(zip_file, temp_dir)
        os.remove(zip_file)

        if index_file is None:
            raise FileNotFoundError("not a docs document")

        return index_file
