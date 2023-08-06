## Confluent-Kafka Consume/Produce patterns

### Asynchronous Single - fastest individual message throughput, (supposed) higher potential for duplicates

This setup **requires** the environment variable `CONSUMER_ENABLE_AUTO_COMMIT='true'` (the NU default setting)

Message consumptions are commited in batches behind the scenes.

May require tweaking some of the other "performance" configs (as found in `confluent_utils/confluent_runtime_vars.py`)
for individual app optimization.

```python
from confluent_kafka.avro import AvroConsumer, AvroProducer
from nubium_utils.custom_exceptions import NoMessageError
from nubium_utils.confluent_utils import consume_message, produce_message, handle_no_messages, enqueue_auto_commits, shutdown_cleanup
from my_example_app import do_stuff


import logging

LOGGER = logging.getLogger(__name__)


def example_app_loop(consumer, producer, metrics_manager):
    try:
        message_in = consume_message(consumer, metrics_manager)
        message_out = do_stuff(message_in)  # do your stuff!
        produce_message(producer, produce_dict, metrics_manager, message_out)    
        enqueue_auto_commits(consumer, message_in)
    except NoMessageError as e:
        handle_no_messages(e, producer=producer) # if no producer, skip arg accordingly

def example_app_init():
    consumer = AvroConsumer(consumer_config_dict)  # Your config dict here, as usual
    producer = AvroProducer(producer_config_dict)  # Your config dict here, as usual
    metrics_manager = MetricsManager()  # to setup properly, see "Monitoring" in README below

    try:
        while True:
            example_app_loop(consumer, producer, metrics_manager)
    finally:
        shutdown_cleanup(producer=producer, consumer=consumer)  # if no producer/consumer, skip arg accordingly
```


### Synchronous Single - Very slow, but (supposedly) less likely to cause duplicates

This setup **requires** the environment variables `CONSUMER_ENABLE_AUTO_COMMIT='false'`

This most closely emulates previous use patterns and is quite slow in comparison.

Probably best for when speed/throughput requirements are low, but the need for "exactly once" processing 
(or as close to it as possible) is high.

```python
from confluent_kafka.avro import AvroConsumer, AvroProducer
from nubium_utils.custom_exceptions import NoMessageError
from nubium_utils.confluent_utils import consume_message, produce_message, handle_no_messages, synchronous_message_handling, shutdown_cleanup
from my_example_app import do_stuff
import logging

LOGGER = logging.getLogger(__name__)


def example_app_loop(consumer, producer, metrics_manager):
    try:
        message_in = consume_message(consumer, metrics_manager)
        message_out = do_stuff(message_in)  # do your stuff!
        produce_message(producer, produce_dict, metrics_manager, message_out)
        synchronous_message_handling(producer=producer, consumer=consumer) # if no producer/consumer, skip args accordingly
    except NoMessageError as e:
        handle_no_messages(e, producer=producer) # if no producer, skip arg accordingly


def example_app_init():
    consumer = AvroConsumer(consumer_config_dict)  # Your config dict here, as usual
    producer = AvroProducer(producer_config_dict)  # Your config dict here, as usual
    metrics_manager = MetricsManager()  # to setup properly, see "Monitoring" in README below

    try:
        while True:
            example_app_loop(consumer, producer, metrics_manager)
    finally:
        shutdown_cleanup(producer=producer, consumer=consumer)  # if no producer/consumer, skip arg accordingly
```


### Synchronous Batch - When you need to consume `N` messages at once

This setup **requires** the environment variables `CONSUMER_ENABLE_AUTO_COMMIT='true'`.

