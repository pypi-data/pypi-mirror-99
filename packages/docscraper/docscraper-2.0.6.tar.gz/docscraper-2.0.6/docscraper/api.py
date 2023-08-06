from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .spiders import DocScraperSpider


def crawl(domains,
          start_urls=[],
          directory='./output',
          extensions=['.pdf', '.docx', '.doc', '.txt'],
          robotstxt_obey=True,
          download_delay=0,
          time_range=None):
    """ Run the crawler from a Python script.

    :param domains: the domains allowed to be crawled
    :type domains: list
    :param directory: the output directory for downloaded files
    :type directory: str
    :param extensions: the document extension types to download
    :type extensions: list
    :param robotstxt_obey: whether to obey robots.txt instructions
    :type robotstxt_obey: bool
    :param wayback_machine_time_range: dates for crawling the wayback machine
    :type wayback_machine_time_range: tuple

    """
    settings = get_project_settings()

    settings['ROBOTSTXT_OBEY'] = robotstxt_obey
    settings['DOWNLOAD_DELAY'] = download_delay

    # Set directory path for file downloads
    settings['FILES_STORE'] = directory

    settings['FEEDS'] = {
        '{}/file-listing.csv'.format(directory): {'format': 'csv'}
    }
    settings['FEED_EXPORT_FIELDS'] = ['domain', 'url', 'relative_path',
                                      'checksum', 'status', 'url_date',
                                      'filetype', 'filename']

    if time_range is not None:
        settings['DOWNLOADER_MIDDLEWARES'] = {
            'scrapy_wayback_machine.WaybackMachineMiddleware': 5
        }
        settings['WAYBACK_MACHINE_TIME_RANGE'] = time_range

    process = CrawlerProcess(settings)
    process.crawl(DocScraperSpider,
                  domains,
                  start_urls,
                  directory=directory,
                  extensions=extensions,
                  time_range=time_range
                  )

    process.start()

    return
