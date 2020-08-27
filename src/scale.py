import base64
import json
from datetime import datetime

import requests
from timebetween import is_time_between

from bot_config import initialize_bot_config, BotConfig
from discord_utils import output

APP = 'salty-bastion-04148'
PROCESS = 'worker'
HEADERS = None


def scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except:
        return None
    if result.status_code == 200:
        return f"Successfully scaled to {size}!"
    else:
        return "Failed to scale"


def desired_heroku_scale_for(time, start, end):
    if is_time_between(time, start, end):
        return 1
    return 0


def build_heroku_api_request_headers(bot_config: BotConfig):
    utf_encoded_key = bot_config.heroku_api_key.encode("utf-8")
    # Generate Base64 encoded API Key
    base_key = base64.b64encode(utf_encoded_key)
    # Create headers for API call
    built_headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": base_key
    }
    return built_headers


if __name__ == '__main__':
    bot_config = initialize_bot_config(datetime.now())
    HEADERS = build_heroku_api_request_headers(bot_config)
    number_of_dynos = desired_heroku_scale_for(datetime.now().time(), bot_config.start_time, bot_config.end_time)
    result_msg = scale(number_of_dynos)
    output(result_msg)
    res = requests.post("https://nosnch.in/21999e7da7", data={"m": f"Scaled to {number_of_dynos} dynos"})
    output(res)