This approach is only intended for very specific use cases, i.e. when you need to grab
N messages at once to package them for a bulk upload, for example. 
```python
from confluent_kafka.avro import AvroConsumer, AvroProducer
from nubium_utils.custom_exceptions import NoMessageError
from nubium_utils.confluent_utils import consume_message_batch, produce_message, handle_no_messages, enqueue_auto_commits, shutdown_cleanup
from my_example_app import do_stuff
import logging


LOGGER = logging.getLogger(__name__)


def example_app_loop(consumer, producer, metrics_manager):
    try:
        messages_in = consume_message_batch(consumer, metrics_manager, count=1000, timeout=15)
        messages_out = do_stuff(messages_in)  # do your stuff!
        for message_out in messages_out:
            produce_message(producer, produce_dict, metrics_manager, message_out)
        enqueue_auto_commits(consumer, messages_in)
    except NoMessageError as e:
        handle_no_messages(e, producer=producer) # if no producer, skip arg accordingly


def example_app_init():
    consumer = AvroConsumer(consumer_config_dict)  # Your config dict here, as usual
    producer = AvroProducer(producer_config_dict)  # Your config dict here, as usual
    metrics_manager = MetricsManager()  # to setup properly, see "Monitoring" in README below

    try:
        while True:
            example_app_loop(consumer, producer, metrics_manager)
    finally:
        shutdown_cleanup(producer=producer, consumer=consumer)  # if no producer/consumer, skip arg accordingly
```


## Monitoring
The monitoring utils enable metrics to be surfaced from the kafka applications
so the Prometheus server can scrape them.
The Prometheus server can't dynamically figure out pod IPs and scrape the
services directly, so we're using a metrics cache instead.

The metrics cache is a StatefulSet with 2 services assigned to it.
One service is a normal service, with a unique cluster IP address.
The prometheus server scrapes this service endpoint.
The other service doesn't have a cluster IP,
which means that the monitoring utility can find the IP addresses of each
of the backing pods, and send metrics to all of the pods.
This setup gives us high-availability guarantees.

The Monitoring utils are organized into two classes, `MetricsPusher` and `MetricsManager`.

The `MetricsManager` is a container for all of the metrics for the app,
and contains convenience methods for the 3 standardized metrics.
These metrics are
- `messages_consumed`: The number of messages consumed by the app
- `messages_produced`: The number of messages produced by the app
- `message_errors`: The number of exceptions caught in the app (labeled by type)

The `MetricsPusher` handles pushing the applications metrics to the metrics cache.
It determines the list of IP addresses for all of the metrics cache pods,
and sends the current metrics values for all of the metrics.

### Metric names and labels
The names of the metrics in Prometheus are the same as their names as parameters
- `messages_consumed`
- `messages_produced`
- `message_errors`

Two labels exist for every metric:
- `app`: The name of the microservice the metric came from
- `job`: The name of the individual pod the metric came from
The `message_errors` metric also has another label:
- `exception`: The name of the exception that triggered the metric

### Monitoring Setup Examples
The initialization and update loop for application monitoring will differ
from application to application based on their architecture.
The following examples should cover the standard designs we use.

#### Default Kafka Client Application
A Kafka application that directly relies on interacting with Producer or
Consumer clients should have it's monitoring classes set up and its
pushing thread started in the main run function and passed to the loop, as follows:
```python
import os

from confluent_kafka import Consumer, Producer
from nubium_utils.metrics import MetricsManager, MetricsPusher, start_pushing_metrics

def run_function():

    consumer = Consumer()
    producer = Producer()

    metrics_pusher = MetricsPusher(
        os.environ['HOSTNAME'],
        os.environ['METRICS_SERVICE_NAME'],
        os.environ['METRICS_SERVICE_PORT'],
        os.environ['METRICS_POD_PORT'])
    metrics_manager = MetricsManager(job=os.environ['HOSTNAME'], app=os.environ['APP_NAME'], metrics_pusher=metrics_pusher)
    start_pushing_metrics(metrics_manager, int(os.environ['METRICS_PUSH_RATE']))

    try:
        while True:
            loop_function(consumer, producer, metrics_manager=metrics_manager)
    finally:
        consumer.close()

```

The `consume_message()` function from this library expects a metrics_manager object
as an argument, so that it can increment the `messages_consumed` metric.

The application itself needs to increment the `messages_produced` metric
needs to be incremented as necessary by the application itself
whenever a Kafka message is produced. The convenience method on the metrics_manager
`inc_messages_produced()` makes this easier,
since it automatically adds the necessary labels to the metric.

