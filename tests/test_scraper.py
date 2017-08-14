"""
@created_at 2017-08-13
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import os

from datetime import date

from archive_obs.conf import settings
from archive_obs.scrapers.gemini_scraper import GeminiScraper


def test_fetch_ok(request_faker):
    single_date = date(2017, 5, 1)
    gemini_scraper = GeminiScraper({
        'from_date': single_date,
        'to_date': single_date,
    })
    gemini_scraper.fetch()

    expected_path = os.path.join(settings.DATA_PATH, 'responses', 'N20170501S0001.fits.dat')
    got_path = os.path.join(settings.RAW_PATH, 'gemini', '20170501', 'N20170501S0001.fits.dat')

    assert os.path.exists(got_path)

    expected_content = ''
    with open(expected_path, 'rb') as f:
        expected_content = f.read()
    got_content = ''
    with open(got_path, 'rb') as f:
        got_content = f.read()
    assert expected_content == got_content


# TODO
def test_fetch_fail():
    assert True
