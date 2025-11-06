from datetime import datetime
from time import time

def timestamp_to_datetime(seconds):
    return datetime.fromtimestamp(seconds)

print(timestamp_to_datetime(time()))
