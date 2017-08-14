"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import logging
import os
import re
import requests
import progressbar

from pyquery import PyQuery

from archive_obs.base.util import daterange
from archive_obs.conf import settings
from archive_obs.scrapers.base_scraper import BaseScraper


class GeminiScraper(BaseScraper):
    """
    Scraper Gemini Archive
    """

    ARCHIVE_NAME = 'gemini'

    def __init__(self, kwargs, logger=None):
        super(GeminiScraper, self).__init__(kwargs)

        progressbar.streams.wrap_stderr()
        self.logger = logger or logging.getLogger(__name__)

        self.url = settings.SCRAPER_ARCHIVE_URLS.get(self.ARCHIVE_NAME)

    def fetch(self):
        self.logger.info('Scraping data from {} archive'.format(self.ARCHIVE_NAME.title()))

        for single_date in daterange(self.from_date, self.to_date):
            self.logger.info('Fetching date {}'.format(single_date.strftime('%Y-%m-%d')))

            try:
                # Make a request using the search form URL
                r = requests.get('{}/searchform/{}'.format(self.url,
                                                           single_date.strftime('%Y%m%d')))
                pq = PyQuery(r.content)

                # Initialize counters
                self._rows_counter = 0
                self._dump_counter = 0

                # Extract all links from the second column, which are the fits header links
                a_links = pq('table tr.alternating td:nth-child(2) a')
                self._total_rows = len(a_links)
                self.logger.info('Total rows in results: {}'.format(self._total_rows))

                # For be nicer, we use progressbar ;)
                with progressbar.ProgressBar(widgets=['Getting FITS header: ',
                                                      progressbar.Percentage()],
                                             max_value=self._total_rows,
                                             redirect_stdout=True) as bar:
                    bar.update(0)
                    for link in a_links.items():
                        self._rows_counter += 1
                        bar.update(self._rows_counter)

                        try:
                            # Make a request to the FITS header link
                            fits_header_href = link.attr('href')
                            r = requests.get('{}/{}'.format(self.url, fits_header_href))

                            filename = re.sub(r'/', '_', fits_header_href).strip('_') + \
                                settings.FITS_HEADER_EXTENSION
                            try:
                                filename = link.text() + settings.FITS_HEADER_EXTENSION
                            except Exception as err:
                                pass

                            try:
                                # Store the data on disk using a simple method
                                self._dump(single_date, filename, r.content)
                            except Exception as err:
                                self.logger.error('Oops, got an error while dumping '
                                                  'file: {}'.format(str(err)))
                                continue
                        except Exception as err:
                            self.logger.error('Oops, got an error while requesting FITS '
                                              'headers: {}'.format(str(err)))
                            continue

                self._audit()
            except Exception as err:
                self.logger.error('Oops, got an error while fetching results: {}'.format(str(err)))
                continue

    def _dump(self, current_date, filename, content):
        path = os.path.join(settings.RAW_PATH, self.ARCHIVE_NAME,
                            current_date.strftime('%Y%m%d'), filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content.decode(settings.ENCODING_UTF8))
        self._dump_counter += 1  # keep counter of how much files are stored
