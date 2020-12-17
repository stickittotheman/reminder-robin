import time
from datetime import timedelta


def format_timedelta(time_remaining_as_delta: timedelta):
    remaining = time.gmtime(int(time_remaining_as_delta.total_seconds()))
    return time.strftime("%H:%M:%S", remaining)


def generate_visual_countdown_str(time_remaining_as_delta: timedelta):
    return "........................"
