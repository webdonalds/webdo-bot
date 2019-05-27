import requests

_BASE_URL = 'https://apis.tracker.delivery'


def list_carriers():
    return requests.get(f"{_BASE_URL}/carriers").json()


def get_tracking(carrier_id, track_id):
    return requests.get(f"{_BASE_URL}/carriers/{carrier_id}/tracks/{track_id}").json()
