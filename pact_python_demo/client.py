import requests


class UserClient(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_user(self, user_name):
        """Fetch a user object by user_name from the server."""
        uri = self.base_uri + '/users/' + user_name
        response = requests.get(uri);
        if response.status_code == 404:
            return None
        return response.json()

    def get_user_with_header(self, user_name,header = None):
        """Fetch a user object by user_name from the server."""
        uri = self.base_uri + '/users/' + user_name
        response = requests.get(uri,headers = header);
        if response.status_code == 404:
            return None
        return response.json()