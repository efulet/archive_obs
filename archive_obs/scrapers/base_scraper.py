"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import logging


class BaseScraper:
    """
    Define all methods which a scraper have to implement
    """

    def __init__(self, kwargs, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        self.from_date = kwargs.get('from_date')
        self.to_date = kwargs.get('to_date')

        # We can use these numbers for checking how much data was processed
        self._total_rows = 0
        self._rows_counter = 0
        self._dump_counter = 0

    def fetch(self):
        """
        Extract data from an archive
        """
        raise NotImplementedError

    def _audit(self):
        """
        A simple way to audit extracted data
        """
        self.logger.debug('-' * 40)

        self.logger.debug('Total rows in results: {}'.format(self._total_rows))
        self.logger.debug('Total rows counted: {}'.format(self._rows_counter))
        self.logger.debug('Total FITS headers files: {}'.format(self._dump_counter))

        if self._total_rows != self._rows_counter:
            self.logger.debug('Oops, total rows and total rows counted doesn\'t match')

        if self._total_rows != self._dump_counter:
            self.logger.debug('Oops, total rows and downloaded files doesn\'t match')

        self.logger.debug('-' * 40)

    def _dump(self, current_date, filename, content):
        """
        A simple method for storing data on disk
        :param current_date: Date of the extracted data
        :param filename: Name of file
        :param content: Extracted data from Web service
        """
        raise NotImplementedError
