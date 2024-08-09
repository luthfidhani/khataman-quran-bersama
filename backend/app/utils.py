import uuid
import datetime


def generate_short_uuid():
    short_uuid = str(uuid.uuid4().hex[:6])
    return short_uuid


def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime
