import requests
__all__ = ["Request"]

class Request():
    def __init__(
        self,
        endpoint,
        headers
    ):
        self._endpoint = endpoint
        self._headers = headers
    def get_graphql_url(self):
        return "{endpoint}/{path}".format(
            endpoint=self._endpoint,
            path='graphql'
        )
    def get_url(self, path):
        return "{endpoint}/{path}".format(
            endpoint=self._endpoint,
            path=path
        )
    def post(self, payload):
        http_response = {}
        try:
            http_response = requests.post(
                self.get_graphql_url(),
                json=payload,
                headers=self._headers
            )
            http_response.raise_for_status()
        except Exception as err:
            if http_response.content:
                print(f'Error occurred: {err}, content: {http_response.content}')
            else:
                print(f'Error occurred: {err}')
        else:
            data = http_response.json()
            if "error" in data:
                print(f'Error occurred: {data.error}')
            return data.get('data')
    def get(self, path):
        http_response = {}
        try:
            http_response = requests.get(
                self.get_url(path),
                headers=self._headers
            )
            http_response.raise_for_status()
        except Exception as err:
            content = http_response.get('content')
            print(f'Error occurred: {err}, {content}')
        else:
            data = http_response.json()
            if "error" in data:
                error = data.get('error')
                print(f'Error occurred: {error}')
            return data

