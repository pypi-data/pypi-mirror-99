from datetime import datetime
import os
from unittest import main, TestCase


class BaseTestCase(TestCase):

    ALLOWED_DOMAINS = ["books.toscrape.com"]
    START_URLS = ["http://books.toscrape.com"]
    DIRECTORY = os.path.abspath("./tests/output")
    EXTENSIONS = ['.doc', '.docx', '.pdf', '.html']
    ROBOTSTXT_OBEY = False
    DOWNLOAD_DELAY = 0.25
    TIME_RANGE = [datetime(2015, 1, 1), datetime(2020, 1, 1)]


if __name__ == '__main__':
    main()
