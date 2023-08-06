import os
import shutil
from unittest import main

import pandas as pd

from docscraper.api import crawl
from .base import BaseTestCase


class TestCrawlCurrent(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        """ Run crawl only once for all test cases in the class. """
        super(TestCrawlCurrent, cls).setUpClass()
        crawl(cls.ALLOWED_DOMAINS,
              directory=cls.DIRECTORY,
              extensions=cls.EXTENSIONS,
              robotstxt_obey=cls.ROBOTSTXT_OBEY,
              download_delay=cls.DOWNLOAD_DELAY,
              time_range=cls.TIME_RANGE)

    @classmethod
    def tearDownClass(cls):
        super(TestCrawlCurrent, cls).tearDownClass()
        shutil.rmtree(cls.DIRECTORY)

    def test_current_scrape(self):

        df = pd.read_csv(f"{self.DIRECTORY}/file-listing.csv")
        directory = os.path.join(self.DIRECTORY, 'full')
        count = sum([len(files) for r, d, files in os.walk(directory)])
        # file-listing is included in count
        self.assertTrue(df.shape[0] == count)


class TestCrawlTimeRange(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        """ Run crawl only once for all test cases in the class. """
        super(TestCrawlTimeRange, cls).setUpClass()
        crawl(cls.ALLOWED_DOMAINS,
              directory=cls.DIRECTORY,
              extensions=cls.EXTENSIONS,
              robotstxt_obey=False,
              download_delay=0.1,
              time_range=('20170101000000', '20170630000000'))

    @classmethod
    def tearDownClass(cls):
        super(TestCrawlTimeRange, cls).tearDownClass()
        shutil.rmtree(cls.DIRECTORY)

    def test_wayback_machine(self):

        df = pd.read_csv(f"{self.DIRECTORY}/file-listing.csv")
        directory = os.path.join(self.DIRECTORY, 'full')
        count = sum([len(files) for r, d, files in os.walk(directory)])
        # file-listing is included in count
        self.assertTrue(df.shape[0] == count)


if __name__ == "__main__":
    main()
