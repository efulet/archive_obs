"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

from argparse import ArgumentParser, ArgumentTypeError

from datetime import date
from datetime import datetime
from datetime import timedelta


class Options:
    """
    Define several options for the program
    """
    def __init__(self):
        self.parser = ArgumentParser()
        self._init_parser()

    @staticmethod
    def parse_input_date(str_date):
        """
        :param str_date:
        :return: datetime.datetime
        """
        try:
            return datetime.strptime(str_date, '%Y-%m-%d')
        except ValueError:
            msg = 'Not a valid date: {0}'.format(str_date)
            raise ArgumentTypeError(msg)

    def _init_parser(self):
        self.parser.add_argument(
            '--fetch',
            action='store_true',
            dest='fetch',
            default=False,
            help='Fetch FITS headers from archives',
        )

        self.parser.add_argument(
            '-f', '--from_date',
            type=Options.parse_input_date,
            action='store',
            dest='from_date',
            default=date.today() - timedelta(days=1),
            help='Start date for extracting data',
        )

        self.parser.add_argument(
            '-t', '--to_date',
            type=Options.parse_input_date,
            dest='to_date',
            default=date.today() - timedelta(days=1),
            help='End date for extracting data',
        )

        self.parser.add_argument(
            '--parse',
            action='store_true',
            dest='parse',
            default=False,
            help='Parse the raw FITS headers files and convert them in CSV format',
        )

        self.parser.add_argument(
            '--show',
            action='store_true',
            dest='show',
            default=False,
            help='Show a map with the observation coordinates',
        )

        self.parser.add_argument(
            '--save-map',
            action='store_true',
            dest='save_map',
            default=False,
            help='Save the map as PDF file',
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)

    def print_help(self):
        self.parser.print_help()
