import uuid
from time import sleep
from .general_runtime_vars import env_vars


def generate_guid():
    return str(uuid.uuid1())


def parse_headers(msg_header):
    """
    Converts headers to a dict
    :param msg_header: A message .headers() (confluent) or .headers (faust) instance
    :return: a decoded dict version of the headers
    """
    if msg_header:
        msg_header = dict(msg_header)
        return {key: value.decode() for key, value in msg_header.items()}
    return {}


def log_and_raise_error(metrics_manager, error):
    """
    Since the metric manager pushing is a separate thread, ensure an exception gets sent to prometheus
    """
    metrics_manager.inc_message_errors(error)
    sleep(int(env_vars()['METRICS_PUSH_RATE']) * 2 + 1)
    raise
