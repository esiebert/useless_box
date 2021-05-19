# pylint: disable=[missing-module-docstring,missing-function-docstring,redefined-outer-name]
# pylint: disable=[protected-access]
import pytest
import json
from freezegun import freeze_time
from unittest.mock import MagicMock, Mock

from consumer.main import Consumer


@pytest.fixture
def mock_message_broker(mocker):
    return mocker.patch("common.message_broker.MessageBroker")

@pytest.fixture
def mock_processor(mocker):
    return mocker.patch("consumer.processor.sum_numbers", return_value=42)

@pytest.fixture
def consumer(mock_message_broker, mock_processor):
    consumer = Consumer(
        message_broker=mock_message_broker,
        processor=mock_processor,
    )
    mock_message_broker.setup_callback.assert_called_once_with(consumer._callback)
    return consumer

def test_consumer_start(consumer, mock_message_broker):
    consumer.start()
    mock_message_broker.start_consuming.assert_called_once()

@freeze_time('1212-12-12T12:12:12')
def test_consumer_callback(consumer, mock_processor, mock_message_broker):
    # Mock channel and method so that basic_ack doesn't raise an exception
    mock_channel = MagicMock()
    mock_channel.basic_ack = Mock(return_value=None)

    mock_method = MagicMock()
    mock_method.delivery_tag = Mock(return_value=None)

    consumer._callback(mock_channel, mock_method, None, b'')
    mock_processor.assert_called_once_with('')
    mock_message_broker.publish.assert_called_once_with(
        body=json.dumps({
            'timestamp': "1212-12-12 12:12:12",
            'code': '',
            'result': 42,
        })
    )
