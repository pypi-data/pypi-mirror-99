import json
import requests


class MovideskClient:
    HOST = 'https://api.movidesk.com/public/v1'
    HEADERS = {
        'Content-Type': 'application/json',
    }
    RESOURCES = {
        'persons': '/persons',
        'tickets': '/tickets',
    }

    def __init__(self, token):
        self.token = token

    def _get_url(self, resource):
        return '{}{}?token={}'.format(self.HOST, resource, self.token)

    def person_create(self, data):
        url = self._get_url(self.RESOURCES['persons'])
        return requests.post(url, json.dumps(data), headers=self.HEADERS)

    def ticket_create(self, data):
        url = self._get_url(self.RESOURCES['tickets'])
        return requests.post(url, json.dumps(data), headers=self.HEADERS)
