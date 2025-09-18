import os
import logging

import requests
import json

from datetime import datetime
from config import API_URL, API_HEADERS, DATA_RAW_PATH


def dump_raw_data(data, date : datetime) -> None:

    filename = "responce.json"
    filepath = os.path.join(DATA_RAW_PATH, date.strftime("%Y-%m-%d"), filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def fetch_data() -> None:

    response = requests.get(API_URL, headers=API_HEADERS)

    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.now()
        dump_raw_data(data, timestamp)
    else:
        logging.error(f"Can't read API call. Responce code: {response.status_code}.")
        raise Exception(f"APIRequestError: {response.status_code}. Response content: {response.json()}")
    

if __name__ == "__main__":
    fetch_data()