class NoMessageError(Exception):
    """
    No message was returned when consuming from the broker
    """
    def __init__(self, *args):
        if not args:
            default_message = "No messages to consume"
            args = (default_message,)
        super().__init__(*args)


class NetworkError(Exception):
    """
    Generic handler for non-breaking, network-related external call failure.
    """
    def __init__(self, *args, req_status_code=None):
        self.req_status_code = 500
        if req_status_code:
            self.req_status_code = req_status_code
        if not args:
            default_message = f'Encountered a network-related external call failure, status code {self.req_status_code})'
            args = (default_message,)
        super().__init__(*args)


class ConsumeMessageError(Exception):
    """
    Non-trivial errors when consuming from the broker
    """
    pass


class MessageValueException(Exception):
    """
    Represents a significant error in the value of the message
    """
    pass


class ProduceHeadersException(Exception):
    """
    Represents a significant error in the value of the message
    """
    pass


class ProducerTimeoutFailure(Exception):
    """ Exception signifying a producer failing to communicate with the broker(s). """
    def __init__(self, *args):
        if not args:
            default_message = "Producer could not reach the broker(s) when attempting to send a message."
            args = (default_message,)
        super().__init__(*args)


class MaxRetriesReached(Exception):
    """
    Represents that all retry attempts for a retry-looped app have failed.
    """
    def __init__(self, *args):
        if not args:
            default_message = "All app retry attempts have failed"
            args = (default_message,)
        super().__init__(*args)


class RetryTopicSend(Exception):
    """
    Represents that an external call has failed but further retries will be attempted.
    Only a placeholder for logging a message sent to a retry topic when the app did not provide an explicit exception.
    """
    def __init__(self, *args):
        if not args:
            default_message = "External call attempt has failed, but will retry."
            args = (default_message,)
        super().__init__(*args)


class FailureTopicSend(Exception):
    """
    Represents that an external call has failed and no further retries will be attempted.
    Only a placeholder for logging a message sent to a failure topic when the app did not provide an explicit exception.
    """
    def __init__(self, *args):
        if not args:
            default_message = "External call attempt has failed and no (additional?) retries will be attempted."
            args = (default_message,)
        super().__init__(*args)


class IncompatibleEnvironmentError(Exception):
    def __init__(self, env_var_name, env_var_value, *args):
        default_message = f"The method called is not compatible with the env var {env_var_name}=={env_var_value}"
        args = (default_message, *args)
        super().__init__(*args)
