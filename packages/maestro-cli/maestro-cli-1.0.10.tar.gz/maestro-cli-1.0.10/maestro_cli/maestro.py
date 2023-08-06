"""
Maestro Gateway
"""
from maestro_cli.api import APISession
from maestro_cli.config import get_setting
from maestro_cli.jobrequest import JobRequest
from maestro_cli.utils import json_dumps


class Maestro(APISession):
    """
    Maestro High Level API
    """

    def __init__(self, url=None, token=None, project='unknown'):
        if token is None:
            token = get_setting('API', 'key')
        if url is None:
            url = get_setting('API', 'domain')

        super(Maestro, self).__init__(url, token, project)

    def launch_jobrequest(self,
                          jobdescriptor_id, datas={},
                          priority=0, auto_start=True):
        """
        Create and launch a JobRequest
        """
        payload = {
            'descriptor': '/api/jobdescriptor/%s/' % jobdescriptor_id,
            'priority': priority,
            'parameters': json_dumps(datas),
        }
        if auto_start:
            payload['auto_start'] = True

        response = self.api.post(
            self.base_jobrequest_url,
            data=payload
        )

        if response.status_code != 201:
            raise ValueError(
                'JobRequest cannot be launched [%s]\n%s' % (
                    response.status_code,
                    response.content
                )
            )

        return self.get_jobrequest(response.json()['id'])

    def get_jobrequest(self, jobrequest_id):
        """
        Acquire a JobRequest
        """
        return JobRequest(
            jobrequest_id,
            self.api_url,
            self.api_token,
            self.project
        )
