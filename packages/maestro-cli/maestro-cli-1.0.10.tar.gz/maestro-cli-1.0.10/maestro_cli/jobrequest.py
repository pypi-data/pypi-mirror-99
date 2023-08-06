"""
Maestro JobRequest
"""
import time

from maestro_cli.api import APISession
from maestro_cli.utils import deep_get

CACHE_TIMEOUT = 3


class JobRequest(APISession):
    """
    JobRequest High Level API
    """

    def __init__(self, request_id, url, token, project):
        super(JobRequest, self).__init__(url, token, project)
        self.request_id = request_id
        self._cache = None
        self._cache_time = None
        self.datas  # Populate cache

    def fetch_datas(self):
        """
        Fetch the JobRequest datas
        """
        response = self.api.get(
            '%s%s/' % (self.base_jobrequest_url, self.request_id)
        )

        if response.status_code == 401:
            raise ValueError('Invalid credentials')

        if response.status_code != 200:
            raise ValueError('JobRequest #%s does not exist' % self.request_id)

        return response.json()

    @property
    def datas(self):
        """
        Most recent datas about the JobRequest
        """
        if not self._cache or (
                time.time() > self._cache_time + CACHE_TIMEOUT
        ):
            self._cache = self.fetch_datas()
            self._cache_time = time.time()

        return self._cache

    def __getattr__(self, name):
        """
        Magic accessor for properties of JobRequest
        """
        if name not in self.__dict__:
            if name in self.datas:
                return self.datas[name]
            raise AttributeError('%s is not a valid attribute' % name)

        return self.__dict__[name]

    def __repr__(self):
        return '<JobRequest #%s>' % self.request_id

    # Actions
    def action(self, action_url):
        """
        Launch an action of the JobRequest
        """
        response = self.api.post(action_url)

        content = response.json()

        if response.status_code != 200:
            message = content['job request'].encode('utf-8')

            raise ValueError(
                'JobRequest #%s : %s' % (self.request_id, message)
            )

        return content

    def start(self):
        """
        Start a JobRequest
        """
        return self.action(self.datas['start'])

    def restart(self):
        """
        Restart a JobRequest
        """
        return self.action(self.datas['restart'])

    def cancel(self):
        """
        Cancel a JobRequest
        """
        return self.action(self.datas['cancel'])

    def complete(self):
        """
        Complete a JobRequest
        """
        return self.action(self.datas['complete'])

    def search_tasks(self, search_parameters={}):
        jobrequest_datas = self.datas
        tasks = []
        for task in jobrequest_datas.get('tasks', []):
            valid_task = True
            for task_key, search_value in search_parameters.items():
                if deep_get(task, task_key, '') != search_value:
                    valid_task = False
                    break

            if valid_task:
                tasks.append(task)

        return tasks
