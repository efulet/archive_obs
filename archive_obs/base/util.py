"""
@created_at 2017-08-13
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

from datetime import datetime
from datetime import timedelta


def parse_input_date(str_input):
    """
    :param str_input:
    :return: datetime.datetime
    """
    try:
        dd = datetime.strptime(str_input, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        dd = datetime.strptime(str_input, '%Y-%m-%d')
    return dd


def daterange(from_date, to_date):
    """
    Generate a range a dates using a starting and end date
    :param from_date:
    :param to_date:
    :return: A yield with date
    """
    for n in range(int((to_date - from_date).days) + 1):
        yield from_date + timedelta(n)
