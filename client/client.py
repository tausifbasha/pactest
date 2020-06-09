import requests

BASE_URL = "http://localhost:5005"


def get_users_phone(user, endpoint='phone'):
    return requests.get('/'.join([BASE_URL, endpoint, user]))
