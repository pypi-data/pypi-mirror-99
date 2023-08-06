from datetime import datetime, timezone
import logging
import os
import re
from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging

from ..items import DocscraperItem


class DocLinkExtractor(LinkExtractor):  # lgtm [py/missing-call-to-init]

    def __init__(self, domains, extensions, *args, **kwargs):
        """ Custom link extractor to extract document links.

        :param extensions: a list of file extensions for extraction
        :type extensions: list

        """

        super(DocLinkExtractor, self).__init__(*args, **kwargs)
        # Keep the default values in deny_extensions except the ones we want
        self.deny_extensions = [e for e in self.deny_extensions if
                                e not in extensions]


class DocScraperSpider(CrawlSpider):

    name = "DocScraperSpider"
    handle_httpstatus_list = [404]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self,
                 domains,
                 start_urls=[],
                 directory='./output',
                 extensions=['.pdf', '.doc', '.docx'],
                 time_range=None,
                 **kwargs):
        """ The Spider to crawl site(s) for documents.

        :param domains: A list of allowed domains for the crawl
        :type domains: list
        :param start_urls: A list of the start urls for the crawl
        :type start_urls: list
        :param directory: The directory path to which to save documents
        :type directory: str
        :param extensions: A list of document extensions
                           (e.g., [".pdf", ".doc", ".docx"])
        :type extensions: list, optional
        :param time_range: A tuple of datetime values or YYYYmmddHHMMSS strings
        :param time_range: 2-value tuple

        """

        self.items = []
        self.directory = directory
        self.extensions = extensions
        self.time_range = self.set_time_range(time_range)
        extractor = DocLinkExtractor(domains, extensions)
        self.rules = (
            Rule(extractor, follow=True,
                 callback='parse_item',
                 process_links='process_links'
                 ),
        )
        # parse the allowed domains and start urls
        self.allowed_domains = []
        self.start_urls = start_urls
        if self.time_range is not None:
            domains.append('web.archive.org')
        for domain in domains:
            url_parts = domain.split('://')
            unqualified_url = url_parts[-1]
            url_scheme = url_parts[0] if len(url_parts) > 1 else 'http'
            full_url = '{0}://{1}'.format(url_scheme, unqualified_url)
            bare_domain = unqualified_url.split('/')[0]
            self.allowed_domains.append(bare_domain)
            if len(start_urls) == 0 and bare_domain != 'web.archive.org':
                self.start_urls.append(full_url) # lgtm [py/modification-of-default-value]

        super(DocScraperSpider, self).__init__(**kwargs)

        self.check_directory(self.directory)

    def parse_start_url(self, response):
        # scrapy doesn't call the callbacks for the start urls by default,
        # this overrides that behavior so that any matching callbacks are called
        for rule in self._rules:
            if rule.link_extractor._link_allowed(response):
                if rule.callback:
                    rule.callback(response)

    @staticmethod
    def set_time_range(time_range):
        if time_range is None:
            return None

        # allow a single time to be passed in place of a range
        if type(time_range) not in [tuple, list]:
            time_range = (time_range, time_range)

        # translate the times to unix timestamps
        def parse_time(time):
            if type(time) in [int, float, str]:
                time = int(time)
                # realistic timestamp range
                if 10 ** 8 < time < 10 ** 13:
                    return time
                # otherwise archive.org timestamp format (possibly truncated)
                time_string = str(time)[::-1].zfill(14)[::-1]
                time = datetime.strptime(time_string, '%Y%m%d%H%M%S')
                time = time.replace(tzinfo=timezone.utc)
            return time.timestamp()

        return [parse_time(time) for time in time_range]

    @staticmethod
    def check_directory(directory):
        directory = os.path.abspath(directory)
        if os.path.exists(directory) and len(os.listdir(directory)) > 0:
            raise Exception('Directory is not empty. Please provide an empty '
                            'or non-existent directory path.')
        return

    def process_links(self, links):
        """ Limit links to allowed domains only.

        This method prevents the scraper from expanding its search beyond the
        scope of the project.
        """
        domains = [d for d in self.allowed_domains if d != 'web.archive.org']
        domains = '^https?\://(?:%s)' % '|'.join(domains)
        allowed_links = []
        for link in links:
            link.url = re.split('/web/(\d{14})/', link.url)[-1]
            if re.match(domains, link.url) and 'screenshot' not in link.url:
                allowed_links.append(link)
        return allowed_links

    def parse_item(self, response):
        """ Download document and save metadata to files attribute. """

        if response.status == 404:
            return

        item = DocscraperItem()

        f = response.url.split("/")[-1]
        ext = os.path.splitext(f)[-1]

        if ext in self.extensions:
            url = response.meta.get('wayback_machine_url', response.url)
            timestamp = response.meta.get('wayback_machine_time',
                                          datetime.now())

            domain = urlparse(url).netloc

            item['domain'] = domain
            item['url_date'] = timestamp
            item['file_urls'] = [url]

            yield item







