import os
from unittest import main, TestCase


class BaseTestCase(TestCase):

    ALLOWED_DOMAINS = ["books.toscrape.com"]
    START_URLS = []
    DIRECTORY = os.path.abspath("./tests/output")
    EXTENSIONS = [".html", ".pdf", ".docx", ".doc", ".svg"]
    ROBOTSTXT_OBEY = True
    DOWNLOAD_DELAY = 0
    TIME_RANGE = None


if __name__ == '__main__':
    main()
