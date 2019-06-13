import os
import requests

_BASE_URL = 'https://api.waqi.info'
_WAQI_API_TOKEN = os.environ['WAQI_API_TOKEN']


def get_city_feed(city_name):
    return requests.get(f"{_BASE_URL}/feed/{city_name}/?token={_WAQI_API_TOKEN}").json()['data']
