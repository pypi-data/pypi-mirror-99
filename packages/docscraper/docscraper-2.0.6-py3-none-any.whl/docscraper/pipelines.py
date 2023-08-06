import hashlib
import os

import requests
from scrapy.utils.python import to_bytes


class FileListingPipeline(object):
    """ Pipeline to parse metadata. """

    def process_item(self, item, spider):
        """
        :param item: the item passing through the item pipeline
        :type item: docscraper.items.DocScraperItem
        :param spider: the spider currently crawling
        :type spider: docscraper.spiders.DocScraperSpider
        :return: the parsed item object
        :rtype: docscraper.items.DocScraperItem
        """
        item['url'] = item['file_urls'][0]

        if len(item['files']) == 0:
            r = requests.get(item['url'])
            media_guid = hashlib.sha1(to_bytes(item['url'])).hexdigest()
            f, ext = os.path.splitext(item['url'])
            fname = '{}{}'.format(media_guid, ext)
            fpath = '{}/full'.format(spider.directory)
            os.makedirs(fpath, exist_ok=True)
            outfile = '{}/{}'.format(fpath, fname)
            with open(outfile, 'wb') as f:
                f.write(r.content)
            item['files'] = [{'url': r.url,
                              'path': 'full/{}'.format(fname),
                              'checksum': hashlib.md5(r.content).hexdigest(),
                              'status': r.status_code}]

        item['original_filename'] = item['url'].split('/')[-1]
        item['filetype'] = os.path.splitext(item['original_filename'])[-1]\
            .replace('.', '')\
            .upper()
        item['relative_path'] = item['files'][0]['path']
        item['checksum'] = item['files'][0]['checksum']
        item['status'] = item['files'][0]['status']

        return item