The application also needs to be set to increment the `message_errors` metric
whenever an exception is caught.

An example loop function might look like this:
```python
import os
import logging

from nubium_utils import consume_message
from nubium_utils.custom_exceptions import NoMessageError


def loop_function(consumer, producer, metrics_manager):
    try:
        message = consume_message(consumer, int(os.environ['CONSUMER_POLL_TIMEOUT']), metrics_manager)
        outgoing_key = message.value()['email_address']
        producer.produce(topic='outgoing_topic',key=outgoing_key,value=message.value())
        metrics_manager.inc_messages_produced(1)
    except NoMessageError:
        pass
    except KeyError as error:
        metrics_manager.inc_message_errors(error)
        logging.debug('Message missing email address')


```

#### Flask Kafka Application
The setup becomes a little bit different with a Flask application.
The metrics_manager should be accessible through the app's configuration,
so that it can be accessed in route functions.

The preferred method for error monitoring is to hook into the built in
flask error handling loop, using the `@app.errorhandler` decorator.
Here is an example `create_app()` function

```python
import flask
from werkzeug.exceptions import HTTPException

from .forms_producer_app import forms_producer
from .util_blueprint import app_util_bp

def create_app(config):
    """
    Creates app from config and needed blueprints
    :param config: (Config) object used to configure the flask app
    :return: (flask.App) the application object
    """
    app = flask.Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(forms_producer)
    app.register_blueprint(app_util_bp)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """
        Increment error gauge on metrics_manager before returning error message
        """
        response = e.get_response()
        response.data = f'{e.code}:{e.name} - {e.description}'
        app.config['MONITOR'].inc_message_errors(e)
        return response

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        app.config['MONITOR'].inc_message_errors(error)
        return f'Unhandled exception: {error}', 500

    return app
```

The route functions for produced messages should increase the `messages_produced`
metric when necessary.
Example:
```python

@forms_producer.route('/', methods=["POST"])
@AUTH.login_required
def handle_form():
    """
    Ingests a dynamic form from Eloqua and produces it to the topic
    """
    values = request.json
    string_values = {key: str(value) for key, value in values.items()}
    LOGGER.debug(f'Processing form: {values}')

    current_app.config['PRODUCER'].produce(
        topic=current_app.config['TOPIC'],
        key=values['C_EmailAddress'],
        value={'form_data': string_values},
        on_delivery=produce_message_callback
    )
    current_app.config['MONITOR'].inc_messages_produced(1)

    return jsonify(success=True)
```

#### Faust Streams Application
Monitoring for the Faust streams application is much simpler.
The `FaustAppWrapper` base class in this library has builtin metrics_manager integration.
It sets metrics to the values of Faust's internally tracked metrics,
and increments the exception metric using Faust's error handling.
The standalone metric pushing thread isn't needed here;
instead, the `app.timer` decorator is used to define a pushing thread
that runs asynchronously as part of the Faust App

Simply import the `FaustAppWrapper` and define an app wrapper class from it
with your app's agents.

The metrics_manager and metrics pusher need to be initialized in the run file,
like this example:
```python
import os

from nubium_utils import get_ssl_context, MetricsManager, MetricsPusher
from nubium_utils.faust_utils import get_config

from duplicates_filter.duplicates_filter_app import FaustApp
from utilities.avro_utils import get_avro_client

ssl_context = get_ssl_context()
app_config = get_config()

metrics_pusher = MetricsPusher(job=os.environ['HOSTNAME'], metrics_service_name=os.environ['METRICS_SERVICE_NAME'], metrics_service_port=os.environ['METRICS_SERVICE_PORT'], metrics_pod_port=os.environ['METRICS_POD_PORT'])
metrics_manager = MetricsManager(job=metrics_pusher.job, app=app_config['id'], metrics_pusher=metrics_pusher)

duplicate_filter = FaustApp(
    app_config,
    avro_client=get_avro_client(),
    metrics_manager=metrics_manager,
    metrics_pusher=metrics_pusher
)
duplicate_filter.app.main()

```
