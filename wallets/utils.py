from datetime import datetime
from zoneinfo import ZoneInfo

import requests


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")
    return response.json()


def get_current_date():
    return datetime.now(tz=ZoneInfo('UTC'))
