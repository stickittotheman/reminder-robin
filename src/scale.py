import base64
import json
from datetime import datetime, time, timedelta

import requests

from bot_config import initialize_bot_config, BotConfig
from discord_utils import output

APP = 'salty-bastion-04148'
PROCESS = 'worker'
HEADERS = None
ARBITRARY_DATE = datetime(1988, 3, 14)


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


def build_heroku_api_request_headers(the_bot_config: BotConfig):
    utf_encoded_key = the_bot_config.heroku_api_key.encode("utf-8")
    # Generate Base64 encoded API Key
    base_key = base64.b64encode(utf_encoded_key)
    # Create headers for API call
    built_headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": base_key
    }
    return built_headers


def is_time_between(t, start, end):
    if start == end:
        return True
    day_add = 1 if end < start else 0
    end_add = 1 if day_add and end == time(0, 0, 0, 0) else 0
    test_add = 1 if day_add and t < start else 0
    td_time_start = timedelta(hours=start.hour,
                              minutes=start.minute,
                              seconds=start.second,
                              microseconds=start.microsecond)
    td_time_end = timedelta(days=day_add + end_add,
                            hours=end.hour,
                            minutes=end.minute,
                            seconds=end.second,
                            microseconds=end.microsecond)
    td_testing = timedelta(days=test_add,
                           hours=t.hour,
                           minutes=t.minute,
                           seconds=t.second,
                           microseconds=t.microsecond)
    start_date = ARBITRARY_DATE + td_time_start
    end_date = ARBITRARY_DATE + td_time_end
    testing_date = ARBITRARY_DATE + td_testing
    return start_date <= testing_date <= end_date


if __name__ == '__main__':
    bot_config = initialize_bot_config(datetime.now())
    HEADERS = build_heroku_api_request_headers(bot_config)
    number_of_dynos = desired_heroku_scale_for(datetime.now().time(), bot_config.start_time, bot_config.end_time)
    result_msg = scale(number_of_dynos)
    output(result_msg)
    res = requests.post("https://nosnch.in/21999e7da7", data={"m": f"Scaled to {number_of_dynos} dynos"})
    output(res)
