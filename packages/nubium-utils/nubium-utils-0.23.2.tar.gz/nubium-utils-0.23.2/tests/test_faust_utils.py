from unittest import mock, TestCase
from unittest.mock import patch
from nubium_utils.faust_utils import FaustAppWrapper
from nubium_utils.faust_utils import InstrumentedApp
from nubium_utils.faust_utils import get_ssl_context
from nubium_utils.faust_utils import faust_runtime_vars
import importlib


class ImplementedAppWrapper(FaustAppWrapper):

    def _init_agents(self):
        pass

    def _init_records(self):
        pass

    def _init_serializers(self):
        pass

    def _init_tables(self):
        pass

    def _init_topics(self):
        pass


class TestFaustAppWrapper(TestCase):
    """
    Tests the app wrapper
    """
    def tearDown(self):
        self.env_patch.stop()

    def setUp(self):
        self.env_patch = patch.dict(
            'os.environ',
            {
                "HOSTNAME": "TEST",
                "APP_NAME": "TEST",
                "TOPIC_PARTITIONS": "1"
            }
        )
        self.env_patch.start()
        importlib.reload(faust_runtime_vars)

    def test_app_creation(self):

        test_faust_config = {
            'id': 'test-id',
            'broker': 'kafka://test',
            'store': "memory://"
        }
        mock_monitor = mock.MagicMock()

        app_wrapper = ImplementedAppWrapper(test_faust_config, avro_client=None, metrics_manager=mock_monitor)
        assert app_wrapper.app.__class__ == InstrumentedApp

    def test_add_input_topic(self):

        test_faust_config = {
            'id': 'test-id',
            'broker': 'kafka://test',
            'store': "memory://"
        }
        mock_monitor = mock.MagicMock()
        mock_serializer = mock.MagicMock()

        app_wrapper = ImplementedAppWrapper(test_faust_config, avro_client=None, metrics_manager=mock_monitor)
        faust_topic = app_wrapper.add_input_topic('test_topic', mock_serializer)

        # Assert that method returns a faust_topic
        assert faust_topic.get_topic_name() == 'test_topic_Internal_test-id'

        # Assert that a input_topic is added
        input_topic = app_wrapper.input_topics['test_topic']

        # Assert that a converter agent was added
        converter_agent = app_wrapper.app.agents.data['test_topic_agent_internal']
        assert converter_agent.channel == input_topic


class TestFaustHelpers(TestCase):

    def test_no_ssl_context(self):
        """
        get_ssl_context returns None when `USE_SSL` env variable is False
        """
        with mock.patch('nubium_utils.faust_utils.helpers.env_vars') as mock_env:
            mock_env.return_value = {'USE_SSL': 'False'}
            output = get_ssl_context()
            assert output == {}

    def test_get_ssl_context(self):
        """
        SSL context configures from env variables when `USE_SSL` is True
        """
        with mock.patch('nubium_utils.faust_utils.helpers.env_vars') as mock_env:
            mock_env.return_value = {
                'USE_SSL': 'True',
                'SSL_CA_LOCATION': 'test-ca-location',
                'SSL_CERTIFICATE_LOCATION': 'test',
                'SSL_KEY_LOCATION': 'test'}
            with mock.patch('nubium_utils.faust_utils.helpers.ssl') as ssl_patch:
                output = get_ssl_context()['broker_credentials']
                ssl_patch.create_default_context.assert_called_once()
                output.load_cert_chain.assert_called_once()
