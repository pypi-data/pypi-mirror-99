import logging
from json import dumps

from nubium_utils import parse_headers
from nubium_utils.custom_exceptions import ProduceHeadersException, ProducerTimeoutFailure, MaxRetriesReached, RetryTopicSend, FailureTopicSend
from nubium_utils.metrics import MetricsManager
from .confluent_runtime_vars import env_vars

LOGGER = logging.getLogger(__name__)


def confirm_produce(producer, attempts=3, timeout=20):
    """
    Ensure that messages are actually produced by forcing synchronous processing. Must manually check the events queue
    and see if it's truly empty since flushing timeouts do not actually raise an exception for some reason.

    NOTE: Only used for synchronous producing, which is dramatically slower than asychnronous.
    """
    attempt = 1
    while producer.__len__() > 0:
        if attempt <= attempts:
            LOGGER.debug(f"Produce flush attempt: {attempt} of {attempts}")
            producer.flush(timeout=timeout)
            attempt += 1
        else:
            raise ProducerTimeoutFailure


def produce_message(producer, producer_kwargs: dict, metrics_manager: MetricsManager,
                    consumed_msg_headers_passthrough: tuple = ()):
    """
    Helper for producing a message with confluent_kafka producers; primarily handles headers passthrough and enforcing
    all required headers fields exist before producing.
    You can pass in the previous message headers via 'consumed_msg_headers_passthrough', which extracts the headers.
    Then, if you wish to overwrite any of them, you can provide your own "headers" keyword in 'producer_kwargs'
    which will take that dict and overwrite any matching key in the 'consumed_msg_headers_passthrough' argument.
    You can also provide a None value for a key to remove it entirely.
    :param producer: A confluent_kafka producer
    :type: confluent_kafka.Producer or confluent_kafka.avro.AvroProducer
    :param producer_kwargs: the kwargs to pass into the producer instance
    :type producer_kwargs: dict
    :param metrics_manager: a MetricsManager object instance
    :type metrics_manager: MetricsManager
    :param consumed_msg_headers_passthrough: confluent_kafka Message.headers() from a consumed msg; will add all to new message
    :type consumed_msg_headers_passthrough: tuple
    """
    required_fields = ['guid', 'last_updated_by']

    if 'header' in producer_kwargs:
        raise KeyError('"header" is not the appropriate key for producing message headers; use "headers" instead')

    headers_out = parse_headers(consumed_msg_headers_passthrough)
    headers_out.update(producer_kwargs.get('headers', {}))
    headers_out = {key: value for key, value in headers_out.items() if value is not None}
    missing_required_keys = [key for key in required_fields if key not in headers_out]
    if missing_required_keys:
        raise ProduceHeadersException(f'Message headers are missing the required key(s): {missing_required_keys}')
    producer_kwargs['headers'] = headers_out

    LOGGER.debug('Polling for previous successful produce callbacks before adding additional produces to queue...')
    producer.poll(0)
    LOGGER.debug(f'Adding a message to the produce queue for topic {producer_kwargs["topic"]}')
    producer.produce(**producer_kwargs)
    metrics_manager.inc_messages_produced(1, producer_kwargs['topic'])
    LOGGER.info(f'Message added to the produce queue; GUID {headers_out.get("guid")}')


def produce_retry_message(message, producer, exception=None, value_schema=None):
    """
    Produces a message to the correct retry topic with an updated header
    Note: "exception" can be an Exception or plain str.

    The message header should contain a `kafka_retry_count` field,
    which is an integer representation of how many times the message has
    been tried for the current topic.
    If greater than the allowed maximum, produces to the retry topic.
    If less than the allowed maximum, produces to the current topic.
    """

    headers = dict(message.headers())
    guid = headers.get('guid', b'N/A').decode()
    kafka_retry_count = int(headers.get('kafka_retry_count', '0'))
    retry_topic = None
    if not value_schema:
        value_schema = producer._value_schema

    if kafka_retry_count < int(env_vars()['RETRY_COUNT_MAX']):
        headers['kafka_retry_count'] = str(kafka_retry_count + 1)
        retry_topic = env_vars()['CONSUME_TOPICS']
    else:
        headers['kafka_retry_count'] = '0'
        retry_topic = env_vars().get('PRODUCE_RETRY_TOPICS', '')

    if retry_topic:
        if not exception:
            exception = RetryTopicSend()
        LOGGER.warning('; '.join([str(exception), f'retrying GUID {guid}']))
        LOGGER.debug('Polling for previous successful produce callbacks before adding additional produces to queue...')
        producer.poll(0)
        producer.produce(
            topic=retry_topic,
            value=message.value(),
            key=message.key(),
            headers=headers,
            value_schema=value_schema)
        confirm_produce(producer)
    else:
        if not exception:
            exception = FailureTopicSend()
        LOGGER.error('; '.join([str(exception), f'GUID {guid}']))
        produce_failure_message(message, producer, exception=MaxRetriesReached(), value_schema=value_schema)


def produce_failure_message(message, producer, exception=None, value_schema=None):
    """
    Produces a message onto a deadletter queue.
    Note: "exception" can be an Exception or plain str.
    """
    if not value_schema:
        value_schema = producer._value_schema
    headers = dict(message.headers())
    guid = headers.get('guid', b'N/A').decode()
    headers['kafka_retry_count'] = '0'

    if not exception:
        exception = FailureTopicSend()
    LOGGER.error('; '.join([type(exception).__name__, str(exception), f'failing GUID {guid}']))
    headers["exception"] = dumps({"name": type(exception).__name__, "description": str(exception)})

    LOGGER.debug('Polling for previous successful produce callbacks before adding additional produces to queue...')
    producer.poll(0)
    LOGGER.debug(f'Adding a message to the produce queue for deadletter/failure topic {env_vars()["PRODUCE_FAILURE_TOPICS"]}')
    producer.produce(
        topic=env_vars()['PRODUCE_FAILURE_TOPICS'],
        value=message.value(),
        key=message.key(),
        headers=headers,
        value_schema=value_schema)
    LOGGER.info(f'Message added to the deadletter/failure topic produce queue; GUID {guid}')
