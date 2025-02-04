import json

import requests

from dydx3.errors import DydxApiError
from dydx3.helpers.request_helpers import remove_nones

# TODO: Use a separate session per client instance.
session = requests.session()
session.headers.update({
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'dydx/python',
})


class Response(object):
    def __init__(self, data={}, headers=None):
        self.data = data
        self.headers = headers


def request(uri, method, headers=None, data_values={}, api_timeout=None, proxies=None):
    response = send_request(
        uri,
        method,
        headers,
        data=json.dumps(
            remove_nones(data_values)
        ),
        timeout=api_timeout,
        proxies=proxies,
    )
    if not str(response.status_code).startswith('2'):
        raise DydxApiError(response)

    if response.content:
        return Response(response.json(), response.headers)
    else:
        return Response('{}', response.headers)


def send_request(uri, method, headers=None, proxies=None, **kwargs):
    print('uri', uri)
    print('method', method)
    print('headers', headers)
    print('proxies', proxies)
    return getattr(session, method)(uri, headers=headers, proxies=proxies, **kwargs)
