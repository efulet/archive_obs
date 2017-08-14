#!/usr/bin/env python

"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import logging.config
import sys

from archive_obs.base.options import Options
from archive_obs.base.stats import show
from archive_obs.conf import settings
from archive_obs.parsers.parser_csv import ParserCsv
from archive_obs.scrapers.gemini_scraper import GeminiScraper

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


def main(args=None):
    try:
        if not args:
            args = sys.argv

        options = Options()
        if not len(args) > 1:
            options.print_help()
            return 1
        parsed_args = options.parse(args[1:])

        # This proof-of-concept is just scraping Gemini Archive.
        # It's using only the date input field. For getting the maximum data from the web
        # service, we are adding only one date into the field at a time from starting date
        # until the end date.
        # We can add more archives and another inputs in the future for filtering data
        logger.info('Welcome to Archive Observations project')

        # Start fetch data. The data is stored as text (raw) format.
        if parsed_args.fetch:
            gemini_scraper = GeminiScraper({
                'from_date': parsed_args.from_date,
                'to_date': parsed_args.to_date,
            })
            gemini_scraper.fetch()

        # Parse the raw FITS headers files and convert them in CSV format (csv file delimiter
        # by tab). Take files in a range of dates
        if parsed_args.parse:
            parser = ParserCsv({
                'from_date': parsed_args.from_date,
                'to_date': parsed_args.to_date,
            })
            parser.parse()

        # Show a map with the observation coordinates. Also, you can save it as PDF file.
        if parsed_args.show:
            show(parsed_args.save_map)

        return 0
    except Exception as err:
        logger.error(str(err))


if __name__ == '__main__':
    sys.exit(main())
