import os
import shutil
from unittest import main

from docscraper.spiders.docscraper import DocLinkExtractor, DocScraperSpider
from docscraper.api import crawl
import pandas as pd

from .base import BaseTestCase


class TestDocLinkExtractor(BaseTestCase):

    def setUp(self) -> None:
        super(self.__class__, self).setUp()
        self.extractor = DocLinkExtractor(self.EXTENSIONS)

    def tearDown(self) -> None:
        super(self.__class__, self).tearDown()
        self.extractor = None

    def test_deny_extensions(self):
        for ext in self.EXTENSIONS:
            self.assertNotIn(ext, self.extractor.deny_extensions)


class TestDocScraperSpider(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        """ Run crawl only once for all test cases in the class. """
        super(TestDocScraperSpider, cls).setUpClass()
        crawl(cls.ALLOWED_DOMAINS,
              cls.START_URLS,
              directory=cls.DIRECTORY,
              extensions=cls.EXTENSIONS)

    @classmethod
    def tearDownClass(cls):
        super(TestDocScraperSpider, cls).tearDownClass()
        shutil.rmtree(cls.DIRECTORY)

    def test_document_directories_created(self):
        directory = os.path.join(self.DIRECTORY, 'full')
        self.assertTrue(os.path.exists(directory))

    def test_documents_downloaded(self):
        directory = os.path.join(self.DIRECTORY, 'full')
        self.assertTrue(len(os.listdir(directory)) > 0)

    def test_file_listing(self):
        df = pd.read_csv(f"{self.DIRECTORY}/file-listing.csv")
        directory = os.path.join(self.DIRECTORY, 'full')
        count = sum([len(files) for r, d, files in os.walk(directory)])
        # file-listing is included in count
        self.assertTrue(df.shape[0] == count)

    def test_check_directory(self):
        self.failUnlessRaises(Exception, DocScraperSpider,
                              self.ALLOWED_DOMAINS,
                              self.START_URLS,
                              directory='./output',
                              extensions=self.EXTENSIONS)


if __name__ == "__main__":
    main()

