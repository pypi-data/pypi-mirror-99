"""
Session API
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class APISession(object):

    def __init__(self, url, token, project):
        self.api_url = url
        self.api_token = token
        self.project = project

        self.api_headers = {
            'Authorization': 'Token %s' % self.api_token,
            'User-Agent': 'Maestro CLI/1.0.9 - %s' % self.project
        }

        self.api = requests.Session()
        self.api.headers.update(self.api_headers)
        self.api.mount(
            self.api_url,
            HTTPAdapter(
                max_retries=Retry(total=5, backoff_factor=0.5)
            )
        )

    @property
    def base_jobrequest_url(self):
        return '%s/api/jobrequest/' % self.api_url
