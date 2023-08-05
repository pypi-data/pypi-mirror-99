import copy
import requests
from .constants import BASE_API_URL, LATEST_API_VERSION


class PathConstruct():

    def __init__(self):
        self.url = f'{BASE_API_URL}/{LATEST_API_VERSION}'

    def transform_url(self, module, path):
        return f'{self.url}/{module}/{path}/'


class RequestConstructor(PathConstruct):

    def __init__(self, api_key):
        super(RequestConstructor, self).__init__()
        self.api_key = api_key

    def prepare_headers(self, headers):
        result = copy.deepcopy(headers)
        result.update({
            "X-Api-Key": self.api_key
        })
        return result

    def request(self, method, url, data={}, headers={}, params={}):
        kwargs = {
            'headers': self.prepare_headers(headers),
            'data': data,
            'params': params
        }
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
