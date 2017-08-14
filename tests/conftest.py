"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import pytest
import os

os.environ['TESTING'] = 'test'  # noqa
os.environ['PYTHON_ENV'] = 'test'  # noqa

from archive_obs.conf import settings


class HttpResponse:
    def __init__(
            self,
            status_code,
            headers,
            content_type,
            content=None,
            cookies=[],
            url='foo.html',
    ):
        self.status_code = status_code
        self.headers = {
            'Content-Type': content_type,
        }
        self.content = content
        self.cookies = cookies
        self.url = url


@pytest.fixture
def request_faker(monkeypatch):
    def get_faker(url, **kwargs):
        response = 'hello'

        if 'searchform' in url:
            path = os.path.join(settings.DATA_PATH, 'responses', 'gemini_search_20170501.html')
            with open(path, 'r') as f:
                response = f.read()

        if 'fullheader' in url:
            path = os.path.join(settings.DATA_PATH, 'responses', 'N20170501S0001.fits.dat')
            with open(path, 'rb') as f:
                response = f.read()

        return HttpResponse(200, {}, 'text/html', response)

    def post_faker(url, **kwargs):
        return HttpResponse(200, {}, 'text/html', 'hello')

    import requests
    monkeypatch.setattr(requests, 'get', get_faker)
    monkeypatch.setattr(requests, 'post', post_faker)
